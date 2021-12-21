sep = "<SEP>"

def format_send_message(to_server):  #send
    sender = to_server[0]
    message = to_server[1]
    recipient = to_server[2]
    return str(0)+sep+sender+sep+message+sep+recipient


def format_login_request(to_server):  #auth
    username = to_server[0]
    password = to_server[1]
    return str(1)+sep+username+sep+str(password)


def format_new_account(to_server):  #new acc
    username = to_server[0]
    password = to_server[1]
    return str(2)+sep+username+sep+str(password)


def format_change_password(to_server):  #change pwd
    username = to_server[0]
    curr_password = to_server[1]
    new_password = to_server[2]
    return str(3)+sep+username+sep+curr_password+sep+new_password


def format_add_contact(to_server):  #new contact
    username = to_server[0]
    contact = to_server[1]
    return str(4)+sep+username+sep+contact


def format_public_key_announcment(username, pub_key):
    return str(6)+sep+username+sep+str(pub_key)


def inverse_format(from_server):
    """Recognizes action from the server and says whether it should execute"""
    input = from_server.split(sep)
    action = int(input[0])
    strbool = input[1]  # "True"
    if action in range(5):
        bool_res = True if strbool == "OK" else False
        return action, bool_res
    elif action == 5:
        """server is sending a message to a client"""
        mess = input[1]
        sender = input[2]
        return sender, mess
    else:
        print("error action "+str(action))


def order_is_confirmation(order: str):
    input = order.split(sep)
    if int(input[0]) in range(5):
        return True
