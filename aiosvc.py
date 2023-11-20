import asyncio as aio
from typing import Callable, Awaitable

__all__ = ['Service', 'Runnable']

class _ErrorRaisingLock(aio.Lock):
    def __init__(self):
        super().__init__()
        self._meta_lock = aio.Lock()

    async def __aenter__(self):
        async with self._meta_lock:
            if self.locked():
                raise RuntimeError("Lock is already acquired")
            
            return await super().__aenter__()

class Service:
    def __init__(self, on_start: Callable[[], Awaitable] = None, on_stop: Callable[[], Awaitable] = None):
        if on_start is not None:
            self.on_start = on_start
        
        if on_stop is not None:
            self.on_stop = on_stop
        
        self._lock = _ErrorRaisingLock()
        self._started = False
        self._done = False

    async def start(self):
        async with self._lock:
            if self._done:
                raise RuntimeError("Service has already stopped")

            if self._started:
                raise RuntimeError("Service has already started")

            await self.on_start()

            self._started = True
    
    async def stop(self):
        async with self._lock:
            if not self._started:
                raise RuntimeError("Service has not yet started")

            if self._done:
                raise RuntimeError("Service has already stopped")

            try:
                await self.on_stop()
            finally:
                self._done = True
    
    async def on_start(self): ...
    
    async def on_stop(self): ...

class Runnable(Service):
    def __init__(self, run: Callable[[aio.Event, aio.Event], Awaitable] = None):
        super().__init__()

        if run is not None:
            self.run = run
        
        self._event_on_ready = aio.Event()
        self._event_on_stop = aio.Event()

        self._task: aio.Task = None
        
    async def on_start(self):
        self._task = aio.create_task(self.run(self._event_on_ready, self._event_on_stop))

        either = [
            self._task,
            self._event_on_ready.wait()
        ]

        await aio.wait(either, return_when=aio.FIRST_COMPLETED)
    
    async def on_stop(self):
        self._event_on_stop.set()
        await self._task
    
    async def run(self, on_ready: aio.Event, on_stop: aio.Event): ...

