from src.Crypt.diffhellm import build
import base64
import hashlib

from cryptography.fernet import Fernet


def setup(username: str):
    dh = build(username)
    return dh


def convert_key_to_fernet(shared_key):
    shared_key = int(shared_key, 16)
    return base64.urlsafe_b64encode(shared_key.to_bytes(32, 'big'))


def encrypt_msg(fern: Fernet, msg):
    return fern.encrypt(bytes(msg, 'utf-8'))


def decrypt_str_msg(fern: Fernet, tok):
    return str(fern.decrypt(tok), 'utf-8')


def hash_pswd(password: str):
    res = hashlib.md5(password.encode('utf-8'))
    print(res.hexdigest())
    return res.hexdigest()
