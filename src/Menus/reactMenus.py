from src.Account.account import *
from src.Messaging.message import *
from src.Menus.printMenus import *

sep = "<SEP>"


def reactTopMenu(option, connection):
    if option == 1:  # create account
        createAccount(connection)
    elif option == 2:  # login
        acc = login(connection)
    else:
        print("Invalid option. Please enter a number between 1 and 2")
    printActionMenu()
    while True:
        try:
            action = int(input("Enter your choice : "))
            break
        except:
            print("Wrong input. Please enter a number")
    reactActionMenu(action, acc, connection)


def reactActionMenu(option, acc, connection):
    if option == 1:  # send a message
        toServ = sendMessage(acc, connection)
    elif option == 2:  # add a contact to the contact list
        addContact(acc, connection)
    else:
        print("Invalid option. Please enter a number between 1 and 2")
    return toServ


def sendMessage(acc, connection):
    print("Here is your contact list : ", acc.contacts)
    recipient = input("Send to : ")
    content = input("Write here : ")
    mess = Message(acc.getUsername(), recipient, content)
    toServ = [0, acc.getUsername(), mess, recipient]
    if authenticate(toServ, connection):
        mess = Message(acc.getUsername(), recipient, content)
    else:
        print("This person does not exist in our database. Please try again.")
        # TODO : try again
    return mess


def createAccount(connection):
    print("You don't have an account yet. Please enter a username and then enter a password")
    username = input("Username : ")
    password = input("Your password : ") # Todo : demander une deuxieme fois le mdp ?
    password = hash(password)
    toServ = [1, sername, password]
    if authenticate(toServ, connection):
        print("You have successfully created you BPost Account !")
        login(connection)
    else:
        print("This username already exists. Please choose a different username")
        # TODO : try again


def login(connection):
    print("Welcome back to the BPost Messaging App !")
    print("Please enter your username and then enter your password")
    username = input("Username : ")
    password = input("Your password : ")
    password = hash(password)
    toServ = [2, username, password]  # info to send to the server !! formatage
    if authenticate(toServ, connection):
        print("Login successful")
        acc = Account(username, password)
    else:
        print("Your username or password is incorrect. Please try again")
        # TODO : try again
    return acc


def addContact(acc, connection):
    contact = input("What is the username of the contact you would like to add to your list : ")
    toServ = [4, acc.getUsername(), contact]
    if authenticate(toServ, connection):  # contact exists?
        acc.newContact(contact)
        print("Contact successfully added to your list")
    else:
        print("This person does not exist in our database. Please try again.")
        # TODO : try again


def authenticate(action, toServer, connection):
    # format with the action !

    connection.send_message(toServer)
    state = connection.receive_message()
    if state:
        return True
    else:
        return False


def inverse_format(from_server):
    """Recognizes action from the server and says whether it should execute"""
    input = from_server.split(sep)
    action = input[0]
    bool = input[1]
    if bool:
        if action == 0:
            return "message was sent"
        elif action == 1:
            return "user logged in"
        elif action == 2:
            return "account created"
        elif action == 3:
            return "password changed"
        elif action == 4:
            return "contact added"
        elif action == 5:
            """server is sending a message to a client"""
            mess = input[1]
            recip = input[2]
            return mess+"<SEP>"+recip
        else:
            print("action was not an int between 0 and 4")
        return
    else:
        print("error action "+str(action))


def format_send_message(to_server):  #send
    sender = to_server[0]
    message = to_server[1]
    recipient = to_server[2]
    return str(0)+sep+sender+sep+message+sep+recipient


def format_login_request(to_server):  #auth
    username = to_server[0]
    password = to_server[1]
    return str(1)+sep+username+sep+password


def format_new_account(to_server):  #new acc
    username = to_server[0]
    password = to_server[1]
    return str(2) +sep+ username +sep+ password


def format_change_password(to_server):  #change pwd
    username = to_server[0]
    curr_password = to_server[1]
    new_password = to_server[2]
    return str(3) +sep+ username +sep+ curr_password +sep+ new_password


def format_add_contact(to_server):  #new contact
    username = to_server[0]
    contact = to_server[1]
    return str(4) +sep+ username +sep+ contact