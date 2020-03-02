import asyncio
import json
from enum import IntEnum

PORT_NUM = 30270


class LogType(IntEnum):
    DEBUG = 0,
    WARNING = 1,
    ERROR = 2


class Log:
    def __init__(self, message: str, log_type: LogType = LogType.DEBUG, timestamp=0):
        self.message = message
        self.log_type = log_type
        self.timestamp = timestamp

    @classmethod
    def create_from_raw_bytes_json(cls, data):
        full_message = data.decode()
        json_data = json.loads(full_message)

        return cls(json_data['message'], LogType(json_data['type']), json_data['timestamp'])

    def to_json(self):
        return json.dumps({"message": self.message, "type": int(self.log_type), "timestamp": self.timestamp})


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
        server = await asyncio.start_server(self._callback, None, PORT_NUM)
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
        log = Log.create_from_raw_bytes_json(data)
        self.logs.append(log)

    def clear(self):
        self.logs.clear()
