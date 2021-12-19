from Account.account import *
from Messaging.message import *


def printTopMenu():
    print("1 -- Create an account")
    print("2 -- Login")


def printActionMenu():
    print("1 -- Send a message")
    print("2 -- Add a contact to my list")


def reactTopMenu(option):
    if option == 1:  # create account
        print("You don't have an account yet. Please enter a username and then enter a password")
        username = input("Username : ")
        password = input("Your password : ")
        password = hash(password)
        acc = Account(username, password)
        toServ = [acc]  # info to send to the server
        print("You have successfully created you BPost Account !")

    elif option == 2:  # login
        print("Welcome back to the BPost Messaging App !")
        print("Please enter your username and then enter your password")
        username = input("Username : ")
        password = input("Your password : ")
        password = hash(password)
        toServ = [username, password]  # info to send to the server
        # il faut pouvoir avoir l'account en return
    else:
        print("Invalid option. Please enter a number between 1 and 2")

    printActionMenu()
    try:
        action = int(input("Enter your choice : "))
    except:
        print("Wrong input. Please enter a number")
    reactActionMenu(action,acc)
    return option, toServ


def reactActionMenu(option, acc):
    if option == 1:  # send a message
        # print(sender.contacts)
        # might print a list of contacts
        recipient = input("Send to : ")
        content = input("Write here : ")
        mess = Message(acc.getUsername(), recipient, content)
        toServ = [mess]
    elif option == 2:  # add a contact to the contact list
        contact = input("What is the username of the contact you would like to add : ")
        acc.newContact(contact)
        # ajouter au serveur ?
    else :
        print("Invalid option. Please enter a number between 1 and 2")
    return option, toServ