import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64

SALT = b'b3sT s@1t 3vaa'

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    return hashed

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf8'), hashed)

def decrypt_password(encrypted, key):
    crypter = Fernet(key)
    decrypted = crypter.decrypt(encrypted)
    return decrypted

def encrypt_password(password, key):
    crypter = Fernet(key)
    encrypted = crypter.encrypt(password.encode('utf8'),)
    return encrypted

def make_key(password):
    global SALT
    kdf = Scrypt(salt = SALT, length = 32, n = 2 ** 14 ,r = 8, p = 1)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf8')))
    return key
