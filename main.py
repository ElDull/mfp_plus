from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64
from hashlib import sha256
import os
import json
from getpass import getpass, getuser
HOME = "/home/"+getuser()

                
def store_key(key):
    """
    if no .passman file found
    create and store the hashed key there
    """
    hashed = sha256(key).hexdigest()
    with open(f"{HOME}/.passman_master", 'w') as f:
        json.dump({"master_password":hashed}, f)
    return key
def validate_key(key):
    with open(f'{HOME}/.passman_master') as f:
        if json.load(f)["master_password"] == sha256(key).hexdigest():
            return True
        return False 

def make_key(master_password):
    kdf = Scrypt( # derive key
        salt=b'',
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def encrypt_creds(key, creds, service_name):
    f = Fernet(key)
    enc = [f.encrypt(i.encode()) for i in creds]
    d = {service_name:{enc[0].decode(): enc[1].decode()}}
    return d
def decrypt_creds(d, key, service_name):
    f = Fernet(key)
    dec = {f.decrypt(k.encode()):f.decrypt(v.encode()) for k,v in d[service_name].items()}
    dec = {k.decode():v.decode() for k,v in dec.items()}
    return dec 
def fetch_dict():
    with open(f'{HOME}/.passman') as f:
        return json.load(f)
def update_json(d):
    with open(f'{HOME}/.passman', 'w') as f:
       json.dump(d, f) 
