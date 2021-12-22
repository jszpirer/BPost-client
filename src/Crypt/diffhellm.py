import genericpath

from diffiehellman.diffiehellman import DiffieHellman
import pathlib
import os


def generate_keys(dh: DiffieHellman, username: str):
    """Generates public and private keys if they are not stored yet"""
    private_key_file = pathlib.Path(__file__).with_name("keys") / username / "private.txt"
    public_key_file = pathlib.Path(__file__).with_name("keys") / username / "public.txt"
    if genericpath.isfile(public_key_file):
        f = open(private_key_file, 'r')
        dh._DiffieHellman__private_key = int(f.read())
        f.close()
        f = open(public_key_file, 'r')
        dh.public_key = int(f.read())
        f.close()
    else:
        os.makedirs(pathlib.Path(__file__).with_name("keys") / username)
        dh.generate_private_key()
        dh.generate_public_key()
        f = open(private_key_file, 'w')
        f.write(str(dh._DiffieHellman__private_key))
        f.close()
        f = open(public_key_file, 'w')
        f.write(str(dh.public_key))
        f.close()


def build(username: str):
    dh = DiffieHellman()
    generate_keys(dh, username)
    return dh

