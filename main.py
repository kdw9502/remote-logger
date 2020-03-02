import asyncio

from RemoteDebuggerApp import RemoteDebuggerApp
from UDPBroadCastListener import UDPBroadCastListener as Listener


def main():
    asyncio.run(app_run())
    # asyncio.run(tester_run())


async def app_run():
    await RemoteDebuggerApp().run()


async def tester_run():
    await Listener().listen()


if __name__ == '__main__':
    main()
