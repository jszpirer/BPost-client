import websockets
import asyncio
import ssl
import src.format as format


class ServerConnection:

    def __init__(self, server_url, server_port):
        self.uri = f"wss://{server_url}:{server_port}"
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.private_messages = list()  # list of pairs (sender_username: str, message: str)
        self.server_responses = list()  # list of pairs (action_type: int, result: bool)
        self.messages_to_send = list()
        self.keep_turning = True

    async def start(self):
        print("Starting server")
        await self.connect()

    async def connect(self):
        async with websockets.connect(self.uri, ssl=self.ssl_context) as ws:
            await asyncio.gather(
                self.sender_handler(ws),
                self.receiver_handler(ws),
            )

    async def sender_handler(self, ws):
        while self.keep_turning:
            for m in self.messages_to_send:
                await ws.send(m)
                self.messages_to_send.remove(m)
                print("Sent message :", m)
            await asyncio.sleep(0.01)

    async def receiver_handler(self, ws):
        async for order in ws:
            if format.order_is_confirmation(order):
                print("Ajouté dans les réponses serveur")
                self.server_responses.append(format.inverse_format(order))
            else:
                print("Ajouté message privé reçu")
                self.private_messages.append(format.inverse_format(order))

            print(order)

    def send_message(self, message: str):
        print("Added message to send")
        self.messages_to_send.append(message)
