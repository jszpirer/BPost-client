
def printTopMenu():
    print("1 -- Create an account")
    print("2 -- Login")


def printActionMenu(connection):
    print("What do you want to do?")
    print("1 -- Send a message")
    print("2 -- Add a contact to my list")
    print("3 -- Change password")
    print("4 -- Read new messages (" + str(len(connection.private_messages)) + " unread conversations)")
    print("5 -- Exit and close program")








