sep = "<SEP>"

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
    return str(2)+sep+username+sep+password


def format_change_password(to_server):  #change pwd
    username = to_server[0]
    curr_password = to_server[1]
    new_password = to_server[2]
    return str(3)+sep+username+sep+curr_password+sep+new_password


def format_add_contact(to_server):  #new contact
    username = to_server[0]
    contact = to_server[1]
    return str(4)+sep+username+sep+contact


def inverse_format(from_server):
    """Recognizes action from the server and says whether it should execute"""
    input = from_server.split(sep)
    action = input[0]
    strbool = input[1]  #"True"
    if strbool == "OK":
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