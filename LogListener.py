import asyncio
import json
from datetime import datetime
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
    def create_from_json(cls, data: str):
        json_data = json.loads(data)

        return cls(json_data['message'], LogType(json_data['type']), json_data['timestamp'])

    def to_json(self):
        return json.dumps({"message": self.message, "type": int(self.log_type), "timestamp": self.timestamp})

    def __str__(self):
        return json.dumps({"message": self.message, "type": self.log_type.name,
                           "timestamp": str(datetime.fromtimestamp(self.timestamp))}, indent=4, sort_keys=True)


class LogListener:
    def __init__(self):
        self.logs = []
        self.new_log_callback = None

    @classmethod
    def create_with_new_log_callback(cls, callback):
        instance = cls()
        instance.new_log_callback = callback
        return instance

    async def listen(self):
        server = await asyncio.start_server(self._on_server_get_message, None, PORT_NUM)
        my_ip = server.sockets[0].getsockname()
        print(f'server started on ip {my_ip}')

        async with server:
            await server.serve_forever()

    async def _on_server_get_message(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        await self.add_log(reader, writer)
        if callable(self.new_log_callback):
            self.new_log_callback()

    async def add_log(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(1024)
        print(f"client ip : {writer.get_extra_info('peername')} message:{data}")
        log = Log.create_from_json(data.decode())
        self.logs.append(log)

    def find_log_by_message(self, message: str):
        for log in self.logs:
            if log.message == message:
                return log

    def find_log_by_timestamp(self, timestamp: float):
        for log in self.logs:
            if log.timestamp == timestamp:
                return log

    def clear(self):
        self.logs.clear()
