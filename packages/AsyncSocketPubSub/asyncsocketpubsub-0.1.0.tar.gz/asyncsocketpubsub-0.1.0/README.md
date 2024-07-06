# AsyncSocketPubSub

This module provides Pub/Sub based communication using socket communication.

## Requirement

This module requires the [`pubsub`](https://github.com/nehz/pubsub) module:

```shell
pip install pubsub
```

## Usage

directory structure:

```shell
┋
┣ AsyncSocketPubSub
┣ xxx.py
┋
```

see [examples](https://github.com/amenaruya/AsyncSocketPubSub/tree/main/example)

### Simple using

Use `threading` for publisher and subscriber when using `pubsub` module.

```python
from AsyncSocketPubSub.server import PubSubClients
from threading import Thread
import time

# similar to topic in MQTT
CHANNEL = "C"

def Subscriber():
    subClient = PubSubClients(id = "subscriber")
    while True:
        data = subClient.subscribe(channel = CHANNEL)
        print(data)

def Publisher():
    pubClient = PubSubClients(id = "publisher")
    while True:
        pubClient.publish(
            channel = CHANNEL,
            payload = "hello"
        )
        time.sleep(3)

# thread
sub = Thread(
    target = Subscriber,
    daemon = True
)
sub.start()

Publisher()

```

### Server and Client

`pubsub` module can send/receive the dict objects. This module also can do that as well.  

Socket server:

```python
from AsyncSocketPubSub import runServer

runServer(
    host = "0.0.0.0",    # host IP address
    port = 18883         # port number
)

```

Socket client as publisher:

```python
from socket import socket
from AsyncSocketPubSub.client import PubSubClient

ADDRESS = "127.0.0.1"   # server IP address
PORT = 18883            # server port
ID = "Publisher"        # client ID
CHANNEL = "C"           # channel

# DATA = "hello" # str type
DATA = {"int": 1, "str": "hello", "float": 1.3, "list": ["a", 2]} # dict type

psClient = PubSubClient(
    serverAddress = ADDRESS,
    serverPort = PORT,
    id = ID
)

# connect to server
psClient.connect(socketClient = socket())

# publish
psClient.publish(
    channel = CHANNEL,
    payload = DATA
)

```

Socket client as subscriber:

```python
from socket import socket
from AsyncSocketPubSub.client import PubSubClient

ADDRESS = "127.0.0.1"   # server IP address
PORT = 18883            # server port
ID = "Subscriber"       # client ID
CHANNEL = "C"           # channel

psClient = PubSubClient(
    serverAddress = ADDRESS,
    serverPort = PORT,
    id = ID
)

# connect to server
psClient.connect(socketClient = socket())

# subscriber
psClient.subscribe(CHANNEL)

```
