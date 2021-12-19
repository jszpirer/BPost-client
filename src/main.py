import asyncio
from Messaging.ServerConnection import ServerConnection
from Menus.printMenus import *
from Menus.reactMenus import *


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6666
separator = "<SEP>"


async def main():
    serverconn = ServerConnection("localhost")
    await serverconn.receiveMessage()

    print("Welcome in BPost-Client")
    printTopMenu()  # choice between creating an account or log in
    while True :
        try:
            optionTop = int(input("Enter your choice : "))
            break
        except:
            print("Wrong input. Please enter a number")
    reactTopMenu(optionTop, serverconn)


if __name__ == '__main__':
    asyncio.run(main())
