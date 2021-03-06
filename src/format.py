sep = "<SEP>"


def format_send_message(to_server):  #send
    """Formats the message with sender and recipient info to add to the list of elements to send to the server"""
    sender = to_server[0]
    message = to_server[1]
    recipient = to_server[2]
    return str(0)+sep+sender+sep+str(message)+sep+recipient


def format_login_request(to_server):  #auth
    """Formats the username and password at login to add to the list of elements
     to send to the server for confirmation"""
    username = to_server[0]
    password = to_server[1]
    return str(1)+sep+username+sep+str(password)


def format_new_account(to_server):  #new acc
    """Formats the username and password at the creation of an account
    to add to the list of elements to send to the server for confirmation"""
    username = to_server[0]
    password = to_server[1]
    return str(2)+sep+username+sep+str(password)


def format_change_password(to_server):  #change pwd
    """Formats the old and new password of an user to add to the list of elements to
    send to the server for confirmation"""
    username = to_server[0]
    curr_password = to_server[1]
    new_password = to_server[2]
    return str(3)+sep+username+sep+curr_password+sep+new_password


def format_add_contact(to_server):  #new contact
    """Formats the information of the contact to add to the contacts list to add to the list of elements
    to send to the server for confirmation"""
    username = to_server[0]
    contact = to_server[1]
    return str(4)+sep+username+sep+contact


def format_public_key_announcment(username, pub_key):
    """Formats the public key"""
    return str(6)+sep+username+sep+str(pub_key)


def inverse_format(from_server):
    """Recognizes action from the server and says whether it should execute"""
    input = from_server.split(sep)
    action = int(input[0])
    strbool = input[1]  # "True"
    if action == 4:
        bool_res = True if strbool == "OK" else False
        # Return la clef publique de l'autre
        if bool_res:
            return action, bool_res, input[2]  # TODO v??rifier le type de la clef publique de l'autre
        else:
            return action, bool_res, "no_key"
    if action in range(5):
        bool_res = True if strbool == "OK" else False
        return action, bool_res
    elif action == 5:
        """server is sending a message to a client"""
        mess = input[1]
        sender = input[2]
        return sender, mess


def order_is_confirmation(order: str):
    """Checks the order is a confirmation message from the server and not a message received from another client"""
    input = order.split(sep)
    if int(input[0]) in range(5):
        return True
