from dataclasses import dataclass as _dataclass
import asyncio as _asyncio
from typing import Hashable as _Hashable

@_dataclass
class _LockData:
    lock: _asyncio.Lock
    holders_amount: int

class Storage:
    def __init__(self) -> None:
        self._contents = {}

class Lock:
    def __init__(self, storage: Storage, key: _Hashable) -> None:
        self._storage = storage
        self._key = key
    async def acquire(self):
        lock_data = self._storage._contents.setdefault(
            self._key,
            _LockData(lock=_asyncio.Lock(), holders_amount=0),
        )
        lock_data.holders_amount += 1
        await lock_data.lock.acquire()
    async def release(self):
        lock_data = self._storage._contents[self._key]
        await lock_data.lock.release()
        lock_data.holders_amount -= 1
        if lock_data.holders_amount == 0:
            del self._storage._contents[self._key]
    async def __aenter__(self, *args, **kwargs):
        _ = args, kwargs
        await self.acquire()
    async def __aexit__(self, *args, **kwargs):
        _ = args, kwargs
        await self.release()
