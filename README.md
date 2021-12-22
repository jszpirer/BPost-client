# BPost-client
Une application de messagerie cryptée moderne et jamais en retard.

BPost is a Messaging App implemented for the project of the Communication Networks : Protocols and Architectures course from Prof. Dricot.

# Execute
This project uses a command-line interface.

To launch the client part of the project, first launch the server (cf. BPost-server repository : https://github.com/AFlachs/BPost-server)

To open a client session, execute the file src/main.py within a Python Virtual Environment. All modules used in the App are listed in the requirements.txt document. These allow users to build an adapted Python Virtual Environment.
Careful that a user can log in on one device only.

# Structure

The source code is in src.

# Functionalities

Creating accounts, logging into registered accounts, adding contacts, sending and recieving messages, changing passwords.

You can only send messages to contacts you have in your contact list.

# Cryptography 
This messaging app crypts the messages between two clients by using symmetric cryptography based on a common key given by the Diffie-Hellman algorithm.
