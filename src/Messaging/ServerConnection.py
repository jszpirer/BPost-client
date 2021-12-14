import websockets


class ServerConnection:
    clientWebsocket = None

    def __init__(self, serverUrl):
        async with websockets.connect(serverUrl) as self.clientWebsocket:
            print("Connection established")
            while True:
                message = yield from self.clientWebsocket.recv()
                if message is None:
                    # La connection est fermée.
                    break
                yield from self.receiveMessage(message)

    def sendMessage(self, message):
        print(message)

    def receiveMessage(self, message):
        print(message)
