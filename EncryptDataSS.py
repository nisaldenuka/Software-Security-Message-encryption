import base64
import os  # Import the os module
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def Encryption(message,role):

    #open the message Key
    skey=open('DHmessage.key','rb')
    key=skey.read()

    # Load your private key without a password
    with open('private_keyDHnew.pem', 'rb') as private_key_file:
        private_key = serialization.load_pem_private_key(private_key_file.read(), password=None)

    # Load the recipient's public key
    with open('public_keyDHnew.pem', 'rb') as public_key_file:
        recipient_public_key = serialization.load_pem_public_key(public_key_file.read())

    # Generate a shared key using Diffie-Hellman
    shared_key = private_key.exchange(recipient_public_key)
    print(shared_key)

    # Derive an encryption key using a KDF (e.g., PBKDF2)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=b'MyFixedSalt1234',
        iterations=100000,
        length=32  # Specify the desired key length
    )

    encryption_key = kdf.derive(shared_key)
    #print(encryption_key)

    # Create a Fernet key using the derived key
    fernet_key = base64.urlsafe_b64encode(encryption_key)

    # Create a Fernet cipher using the Fernet key
    cipher = Fernet(fernet_key)

    # Encrypt the data
    encrypted_data = cipher.encrypt(bytes(message, 'utf-8'))

    # Save the encrypted data to a file
    if  role=='Admin':


        with open('EncryptedFileAdmin', 'wb') as encrypted_file:
           encrypted_file.write(encrypted_data)
    elif role=='User':
        with open('EncryptedFileUser', 'wb') as encrypted_file:
           encrypted_file.write(encrypted_data)