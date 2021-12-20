from src.Account.account import *
from src.Messaging.message import *
from src.Menus.printMenus import *


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
    confPassword = input("Please confirm your password : ")
    if password == confPassword:
        password = hash(password)
    else:
        print("Passwords don't match")
        # TODO : passwords don't match
    toServ = [username, password]  # info to send to the server
    if authenticate("newAccount", toServ, connection):
        print("You have successfully created you BPost Account !")
        acc = login(connection)
        return acc
    else:
        print("This username already exists. Please choose a different username")
        return createAccount(connection)


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
        return acc
    else:
        print("Your username or password is incorrect. Please try again")
        return login(connection)



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
        return mess
    else:
        print("This person does not exist in our database. Please try again.")
        return sendMessage(acc, connection)



def addContact(acc, connection):
    contact = input("What is the username of the contact you would like to add to your list : ")
    toServ = contact
    if authenticate("add Contact to list", toServ, connection):  # contact exists?
        acc.newContact(contact)
        print("Contact successfully added to your list")
    else:
        print("This person does not exist in our database. Please try again.")
        addContact(acc, connection)


def authenticate(action, toServer, connection):
    # format with the action !
    connection.send_message(toServer)
    state = connection.receive_message()
    if state:
        return True
    else:
        return False
