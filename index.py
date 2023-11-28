from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64, os

def load_public_key(file_name):
    with open(file_name, 'rb') as file:
        public_key_data = file.read()
        public_key = serialization.load_pem_public_key(public_key_data, backend=default_backend())
    return public_key

def load_private_key(file_name):
    with open(file_name, 'rb') as file:
        private_key_data = file.read()
        private_key = serialization.load_pem_private_key(private_key_data, password=None, backend=default_backend())
    return private_key

def encrypt_file(msg, key):
    encrypted_msg = base64.b64encode(key.encrypt(
        msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ))
    return encrypted_msg

def decrypt_file(msg, key):
    decrypted_msg = key.decrypt(
        base64.b64decode(msg), 
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_msg

def main():
    new_directory = 'new_user_profiles'
    file_path = "user_profiles"
    files = os.listdir(file_path)
    old_key = load_private_key('old_private_key.pem')
    new_key = load_public_key('new_public_key.pem')

    file_name = 'valerie83.bin'
    os.makedirs(new_directory)

    with open('user_profiles/valerie83.bin', 'rb') as file:
        encrypted_file = file.read()

    decrypted_file = decrypt_file(encrypted_file, old_key)

    newly_encrypted_file = encrypt_file(decrypted_file, new_key)

    with open (new_directory + '/' + file_name, 'wb') as file:
        file.write(newly_encrypted_file)

    for f in files:
        if os.path.isfile(os.path.join(file_path, f)):
            print(f)
            with open(file_path + '/' + f, 'rb') as file:
                encrypted_file = file.read()

            decrypted_file = decrypt_file(encrypted_file, old_key)

            newly_encrypted_file = encrypt_file(decrypted_file, new_key)

            with open (new_directory + '/' + f, 'wb') as file:
                file.write(newly_encrypted_file)

if __name__ == "__main__":
    main()