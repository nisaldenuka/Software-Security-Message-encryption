from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet

def KeyGeneration():

    #create key
    key=Fernet.generate_key()

    #write a key
    k=open('DHmessage.key','wb')
    k.write(key)
    k.close()
    # Generate a Diffie-Hellman key pair
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    private_key = parameters.generate_private_key()

    # Serialize and save the private key
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open('private_keyDHnew.pem', 'wb') as private_key_file:
        private_key_file.write(private_key_pem)
        private_key_file.close() 


    # Serialize and save the public key
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open('public_keyDHnew.pem', 'wb') as public_key_file:
        public_key_file.write(public_key_pem)
        public_key_file.close() 

