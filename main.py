import asyncio

from RemoteDebuggerApp import RemoteDebuggerApp


def main():
    asyncio.run(RemoteDebuggerApp().run())


if __name__ == '__main__':
    main()
