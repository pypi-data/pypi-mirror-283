#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from abc import abstractmethod
import asyncio
import json
import os
import time
from typing import Any, Callable, Optional

from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor

from ngcbpc.environ import NGC_CLI_PROGRESS_UPDATE_FREQUENCY
from ngcbpc.transfer.utils import (
    bitmask_clear_bit,
    bitmask_is_bit_set,
    bitmask_set_bit_in_size,
)

# contractral constant, cannot be modified without agreement
PARTITION_SIZE = 500000000

# This line instruments aiohttp client sessions and requests, enabling tracing functionality.
# It adds default trace configuration options to all aiohttp requests
AioHttpClientInstrumentor().instrument()

# This line instruments all asyncio functions, enabling tracing without the need to pass a tracer explicitly.
# In asyncio workers, where different contexts may exist for the overall execution and individual worker tasks,
# this instrumentation ensures that tracing captures and respects the distinct contexts of each worker's execution.
AsyncioInstrumentor().instrument()


class AsyncTransferProgress:
    """Track overall transfer progress for a transfer,
    and calls provided callback with a specified maximum update rate,
    including completed, failed, and total bytes and counts.

    Args:
        completed_bytes (int): The number of completed bytes.
        failed_bytes (int): The number of failed bytes.
        total_bytes (int): The total number of bytes.
        completed_count (int): The number of completed items.
        failed_count (int): The number of failed items.
        total_count (int): The total number of items.
        callback_func (Optional[Callable[[int, int, int, int, int, int], Any]]):
            A callback function that accepts six integers representing
            completed_bytes, failed_bytes, total_bytes, completed_count,
            failed_count, and total_count respectively. If provided,
            this function will be called to report progress.
            If set to None, progress updates will not be reported.
        update_rate (float): The maximum update rate for the callback function,
            in seconds. Progress updates will be reported at most once per
            this duration. Ignored if callback_func is None.

    """  # noqa: D205

    def __init__(
        self,
        completed_bytes: int = 0,
        failed_bytes: int = 0,
        total_bytes: int = 0,
        completed_count: int = 0,
        failed_count: int = 0,
        total_count: int = 0,
        callback_func: Optional[  # pylint: disable=unsubscriptable-object
            Callable[[int, int, int, int, int, int], Any]
        ] = None,
        update_rate=NGC_CLI_PROGRESS_UPDATE_FREQUENCY,
    ):
        self.lock = asyncio.Lock()
        self.completed_bytes = completed_bytes
        self.failed_bytes = failed_bytes
        self.total_bytes = total_bytes
        self.completed_count = completed_count
        self.failed_count = failed_count
        self.total_count = total_count
        self.callback_func = callback_func

        self.update_rate = update_rate if callback_func else -1
        self.next_update = time.time() + update_rate if callback_func else -1

    async def debounced_update_progress(self):
        """Call the update progress callback function if the specified update rate interval has passed.

        'callback_func' is a user provided function with limited capability during lots of concurrent updates.
        Be sure to call update_progress at the end to finalize progress update.
        """
        now = time.time()  # tiny bit less expensive than lock check, thus do it first
        if self.callback_func and now > self.next_update and (not self.lock.locked()):
            async with self.lock:
                self.next_update = now + self.update_rate
                self.update_progress()

    def update_progress(self):
        """Call the update progress callback function with the current progress metrics."""
        if self.callback_func:
            self.callback_func(
                self.completed_bytes,
                self.failed_bytes,
                self.total_bytes,
                self.completed_count,
                self.failed_count,
                self.total_count,
            )

    async def advance(self, size_in_bytes: int, count: int):
        """Advance the progress by adding completed bytes and item count.

        use negatives to undo
        """
        async with self.lock:
            self.completed_bytes += size_in_bytes
            self.completed_count += count
        await self.debounced_update_progress()

    async def fail(self, size_in_bytes: int, count: int):
        """Update the progress by adding failed bytes and item count.

        use negatives to undo
        """
        async with self.lock:
            self.failed_bytes += size_in_bytes
            self.failed_count += count
        await self.debounced_update_progress()

    def read_progress(self):
        """Read the current progress metrics."""
        return (
            self.completed_bytes,
            self.failed_bytes,
            self.total_bytes,
            self.completed_count,
            self.failed_count,
            self.total_count,
        )


class BaseFileNode:  # noqa: D101
    def __init__(
        self,
        file_path: str = "",
        size: int = -1,
        ftime: float = -1.0,
        bitmask: int = -1,
    ):
        """This base file node object tracks the state of a file during transfer.

        FileNode-level asynchronous access should be handled in child classes.
        Read operations typically do not require locking, while write operations usually do.
        Users can implement their own logic for bitmask manipulation if needed.

        Args:
            file_path (str): The path to the file being tracked.
            size (int): The size of the file in bytes.
            ftime (float): A time of the file (Unix timestamp) to record for syncing.
            bitmask (int): The progress bitmask, default intepretation:
                           - 1 represents incomplete status,
                           - 0 represents complete status,
                           - A bitmask value of 0 indicates that all partitions are completed.
        """  # noqa: D401, D404
        self.lock = asyncio.Lock()

        # file metadata
        self.file_path = file_path
        self.size = size
        self.ftime = ftime

        # progress states
        self.bitmask = bitmask

        # temporay states
        # write_change is for AOF persistence
        # are there changes since load | should we persist this node
        self.write_change = False
        # has this file node caused a failure already
        self.failed = False

    @abstractmethod
    def serialize(self) -> str:
        """Serialize the instance state to a string for persistence. concrete method should choose what to persist."""

    @abstractmethod
    def is_match(self, file_path) -> bool:
        """Set condition for the instance matches the system file to ensure it is the same file."""

    @abstractmethod
    def is_sync(self, file_path) -> bool:
        """Set condition for the instance matches the system file and it is synced(same file and done)."""

    @classmethod
    def load(cls, state: str):
        """Load the state of the file node from a JSON string.

        This method loads the state of the file node from a JSON string.
        """
        data = json.loads(state)
        ins = cls()
        for key, val in data.items():
            setattr(ins, key, val)
        return ins

    def save(self) -> str:
        """Save the current state of the file node as a JSON string.

        This method saves the current state of the file node as a JSON string.
        """
        if self.write_change:
            return self.serialize()
        return ""

    def is_partition_complete(self, partition_id: int) -> bool:
        """Check if a partition is completed."""
        return not bitmask_is_bit_set(self.bitmask, partition_id)

    def get_completed_size(self) -> int:
        """Provide the sum of completed partition sizes in bytes."""
        return self.size - bitmask_set_bit_in_size(self.bitmask, self.size, PARTITION_SIZE)

    async def set_partition_complete(self, partition_id: int):
        """Mark one partition complete."""
        async with self.lock:
            self.bitmask = bitmask_clear_bit(self.bitmask, partition_id)
            self.write_change = True


class UploadFileNode(BaseFileNode):  # noqa: D101
    def __init__(
        self,
        file_path: str = "",
        size: int = -1,
        ftime: float = -1.0,
        bitmask: int = -1,
        upload_id="",
        hash="",
        race_flag=False,
        complete=False,
    ):
        """Initialize the upload file node with additional attributes for upload management.

        This class extends BaseFileNode to include attributes specific to upload management.

        Attributes:
            upload_id (str): Identifier set after initiating a multipart upload.
            hash (str): Hash computed by the worker for the file.
            race_flag (bool): Flag necessary to prevent racing condition when multiple producers
                              send the same workload to the consumer. Only one should succeed.
            complete (bool): Marked complete state unique to multipart upload.
        """
        super().__init__(file_path=file_path, size=size, ftime=ftime, bitmask=bitmask)
        self.upload_id = upload_id
        self.hash = hash
        self.race_flag = race_flag
        self.complete = complete

    def serialize(self):
        """Convert the upload file node state to a string.

        This method converts the upload filenode states to a JSON string representation.
        Unnecessary fields are removed to conserve space in serialization.
        """
        include_fields = ["size", "ftime", "bitmask", "upload_id", "hash", "complete"]
        state = {field: getattr(self, field) for field in include_fields}
        return json.dumps(state)

    def is_match(self, file_path) -> bool:
        """Check if the instance matches the system file to ensure it is the same file."""
        # this is the same aws upload sync strategy
        # https://github.com/aws/aws-cli/blob/master/awscli/customizations/s3/syncstrategy/base.py#L226
        return self.size == os.path.getsize(file_path) and self.ftime == os.path.getmtime(file_path)

    def is_sync(self, file_path) -> bool:
        """Check if the instance matches the system file and synced with remote."""
        return self.is_match(file_path) and self.complete

    async def set_file_hash(self, hash):
        """Set the hash for the file."""
        async with self.lock:
            self.hash = hash
            self.write_change = True

    async def set_complete(self):
        """Mark the file as complete."""
        async with self.lock:
            self.complete = True
            self.write_change = True

    async def set_race_flag_once(self):
        """Determine whether the file should be send to mark completion.

        This method determines whether the file should be send to the consumer
        for further processing. It requires a lock since multiple producers may
        concurrently attempt to send the same workload to the consumer, and the
        consumer take time to perform mark completion.

        Returns:
            bool: True if the file is not yet send to the consumer and additional action is needed,
            False if the file is already or will be send to the consumer no additional action is needed.
        """
        async with self.lock:
            should_mark_complete = (
                (self.bitmask == 0)  # All partitions uploaded
                and self.hash  # Hashing completed
                and (not self.complete)  # Not already marked as complete
                and (not self.race_flag)  # No other worker marking completion
            )
            if should_mark_complete:
                # Block further attempts to mark as complete
                self.race_flag = True
            return should_mark_complete

    async def set_failed_once(self) -> bool:
        """Determine whether the file should be marked as failed.

        This method determines whether the file should be marked as failed and
        further processing. It requires a lock since multiple consumers may concurrently
        attempt to fail the same file, but only one consumer should mark it as failed.

        Returns:
            bool: True if the file is marked as failed and additional action is needed,
            False if the file is already marked as failed and no additional action is needed.
        """
        async with self.lock:
            if self.failed:
                # If already marked as failed, no additional action needed
                return False
            # Mark the file as failed and perform additional action
            self.failed = True
            return True


class DownloadFileNode(BaseFileNode):
    """Placeholder class for extending type hinting and code structure.

    This class serves as a placeholder for extending type hinting and code structure.
    It will be further developed in the future.
    """

    def __init__(self):
        """Initialize the download file node."""
        raise NotImplementedError()

    def serialize(self):
        """Convert the download file node state to a string."""
        raise NotImplementedError()

    def is_match(self, file_path) -> bool:
        """Check if the instance matches the system file to ensure it is the same file."""
        raise NotImplementedError()

    def is_sync(self, file_path) -> bool:  # noqa: D102
        raise NotImplementedError()
