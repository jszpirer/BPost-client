import websockets


class ServerConnection:
    clientWebsocket = None

    def __init__(self, serverUrl):
        uri = f"ws://{serverUrl}:8000"
        self.clientWebsocket = websockets.connect(uri)
        print("Connection established")

    def sendMessage(self, message):
        print(message)

    async def receiveMessage(self):
        while True:
            async with self.clientWebsocket as websocket:
                message = await websocket.recv()
            if message is None:
                break
            print(message)

    def manageMessage(self):
        # TODO
        print("envoyer")