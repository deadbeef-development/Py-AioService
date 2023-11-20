To install, run `python3 -m pip install "git+https://github.com/deadbeef-development/Py-AioService.git@v0"`.

You can also add the following to your requirements file:
`git+https://github.com/deadbeef-development/Py-AioService.git@v0`

Example usage of `aiosvc.Service`:
```python
import asyncio as aio
import aiosvc

async def my_service_start():
    print("Preparing...")
    await aio.sleep(1)
    print("Ready")

async def my_service_stop():
    print("Shutting down...")
    await aio.sleep(1)
    print("Done.")
    return

async def main():
    svc1 = aiosvc.Service(my_service_start, my_service_stop)

    await svc1.start()
    await aio.sleep(3)
    await svc1.stop()

if __name__ == '__main__':
    aio.run(main())
```

Example usage of `aiosvc.Runnable`:
```python
import asyncio as aio
import aiosvc

async def my_service(on_ready, on_stop):
    print("Preparing...")
    await aio.sleep(1)
    on_ready.set()
    print("Ready")

    await on_stop.wait()
    print("Shutting down...")
    await aio.sleep(1)
    print("Done.")

    return

async def main():
    svc1 = aiosvc.Runnable(my_service)

    await svc1.start()
    await aio.sleep(3)
    await svc1.stop()

if __name__ == '__main__':
    aio.run(main())
```

