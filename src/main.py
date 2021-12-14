from src.Messaging.ServerConnection import ServerConnection

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6666
separator = "<SEP>"

def main():
    serverconn = ServerConnection("localhost")
    print("Welcome in BPost-Client")

if __name__ == '__main__' :
    main()