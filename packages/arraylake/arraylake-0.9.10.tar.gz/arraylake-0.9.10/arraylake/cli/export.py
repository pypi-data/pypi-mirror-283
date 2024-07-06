import asyncio
import hashlib
import queue
import re
import threading
import time
import warnings
from enum import Enum
from functools import partial
from os import rename
from os.path import isfile

import humanize
import s3fs
import tenacity
import yaml
import zarr
from sqlitedict import SqliteDict
from zarr.core import Array

from arraylake import zarr_util
from arraylake.cli.utils import simple_progress
from arraylake.client import AsyncClient, Client
from arraylake.repo import Repo
from arraylake.types import CollectionName, DBIDBytes


class SupportedExportFormats(str, Enum):
    zarr2 = "zarr2"
    zarr3alpha = "zarr3alpha"


class ExportTarget:
    # FIXME: More sanity checks on the target
    def __init__(self, destination, format, extra_config):
        self.destination = destination
        self.format = format
        self.extra_config = extra_config
        self.transform_path = self._get_path_transformer()

    async def setup(self, loop=None):
        zarr_version = None
        if self.format == SupportedExportFormats.zarr2:
            zarr_version = 2
        elif self.format in {
            SupportedExportFormats.zarr3alpha,
        }:
            # FIXME: We need to do some library checks to see which v3 the
            # customer is intending to target...
            zarr_version = 3
        else:
            raise NotImplementedError

        if self.extra_config is None:
            extra_config_data = {}
        elif isinstance(self.extra_config, dict):
            extra_config_data = self.extra_config
        else:
            with open(self.extra_config) as f:
                extra_config_data = yaml.safe_load(f)

        # if using S3, we need to set up special options
        if str(self.destination).startswith("s3://"):
            fs = s3fs.S3FileSystem(
                anon=False,
                endpoint_url=extra_config_data.get("endpoint_url"),
                key=extra_config_data.get("access_key_id"),
                secret=extra_config_data.get("secret_access_key"),
            )
            store = fs.get_mapper(root=self.destination, check=False)
        else:
            store = self.destination

        self.group = zarr.open_group(store=store, mode="a", zarr_version=zarr_version)

    def _get_path_transformer(self):
        match self.format:
            case SupportedExportFormats.zarr2:
                # convert from data/root/foo/bar/c0/1/2 -> /foo/bar/0.1.2
                chunk_path_pattern = r"c\d+(\/\d+)*$"
                path_offset = len(zarr_util.DATA_ROOT)
                assert path_offset == len(zarr_util.META_ROOT)

                def _rewrite(source_path):
                    # chop off the "data/root/" or "meta/root/" prefixes
                    logical_path = source_path[path_offset:]

                    # if this is a chunk path, translate from slash- to
                    # dot-delimited
                    match = re.search(chunk_path_pattern, logical_path)
                    if match:
                        i = match.start()
                        array_prefix = logical_path[:i]
                        chunk_path = logical_path[i:][1:].replace("/", ".")
                        return f"{array_prefix}{chunk_path}"
                    else:
                        return logical_path

                return _rewrite
            case SupportedExportFormats.zarr3alpha:
                return lambda path: path
            case _:
                raise NotImplementedError

    def delete(self, source_path) -> None:
        dest_path = self.transform_path(source_path)
        del self.group.store[dest_path]
        assert dest_path not in self.group.store

    def write(self, source_path, bytes) -> int:
        dest_path = self.transform_path(source_path)
        self.group.store[dest_path] = bytes
        return len(bytes)


class ExportManager:
    def __init__(
        self,
        repo: str | Repo,
        target: ExportTarget,
        *,
        ref: None | str = None,
        from_ref: None | str = None,
        concurrency: int = 64,
        validate: bool = False,
    ):
        if isinstance(repo, str):
            self.repo_name = repo
            self.repo = None
        elif isinstance(repo, Repo):
            self.repo = repo
            self.repo_name = repo._arepo.repo_name
        self.from_ref = from_ref
        self.ref = ref

        self.from_commit: DBIDBytes | None = None
        self.as_of_commit: DBIDBytes | None = None

        self.target = target
        self.concurrency = concurrency
        self.validate = validate

        self.stats = {"n_chunks": 0, "n_bytes": 0, "n_seconds": 0.0}

    async def __aenter__(self):
        # Check out repos
        with simple_progress(f"Checking out [bold]{self.repo_name}[/bold]..."):
            await self._checkout()

        # Set up statefile and init destination
        await self.target.setup(loop=asyncio.get_running_loop())
        self.statefile = await self._init_statefile()

        # contains a list of paths to be transferred
        # TODO: put the contents of the statefile as well
        self.download_queue: queue.Queue = queue.Queue()
        # contains a tuple of (path, bytes) to be written
        self.upload_queue: queue.Queue = queue.Queue(maxsize=self.concurrency)
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        # FIXME: If completed successfully, delete the statefile?
        assert self.statefile
        self.statefile.close()

        # Regardless of whether the transfer was a success or not, print a
        # summary report with the relevant metadata and stats.
        print(self.report())

    async def _checkout(self):
        self.repo = Client().get_repo(self.repo_name, checkout=False)

        if self.ref:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="You are not on a branch tip", category=UserWarning)
                self.repo.checkout(self.ref, for_writing=True)
        else:
            self.repo.checkout(for_writing=True)

        client = AsyncClient()
        self.async_repo = await client.get_repo(self.repo_name, checkout=False)

        self.as_of_commit = self.repo.session.base_commit
        assert self.as_of_commit
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="You are not on a branch tip", category=UserWarning)
            await self.async_repo.checkout(self.as_of_commit, for_writing=True)

        if self.from_ref:
            self.from_commit, _ = await self.async_repo._get_ref_for_checkout(self.from_ref)

    async def _changes_since(self, commit_id):
        metadata_collection = CollectionName("metadata")
        chunks_collection = CollectionName("chunks")
        nodes_collection = CollectionName("nodes")

        # Iterate over all commits, in chronological order, fetching
        # the deltas across all collections.
        assert self.repo is not None
        log = self.repo.commit_log
        changes = {}
        commits = []
        for commit in log:
            if commit.id == commit_id:
                break
            else:
                commits.append(commit)

        for commit in reversed(commits):
            for collection in (
                metadata_collection,
                chunks_collection,
                nodes_collection,
            ):
                # FIXME: These are synchronous and serialized, which kills
                # performance. I'd really prefer that all of this happened
                # asynchronously. Not a high priority in the grand scheme of
                # things, but this should be rewritten to use arepo and act
                # as an async generator.
                for change in self.repo._wrap_async_iter(
                    self.repo._arepo.db.get_all_paths_for_commit,
                    commit_id=commit.id,
                    collection=collection,
                ):
                    changes[change.path] = {"d": change.deleted, "t": 0, "c": False}

                # assert(self.async_repo)

                # # FIXME: chunk this up a bit using _get_chunk_refs()
                # async for change in self.async_repo.db.get_all_paths_for_commit(commit.id, collection=collection):
                #     if change.deleted:
                #         changes[change.path] = None
                #     else:
                #         changes[change.path] = await self.async_repo._get_chunk_ref(change.path)

        return changes

    def _args_from_array(self, arr):
        return {
            "shape": arr.shape,
            "chunks": arr.chunks,
            "dtype": arr.dtype,
            "compressor": arr.compressor,
            "order": arr.order,
            "filters": arr.filters,
            "fill_value": arr.fill_value,
        }

    # NOTE: This process is currently not checkpointed, so it does not
    # support resumption. It is also dog slow.
    def _copy_metadata(self, statefile, path, item):
        assert self.repo is not None
        src = self.repo.root_group[path]
        dest = None

        if isinstance(src, Array):
            dest = self.target.group.create_dataset(path, **self._args_from_array(src), overwrite=True)
            # Load all the chunk paths for the array into the statefile.
            # FIXME: This could be rewritten to take advantage of arepo and
            # consume the async generator _list_prefix.
            for chunk_path in self.repo.root_group.store.list_prefix(f"{zarr_util.DATA_ROOT}{path}"):
                # FIXME: add to statefile only if it doesn't already exist
                statefile[chunk_path] = {
                    "d": False,  # path to be deleted?
                    "t": 0,  # n_bytes transferred
                    "c": False,  # checksum validated?
                }

            statefile.commit()
        else:
            dest = self.target.group.require_group(path, overwrite=False)
        dest.attrs.update(**src.attrs.asdict())

    def _mk_statefile_name(self):
        # FIXME: Don't shove so much metadata into the filename. Use a proper
        # metadata table for all this info.
        repo = self.repo_name.replace("/", ".")
        from_commit = f"{self.from_commit}-" if self.from_commit else ""
        assert self.repo is not None
        to_commit = self.repo.session.base_commit
        target_hash = hashlib.sha256(str(self.target.destination).encode()).hexdigest()[:10]

        return f"{repo}.{from_commit}{to_commit}.{target_hash}.state"

    async def _init_statefile(self):
        assert self.repo is not None
        self.statefile_name = self._mk_statefile_name()
        if not isfile(self.statefile_name):
            # We don't have an existing statefile, which means we need to set
            # one up and initialize the destination store.
            temp_statefile_name = f"{self.statefile_name}.incomplete"
            temp_statefile = SqliteDict(temp_statefile_name)

            if self.from_commit:
                # The user wants an incremental update.
                with simple_progress(
                    f"Generating manifest from changes between [bold]{self.from_commit}[/bold] and [bold]{self.as_of_commit}[/bold]..."
                ):
                    changes = await self._changes_since(self.from_commit)

                    # Add data and metadata changes, including deletes.
                    for path, body in changes.items():
                        temp_statefile[path] = body
                    temp_statefile.commit()
            else:
                # This is a new export.
                with simple_progress(f"Generating manifest for full export as of [bold]{self.as_of_commit}[/bold]..."):
                    # FIXME: This is reeeeeeeeeeally slow.
                    self.repo.root_group.visititems(partial(self._copy_metadata, temp_statefile))
                    # don't forget the root group metadata
                    self._copy_metadata(temp_statefile, "", self.repo.root_group)

            # Once all changes have been committed, close the file and
            # move it to its proper location. This functions as a rough
            # transactional mechanism, so that we know any statefile without
            # the ".incomplete" suffix is complete. This prevents partial
            # exports.
            temp_statefile.close()
            rename(temp_statefile_name, self.statefile_name)

        return SqliteDict(self.statefile_name)

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_random_exponential(multiplier=1, max=60),
    )
    def _download_item(self):
        assert self.repo is not None
        path, change = self.download_queue.get()
        assert change["t"] == 0
        if change["d"]:
            # FIXME: validate this works for metadata updates
            self.target.delete(path)

            # we set "t" to -1 to indicate that the path has been
            # successfully deleted
            self.statefile[path] = {"d": True, "t": -1, "c": False}
        else:
            if zarr_util.is_chunk_key(path):
                # repo has no validate kwarg
                raw_data = self.repo._get_chunk(path)  # , validate=self.validate)
            else:
                pass
                # does this happen? why?
            # add to upload queue (potentially block if queue is full)
            self.upload_queue.put((path, raw_data))

        self.download_queue.task_done()

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_random_exponential(multiplier=1, max=60),
    )
    def _upload_item(self):
        path, raw_data = self.upload_queue.get()
        n_bytes = self.target.write(path, raw_data)
        n_chunks = 1
        self.statefile[path] = {
            "d": False,
            "t": n_bytes,
            "c": self.validate,
        }
        self.statefile.commit()
        self.upload_queue.task_done()
        self.stats["n_chunks"] += n_chunks
        self.stats["n_bytes"] += n_bytes
        self.pbar.update(self.task_id, advance=n_chunks)

    async def copy_data(self):
        assert self.statefile

        start_time = time.time()
        n_items = len(self.statefile)

        with simple_progress(
            f"Exporting chunks to [bold]{self.target.destination}[/bold]... ",
            total=n_items,
        ) as progress:
            assert progress
            self.pbar = progress[0]
            self.task_id = progress[1]

            # Although slightly slower, using a deterministic sorting for the keys
            # ensures a more pleasant user experience, as the progress bar resumes
            # from where it left off.
            for path, change in sorted(self.statefile.items()):
                if change["t"] == 0:
                    self.download_queue.put_nowait((path, change))
                else:
                    self.pbar.update(self.task_id, advance=1)

            def download_worker_function():
                while True:
                    self._download_item()

            def upload_worker_function():
                while True:
                    self._upload_item()

            nworkers = self.concurrency // 2
            for _ in range(nworkers):
                threading.Thread(target=download_worker_function, daemon=True).start()
                threading.Thread(target=upload_worker_function, daemon=True).start()

            self.download_queue.join()
            self.upload_queue.join()
        self.stats["n_seconds"] = time.time() - start_time

    def report(self):
        extended_stats = {}
        if self.stats["n_seconds"] > 0:
            chunk_rate = self.stats["n_chunks"] / self.stats["n_seconds"]
            transfer_rate = self.stats["n_bytes"] / self.stats["n_seconds"]
            extended_stats = {
                "state_file": self.statefile_name,
                "chunk_rate": f"{chunk_rate:.1f}/s",
                "transfer_rate": f"{humanize.naturalsize(transfer_rate)}/s",
            }

        return self.stats | extended_stats
