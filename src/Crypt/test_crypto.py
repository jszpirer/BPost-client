import crypto
import base64
from cryptography.fernet import Fernet

dh = crypto.setup("Alex")

# Fait usr l'autre machien
dh2 = crypto.setup("Eli")

# On recoit du serveur
foreign_pub_key = dh2.public_key
print("foreign", foreign_pub_key)

dh.generate_shared_secret(foreign_pub_key, True)
print("key :",dh.shared_key)


# Autre machine
dh2.generate_shared_secret(dh.public_key, True)

fern_key = crypto.convert_key_to_fernet(dh.shared_key)
f = Fernet(fern_key)

msg = "Hello la crypto"

# Envoyer msg à user2
# acc.encrypt(msg, user2)
tok = crypto.encrypt_msg(f, "Hello la crypto")
print(tok)
# send_via_serv

# Recois un msg du serv
decrypt = crypto.decrypt_str_msg(f, tok)
print(decrypt)
