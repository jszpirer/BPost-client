class Account:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.contacts = []

    # store username and password in database


    def newContact(self, contactUsername):
        self.contacts.append(contactUsername)

    def getUsername(self):
        return self.username