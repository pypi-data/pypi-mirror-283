from typing import Union
from socket import socket
import json, time

class PubSubClient:
    def __init__(
            self,
            serverAddress: str,
            serverPort: int,
            id: str,
            bufferSize: int = 1024
        ):
        self.__address: str = serverAddress
        self.__port: int = serverPort
        self.__id: str = id
        self.__bufferSize: int = bufferSize

    def __del__(self):
        self.__socket.close()

    def connect(self, socketClient: socket):
        self.__socket: socket = socketClient
        self.__socket.connect((self.__address, self.__port))
        print(f"Connect: {self.__address}:{self.__port}")
        self.__socket.send(
            json.dumps({"id": self.__id}).encode()
        )
        time.sleep(0.1)

    def publish(self, channel: str, payload: Union[str, dict]):
        self.__socket.send(
            json.dumps({
                "mode": "Publish",
                "channel": channel,
                "payload": payload
            }).encode()
        )
        print(f"Publish: {payload}")
        time.sleep(0.1)

    def subscribe(self, channel: str) -> bytes:
        self.__socket.send(
            json.dumps({
                "mode": "Subscribe",
                "channel": channel
            }).encode()
        )
        data: bytes = self.__socket.recv(self.__bufferSize)
        print(f"Subscribe: {data}")
        return data
