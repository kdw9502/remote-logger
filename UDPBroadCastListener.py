import asyncio
import socket

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
            print(data)
            if data == UDPBroadCaster.PASSWORD:
                print(f"server IP is: {addr} ")

            await asyncio.sleep(0.5)
