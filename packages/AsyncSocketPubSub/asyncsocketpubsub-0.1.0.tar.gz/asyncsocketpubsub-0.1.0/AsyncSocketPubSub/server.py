from typing import Union
import pubsub, time, asyncio, json
from threading import Thread

BUFFER_SIZE = 1024

class UndefinedException(Exception): pass

class PubSubClients:
    def __init__(self, id: str):
        self.__id: str = id

    def publish(self, channel: str = None, payload: Union[str, dict] = None):
        if (channel, payload) == (None, None):
            self.__publish()
        else:
            pubsub.publish(
                channel = channel,
                data = payload
            )
            time.sleep(0.1)

    def __publish(self):
        try:
            pubsub.publish(
                channel = self.__channel,
                data = self.__payload
            )
            time.sleep(0.1)
        except:
            raise UndefinedException(
                "Undefined channel or payload or eather. \nhint: setChannel(), setPayload()"
            )

    def subscribe(self, channel: str = None):
        if channel == None:
            return self.__subscribe()
        else:
            queue = pubsub.subscribe(channel)
            return next(queue.listen())["data"]

    def __subscribe(self):
        try:
            queue = pubsub.subscribe(self.__channel)
            return next(queue.listen())["data"]
        except:
            raise UndefinedException(
                "Undefined channel. \nhint: setChannel()"
            )

    def getId(self) -> str:
        return self.__id

    def setChannel(self, channel: str):
        self.__channel: str = channel

    def setPayload(self, payload: Union[str, dict]):
        self.__payload: Union[str, dict] = payload


def PublisherThread(publisher: PubSubClients):
    print(f"{publisher.getId()}: publishing")
    publisher.publish()

def SubscriberThread(subscriber: PubSubClients, writer: asyncio.StreamWriter):
    print(f"{subscriber.getId()}: subscribing")
    data = subscriber.subscribe()
    if type(data) == str:
        data = data.encode()
    elif type(data) == dict:
        data = json.dumps(data).encode()
    writer.write(data)

async def clientHandler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        addr = writer.get_extra_info('peername')
        print(f"{addr} connected")

        # need {"id": "client ID"}
        while True:
            idData: bytes = await reader.read(BUFFER_SIZE)
            if not idData:
                raise Exception("disconnected")
            try:
                clientId = json.loads(idData)["id"]
                print(f"{addr}: {clientId}")
                psClient: PubSubClients = PubSubClients(id = clientId)
                break
            except:
                pass
        del idData
        del clientId

        # need {"mode": "Publish", "channel": "Channel name", "payload": payload}
        while True:
            processData: bytes = await reader.read(BUFFER_SIZE)
            if not processData:
                del psClient
                break
            try:
                process = json.loads(processData)
                print(f"{addr}: {process}")

                mode: str = process["mode"]
                channel: str = process["channel"]

                if mode == "Publish":
                    payload = process["payload"]
                    psClient.setChannel(channel)
                    psClient.setPayload(payload)
                    PT = Thread(
                        target = PublisherThread,
                        args = (psClient,),
                        daemon = True
                    )
                    PT.start()

                elif mode == "Subscribe":
                    psClient.setChannel(channel)
                    ST = Thread(
                        target = SubscriberThread,
                        args = (psClient, writer),
                        daemon = True
                    )
                    ST.start()
            except:
                pass
            time.sleep(0.1)
    finally:
        writer.close()
        print(f"{addr} disconnected")

async def main(host: str, port: int):
    server = await asyncio.start_server(
        client_connected_cb = clientHandler,
        host = host,
        port = port
    )
    print(f"Server: {server.sockets[0].getsockname()}")

    async with server:
        await server.serve_forever()

def runServer(host: str, port: int, bufferSize: int = None):
    if not bufferSize == None:
        global BUFFER_SIZE
        BUFFER_SIZE = bufferSize
    try:
        asyncio.run(main(host = host, port = port))
    finally:
        print("Server: exitting")
        exit(0)
