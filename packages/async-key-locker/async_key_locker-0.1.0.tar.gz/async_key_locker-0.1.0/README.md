# What is this

This library is like an `asyncio.Lock()`, but this library's `Lock` can be activated with various keys, and the locking is distinct for each key

# Installation

`pip install key_locker`

# Usage

```
from key_locker import Storage, Lock

storage = Storage()

lock = Lock(storage, "key")

await lock.acquire()
await lock.release()
async with lock:
    pass
```
