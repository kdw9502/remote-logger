import asyncio
import threading

from RemoteDebuggerApp import RemoteDebuggerApp
from UDPBroadCastListener import UDPBroadCastListener as Listener


def main():
    app_thread = threading.Thread(target=lambda: asyncio.run(app_run()))
    app_thread.start()
    asyncio.run(tester_run())

    app_thread.join()


async def app_run():
    await RemoteDebuggerApp().run()


async def tester_run():
    await Listener().listen()


if __name__ == '__main__':
    main()
