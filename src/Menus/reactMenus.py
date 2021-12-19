from src.Account.account import *
from src.Messaging.message import *
from printMenus import *


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


def createAccount(connection):
    print("You don't have an account yet. Please enter a username and then enter a password")
    username = input("Username : ")
    password = input("Your password : ")
    password = hash(password)
    toServ = [username, password]  # info to send to the server
    if authenticate("newAccount", toServ, connection):
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
    toServ = [username, password]  # info to send to the server !! formatage
    if authenticate("login", toServ, connection):
        print("Login successful")
        acc = Account(username, password)
    else:
        print("Your username or password is incorrect. Please try again")
        # TODO : try again
    return acc


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
    toServ = recipient
    if authenticate("sendMessage", toServ, connection):
        mess = Message(acc.getUsername(), recipient, content)
    else:
        print("This person does not exist in our database. Please try again.")
        # TODO : try again
    return mess


def addContact(acc, connection):
    contact = input("What is the username of the contact you would like to add to your list : ")
    toServ = contact
    if authenticate("add Contact to list", toServ, connection):  # contact exists?
        acc.newContact(contact)
        print("Contact successfully added to your list")
    else:
        print("This person does not exist in our database. Please try again.")
        # TODO : try again


def authenticate(action, toServer, connection):
    # format with the action !
    connection.sendMessage(toServer)
    state = connection.receiveMessage()
    if state:
        return True
    else:
        return False

