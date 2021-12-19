import asyncio
from Menus.printMenus import *
from Menus.reactMenus import *

from ServerConnection import ServerConnection

SERVER_HOST = "localhost"
SERVER_PORT = 8000
separator = "<SEP>"


async def start_menu(server_conn):
    print("Starting menu")
    # Todo
    server_conn.send_message("Test message")
    printTopMenu()  # choice between creating an account or log in
    while True:
        try:
            optionTop = int(input("Enter your choice : "))
            break
        except:
            print("Wrong input. Please enter a number")
    reactTopMenu(optionTop, server_conn)


async def main():
    print("Welcome in BPost-Client")
    server_conn = ServerConnection(SERVER_HOST, SERVER_PORT)
    await asyncio.gather(
        server_conn.start(),
        start_menu(server_conn),
    )


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
