import Crypt.crypto as crpt


class Account:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.contacts = []
        self.dh = crpt.setup(self.username)  # Generating private and public key or read them if already existed for
        # user and machine
        self.contact_fernets = dict()  # Dictionnaire où clef=username, valeur=fernet(clefpartagée)

    # store username and password in database

    def newContact(self, contactUsername):
        self.contacts.append(contactUsername)

    def getUsername(self):
        return self.username