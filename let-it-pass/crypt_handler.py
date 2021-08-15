import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64

# encryption salt
SALT = b'b3sT s@1t 3vaa'

# hash a password and return the hashed result
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf8'), salt)
    return hashed

# validate a password
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf8'), hashed)

# decrypt and password using a given key
def decrypt_password(encrypted, key):
    crypter = Fernet(key)
    decrypted = crypter.decrypt(encrypted)
    return decrypted

# encrypt a password using a given key
def encrypt_password(password, key):
    crypter = Fernet(key)
    encrypted = crypter.encrypt(password.encode('utf8'),)
    return encrypted

# make a key for encryption from the master password
def make_key(password):
    global SALT
    kdf = Scrypt(salt = SALT, length = 32, n = 2 ** 14 ,r = 8, p = 1)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf8')))
    return key
