import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import InvalidToken

def Decryption(role):

    try:
         # Load your private key
        with open('private_keyDHnew.pem', 'rb') as private_key_file:
            private_key = serialization.load_pem_private_key(private_key_file.read(), password=None)

        # Load the sender's public key
        with open('public_keyDHnew.pem', 'rb') as public_key_file:
            sender_public_key = serialization.load_pem_public_key(public_key_file.read())

        # Generate a shared key using Diffie-Hellman
        shared_key = private_key.exchange(sender_public_key)

        # Derive an encryption key using a KDF (e.g., PBKDF2)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=b'MyFixedSalt1234',
            iterations=100000,
            length=32  # Specify the desired key length
        )

        encryption_key = kdf.derive(shared_key)

        # Create a Fernet key using the derived key
        fernet_key = base64.urlsafe_b64encode(encryption_key)

        # Create a Fernet cipher using the Fernet key
        cipher = Fernet(fernet_key)

        if role=='Admin':

        # Load and decrypt the encrypted data
            with open('EncryptedFileAdmin', 'rb') as encrypted_file:
                encrypted_data = encrypted_file.read()
            decrypted_data = cipher.decrypt(encrypted_data)
            data =decrypted_data.decode('utf-8')
        else:
            with open('EncryptedFileUser', 'rb') as encrypted_file:
                encrypted_data = encrypted_file.read()
            decrypted_data = cipher.decrypt(encrypted_data)
            data=decrypted_data.decode('utf-8')
            

        #print("Decrypted Message:", decrypted_data.decode('utf-8'))
        return data

    # except InvalidToken as ei:
    #     print(ei)
    except Exception as e:
        print(f"An error occurred during decryption: {str(e)}")