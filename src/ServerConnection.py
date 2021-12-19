import websockets
import asyncio
import ssl


class ServerConnection:

    def __init__(self, server_url, server_port):
        self.uri = f"wss://{server_url}:{server_port}"
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.messages_to_read = list()
        self.messages_to_send = list()
        self.keep_turning = True

    async def start(self):
        await self.connect()

    async def sender_handler(self, ws):
        while self.keep_turning:
            for m in self.messages_to_send:
                await ws.send(m)
                self.messages_to_send.remove(m)
                print("Sent message :", m)
            await asyncio.sleep(0.01)

    async def receiver_handler(self, ws):
        async for msg in ws:
            self.messages_to_read.append(msg)
            print(msg)
            # Todo : await manage message

    async def connect(self):
        async with websockets.connect(self.uri, ssl=self.ssl_context) as ws:
            await ws.send("Je suis un client qui me connecte")
            await asyncio.gather(
                self.sender_handler(ws),
                self.receiver_handler(ws),
            )

    def send_message(self, message: str):
        self.messages_to_send.append(message)
