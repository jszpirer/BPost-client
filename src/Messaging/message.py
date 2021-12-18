class Message:

    def __init__(self, sender, recipient, content):
        self.sender = sender
        self.recipient = recipient
        self.content = content

    # store username and password in database

    def messageSomeone(self):
        # print(sender.contacts)
        # might print a list of contacts
        self.recipient = input("Send to : ")
        self.content = input("Write here : ")
