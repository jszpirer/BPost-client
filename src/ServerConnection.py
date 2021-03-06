import websockets
import asyncio
import ssl
import format as format


class ServerConnection:

    def __init__(self, server_url, server_port):
        self.uri = f"wss://{server_url}:{server_port}"
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.private_messages = dict()  # list of dict (sender_username: str, received_messages: list)
        self.server_responses = list()  # list of pairs (action_type: int, result: bool)
        self.messages_to_send = list()
        self.keep_turning = True

    async def start(self):
        """Starts the server"""
        print("Starting server")
        await self.connect()

    async def connect(self):
        """Connects to the server"""
        async with websockets.connect(self.uri, ssl=self.ssl_context) as ws:
            await asyncio.gather(
                self.sender_handler(ws),
                self.receiver_handler(ws),
            )

    async def sender_handler(self, ws):
        """Sends the elements of the list of elements to send to the server and then removes them from the list
        once they are sent"""
        while self.keep_turning:
            for m in self.messages_to_send:
                await ws.send(m)
                self.messages_to_send.remove(m)
            await asyncio.sleep(0.01)

    async def receiver_handler(self, ws):
        """Analyses the list of elements received from the server and separates it between the confirmation responses
        and the private messages"""
        async for order in ws:
            if format.order_is_confirmation(order):
                print("Added to responses")
                self.server_responses.append(format.inverse_format(order))
            else:
                print("Added to private message")
                sender, content = format.inverse_format(order)
                if sender in self.private_messages:
                    self.private_messages[sender].append(content)
                else:
                    self.private_messages[sender] = [content]

    def send_message(self, message: str):
        """Adds formatted messages (configuration and messages for clients) to the list of elements to send to the server"""
        self.messages_to_send.append(message)
