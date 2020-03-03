import asyncio

from RemoteDebuggerApp import RemoteDebuggerApp


def run_server():
    asyncio.run(app_run())


async def app_run():
    await RemoteDebuggerApp().run()


if __name__ == '__main__':
    run_server()
