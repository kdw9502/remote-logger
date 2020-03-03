import asyncio
import socket
import time
from asyncio import StreamWriter, StreamReader

import LogListener
import UDPBroadCaster


class UDPBroadCastListener:
    def __init__(self):
        self.socket = self._make_udp_socket()

    @staticmethod
    def _make_udp_socket():
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.bind(('', UDPBroadCaster.PORT_NUM))
        return udp_socket

    async def listen(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            if data == UDPBroadCaster.PASSWORD:
                print(f"server IP is: {addr} ")
                sender = await LogSender.create_with_ip(addr[0])
                await sender.send_log()

            await asyncio.sleep(0.5)


class LogSender:
    def __init__(self):
        self.reader: StreamReader = None
        self.writer: StreamWriter = None

    @classmethod
    async def create_with_ip(cls, ip: str):
        instance = cls()
        instance.ip = ip

        instance.reader, instance.writer = await asyncio.open_connection(ip, LogListener.PORT_NUM)

        return instance

    async def send_log(self):
        self.writer.write(
            LogListener.Log(f"{time.time()} example", LogListener.LogType.DEBUG, time.time()).to_json().encode())
        await self.writer.drain()
