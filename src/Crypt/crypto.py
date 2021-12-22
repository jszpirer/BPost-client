from Crypt.diffhellm import build
import base64
import hashlib

from cryptography.fernet import Fernet


def setup(username: str):
    dh = build(username)
    return dh


def convert_key_to_fernet(shared_key):
    shared_key = int(shared_key, 16)
    return base64.urlsafe_b64encode(shared_key.to_bytes(32, 'big'))


def create_fernet_from_shared_key(shared_key):
    return Fernet(convert_key_to_fernet(shared_key))


def encrypt_msg(fern: Fernet, msg) -> str:
    msg_bytes = bytes(msg, 'utf-8')
    crypted_bytes = fern.encrypt(msg_bytes)
    return str(crypted_bytes, 'utf-8')


def decrypt_str_msg(fern: Fernet, tok: str):
    tok_bytes = bytes(tok, 'utf-8')
    decrypted_bytes = fern.decrypt(tok_bytes)
    return str(decrypted_bytes, 'utf-8')


def hash_pswd(password: str):
    res = hashlib.md5(password.encode('utf-8'))
    return res.hexdigest()
