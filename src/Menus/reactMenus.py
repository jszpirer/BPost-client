from Account.account import *
from Messaging.message import *
from Menus.printMenus import *
from asyncronous_functions import *
from format import *
from ServerConnection import ServerConnection
from Crypt.crypto import hash_pswd

sep = "<SEP>"


async def reactTopMenu(option, connection):
    if option == 1:  # create account
        acc = await createAccount(connection)
    elif option == 2:  # login
        acc = await authenticate(connection)
    else:
        print("Invalid option. Please enter a number between 1 and 2")
    printActionMenu()
    while True:
        try:
            action = await ainput("Enter your choice : ")
            action = int(action)
            break
        except:
            print("Wrong input. Please enter a number")
    await reactActionMenu(action, acc, connection)


async def reactActionMenu(option, acc, connection):
    if option == 1:  # send a message
        toServ = await sendMessage(acc, connection)
    elif option == 2:  # add a contact to the contact list
        await addContact(acc, connection)
    elif option == 3:  # change password
        acc = await changePassword(acc, connection)
    else:
        print("Invalid option. Please enter a number between 1 and 2")
    printActionMenu()
    while True:
        try:
            action = await ainput("Enter your choice : ")
            action = int(action)
            break
        except:
            print("Wrong input. Please enter a number")
    await reactActionMenu(action, acc, connection)


async def sendMessage(acc, connection):
    print("Here is your contact list : ", acc.contacts)
    recipient = await ainput("Send to : ")
    content = await ainput("Write here : ")
    toServ = [acc.getUsername(), content, recipient]
    formatted_request = format_send_message(toServ)
    connection.send_message(formatted_request)
    if await confirmationServ(0, connection):
        mess = Message(acc.getUsername(), recipient, content)
        return mess
    else:
        print("This person does not exist in our database. Please try again.")
        return await sendMessage(acc, connection)


async def createAccount(connection):
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
    print("Welcome back to the BPost Messaging App !")
    print("Please enter your username and then enter your password")
    username, password = await get_user_identification()
    return await login_on_serv(connection, username, password)


async def login_on_serv(connection, username, password):
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
    username = await ainput("Username : ")
    password = await ainput("Your password : ")
    password = hash_pswd(password)
    return username, password


async def changePassword(acc, connection):
    oldPassword = await ainput("Current password : ")
    if hash_pswd(oldPassword) == acc.password:
        newPassword = await ainput("New password : ")
        confNewPassword = await ainput("Please confirm your new password : ")
        if newPassword == confNewPassword:
            newPassword = hash_pswd(newPassword)
            toServ = [acc.getUsername(), hash_pswd(oldPassword), newPassword]
            formatted_request = format_change_password(toServ)
            connection.send_message(formatted_request)
            if confirmationServ(3, connection):
                print("Password successfully modified")
                acc = Account(acc.getUsername(), newPassword)
                return acc
        else:
            print("Passwords don't match")
            await changePassword(acc, connection)
    else:
        print("Your password is incorrect. Please try again")
        await changePassword(acc, connection)


async def addContact(acc, connection):
    contact = await ainput("What is the username of the contact you would like to add to your list : ")
    toServ = [acc.getUsername(), contact]
    formatted_request = format_add_contact(toServ)
    connection.send_message(formatted_request)
    if await confirmationServ(4, connection):
        acc.newContact(contact)
        print("Contact successfully added to your list")
    else:
        print("This person does not exist in our database. Please try again.")
        await addContact(acc, connection)


async def confirmationServ(action: int, connection: ServerConnection):
    """checks the answer of the server to the action request (username correct, etc)"""
    while True:
        for order_response in connection.server_responses:
            print(order_response)
            if order_response[0] == action:  # checks the action value
                connection.server_responses.remove(order_response)
                return order_response[1]
        await asyncio.sleep(1)
