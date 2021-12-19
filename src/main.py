import asyncio
from Messaging.ServerConnection import ServerConnection

SERVER_HOST = "localhost"
SERVER_PORT = 8000
separator = "<SEP>"


async def main():
    serverconn = ServerConnection("localhost")
    await serverconn.receiveMessage()
    print("Welcome in BPost-Client")


if __name__ == '__main__':
    asyncio.run(main())
