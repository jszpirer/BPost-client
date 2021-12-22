import asyncio

from Account.account import *
from Menus.printMenus import *
from asyncronous_functions import *
from format import *
from ServerConnection import ServerConnection
from Crypt.crypto import hash_pswd
from Crypt.crypto import encrypt_msg

sep = "<SEP>"


async def reactTopMenu(option, connection):
    """Launches the actions requested on the top menu based on the choice (option) requested by the user"""
    if option == 1:  # create account
        acc = await createAccount(connection)
    elif option == 2:  # login
        acc = await authenticate(connection)
    else:
        print("Invalid option. Please enter a number between 1 and 2")
    printActionMenu(connection)
    while True:
        try:
            action = await ainput("Enter your choice : ")
            action = int(action)
            break
        except:
            print("Wrong input. Please enter a number")
    await reactActionMenu(action, acc, connection)


def decrypt_message(receiver, sender, m):
    """Decrypts the message received"""
    fernet = receiver.contact_fernets[sender]
    return crpt.decrypt_str_msg(fernet, m)


async def read_messages(acc, connection):
    """Allows to read the messages of a conversation with another user"""
    messages = connection.private_messages
    for sender in messages:
        print(sender + " (" + str(len(connection.private_messages)) + ")")
    sender = await ainput("Which conversation do you want to read (enter username) :")
    while sender not in messages:
        sender = await ainput("Username not valid, try again :")
    if sender not in acc.contacts:
        print("The sender of the message is not in your contact list, adding it so you can read the message")
        await add_contact(acc, connection, sender)
    for m in messages.pop(sender):
        # Decrypting messages
        msg = decrypt_message(acc, sender, m)
        print(sender + ": " + msg)
    await ainput("Enter to continue")


async def reactActionMenu(option, acc, connection):
    """Launches the actions requested on the action menu based on the choice (option) requested by the user"""
    if option == 1:  # send a message
        await sendMessage(acc, connection)
    elif option == 2:  # add a contact to the contact list
        await askContact(acc, connection)
    elif option == 3:  # change password
        acc = await changePassword(acc, connection)
    elif option == 4:  # Read messages
        await read_messages(acc, connection)
    elif option == 5:  # Exit program
        return
    else:
        print("Invalid option. Please enter a number between 1 and 2")
    printActionMenu(connection)
    while True:
        try:
            action = await ainput("Enter your choice : ")
            action = int(action)
            break
        except:
            print("Wrong input. Please enter a valid number")
    await reactActionMenu(action, acc, connection)


def encrypt(sender, dest, content):
    """Encryption of the message before it is added to the list of messages to send to the server"""
    fernet = sender.contact_fernets[dest]
    return crpt.encrypt_msg(fernet, content)


async def sendMessage(acc, connection):
    """Action to send a message to another user. This function asks the user the destination and content of the message
    then encrypts the message, formats it and adds it to the list of messages to send to the server"""
    print("Here is your contact list : ", acc.contacts)
    dest = await ainput("Send to : ")
    if dest not in acc.contacts:
        print("Contact not in list")
        return
    content = await ainput("Write here : ")
    content = encrypt(acc, dest, content)
    toServ = [acc.getUsername(), content, dest]
    formatted_request = format_send_message(toServ)
    connection.send_message(formatted_request)
    if not await confirmationServ(0, connection):
        print("This person does not exist in our database. Please try again.")
        await sendMessage(acc, connection)


async def createAccount(connection):
    """Asks the username and password of the account the user wants to create, formats the request and adds it to the list of
    information to send to the server"""
    print("You don't have an account yet. Please enter a username and then enter a password")
    username = await ainput("Username : ")
    password = await ainput("Your password : ")
    confPassword = await ainput("Please confirm your password : ")
    if password == confPassword:
        password = hash_pswd(password)
    else:
        print("Passwords don't match")
        return await createAccount(connection)
    toServ = [username, password]  # info to send to the server
    formatted_request = format_new_account(toServ)
    connection.send_message(formatted_request)
    if await confirmationServ(2, connection):
        print("You have successfully created you BPost Account !")
        acc = Account(username, password)
        # Since it is the first connexion of the server we need to send the public key
        pub_key = acc.dh.public_key
        connection.send_message(format_public_key_announcment(acc.getUsername(), pub_key))
        return acc
    else:
        print("This username already exists. Please choose a different username")
        return await createAccount(connection)


async def authenticate(connection):
    """Presents the authentication of the user (username + password) when they enter the app"""
    print("Welcome back to the BPost Messaging App !")
    print("Please enter your username and then enter your password")
    username, password = await get_user_identification()
    return await login_on_serv(connection, username, password)


async def login_on_serv(connection, username, password):
    """Formats the authentication, adds it to the list of information to send to the server, then
    verify the answer of the server to confirm the login"""
    formatted_request = format_login_request([username, password])
    connection.send_message(formatted_request)
    if await confirmationServ(1, connection):
        print("Login successful")
        acc = Account(username, password)
        return acc
    else:
        print("Your username or password is incorrect. Please try again")
        return await authenticate(connection)


async def get_user_identification():
    """Gets the identification of the user when they login"""
    username = await ainput("Username : ")
    password = await ainput("Your password : ")
    password = hash_pswd(password)
    return username, password


async def changePassword(acc, connection):
    """Allows the user to change passwords, based on their current password"""
    oldPassword = await ainput("Current password : ")
    if hash_pswd(oldPassword) == acc.password:
        newPassword = await ainput("New password : ")
        confNewPassword = await ainput("Please confirm your new password : ")
        if newPassword == confNewPassword:
            newPassword = hash_pswd(newPassword)
            toServ = [acc.getUsername(), hash_pswd(oldPassword), newPassword]
            formatted_request = format_change_password(toServ)
            connection.send_message(formatted_request)
            if await confirmationServ(3, connection):
                print("Password successfully modified")
                acc = Account(acc.getUsername(), newPassword)
                return acc
        else:
            print("Passwords don't match")
            await changePassword(acc, connection)
    else:
        print("Your password is incorrect. Please try again")
        await changePassword(acc, connection)


async def askContact(acc, connection):
    """The user enters the name of the contact they want to add to their list"""
    contact = await ainput("What is the username of the contact you would like to add to your list : ")
    await add_contact(acc, connection, contact)


async def add_contact(acc, connection, contact):
    """Formats the info of the contact to add to the contacts list, adds it to the list of info to send to the server,
    validates the addition of the contact to the list and gets the public key of the latter"""
    toServ = [acc.getUsername(), contact]
    formatted_request = format_add_contact(toServ)
    connection.send_message(formatted_request)
    validation, contact_pub_key = await confirmation_new_contact(connection)
    if validation:
        acc.newContact(contact, contact_pub_key)
        print("Contact successfully added to your list")
    else:
        print("This person does not exist in our database. Please try again.")
        await askContact(acc, connection)


async def confirmation_new_contact(connection: ServerConnection):
    """Checks the answer of the server to the addition of a contact to the list of contacts and
    gets the public key of the said contact"""
    while True:
        for order_response in connection.server_responses:
            if order_response[0] == 4:  # Réponse d'un ajout de contact
                connection.server_responses.remove(order_response)
                return order_response[1], order_response[2]
        await asyncio.sleep(0.1)


async def confirmationServ(action: int, connection: ServerConnection):
    """checks the answer of the server to the action request (username correct, etc)"""
    while True:
        for order_response in connection.server_responses:
            if order_response[0] == action:  # checks the action value
                connection.server_responses.remove(order_response)
                return order_response[1]
        await asyncio.sleep(0.1)
