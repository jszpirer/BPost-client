class Account:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.contacts = []

    # store username and password in database

    def newAccount(self):
        print("You don't have an account yet")
        self.username = input("Username : ")
        self.password = input("Your password : ")

    def login(self):
        # account already in DB
        self.username = input("Username : ")
        self.password = input("Your password : ")

    def newContact(self, contactUsername):
        self.contacts.append(contactUsername)

