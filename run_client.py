import asyncio

from ClientExample import UDPBroadCastListener


def run_client():
    asyncio.run(tester_run())


async def tester_run():
    await UDPBroadCastListener().listen()


if __name__ == '__main__':
    run_client()
