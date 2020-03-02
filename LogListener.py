import asyncio
import json
from enum import Enum

PORT_NUM = 30270


class LogType(Enum):
    DEBUG = 0,
    Warning = 1,
    Error = 2


class Log:
    def __init__(self, message: str, log_type: LogType = LogType.DEBUG, timestamp=0):
        self.message = message
        self.log_type = log_type
        self.timestamp = timestamp

    @classmethod
    def crate_from_raw_bytes_json(cls, data):
        full_message = data.decode()
        json_data = json.loads(full_message)

        return cls(json_data['message'], json_data['type'], json_data['timestamp'])


class LogListener:
    def __init__(self):
        self.logs = []
        self.callback = None

    @classmethod
    def create_with_new_log_callback(cls, callback):
        instance = cls()
        instance.callback = callback
        return instance

    async def listen(self):
        server = await asyncio.start_server(self._callback, '127.0.0.1', PORT_NUM)
        my_ip = server.sockets[0].getsockname()
        print(f'server started on ip {my_ip}')

        async with server:
            await server.serve_forever()

    async def _callback(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        await self.add_log(reader, writer)
        if callable(self.callback):
            self.callback()

    async def add_log(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        print(f"client ip : {writer.get_extra_info('peername')}")
        data = await reader.read(1024)
        log = Log.crate_from_raw_bytes_json(data)
        self.logs.append(log)

    def clear(self):
        self.logs.clear()