import Crypt.crypto as crpt
from Account.Database import Database as keyDatabase


class Account:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.dh = crpt.setup(self.username)  # Generating private and public key or read them if already existed for
        # user and machine
        self.contact_fernets = dict()  # Dictionnaire où clef=username, valeur=fernet(clefpartagée)
        self.key_database = keyDatabase("key_database.db")

        self.contacts = self.key_database.select_contact_list(self.username)
        for contact in self.contacts:
            shared_key = self.key_database.select_common_key(username, contact)
            self.contact_fernets[contact] = crpt.create_fernet_from_shared_key(shared_key)

    # store username and password in database
    def newContact(self, contact_username, contact_public_key):
        self.contacts.append(contact_username)
        print(contact_public_key, type(contact_public_key))
        self.dh.generate_shared_secret(int(contact_public_key))
        self.key_database.add_new_line(self.username, contact_username, self.dh.shared_key)
        self.contact_fernets[contact_username] = crpt.create_fernet_from_shared_key(self.dh.shared_key)

    def getUsername(self):
        return self.username