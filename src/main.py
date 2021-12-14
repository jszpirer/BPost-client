import asyncio
from Messaging.ServerConnection import ServerConnection

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6666
separator = "<SEP>"


async def main():
    serverconn = ServerConnection("localhost")
    await serverconn.receiveMessage()
    print("Welcome in BPost-Client")


if __name__ == '__main__':
    asyncio.run(main())
