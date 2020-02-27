import asyncio
import socket

PORT_NUM = 39502
PASSWORD = b"remote-logger"


class UDPBroadCaster:
    def __init__(self):
        self.socket = self._make_udp_socket()

    @staticmethod
    def _make_udp_socket():
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(0.2)
        return udp_socket

    async def start_broadcast(self):
        message = PASSWORD
        while True:
            self.socket.sendto(message, ("<broadcast>", PORT_NUM))
            await asyncio.sleep(1)
