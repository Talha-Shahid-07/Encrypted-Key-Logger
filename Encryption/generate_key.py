from cryptography.fernet import Fernet
import os
from Crypto.Random import get_random_bytes


key = Fernet.generate_key()
with open(".\\key.key", "wb") as f:
    f.write(key)

aes_key = get_random_bytes(32)  # AES 256 requires a 32-byte key
with open(".\\aes_key.key", "wb") as f:
    f.write(aes_key)


# # Generate a new RSA key pair
# key = RSA.generate(2048)

# # Export the private key
# private_key = key.export_key()
# with open(".\\private.pem", "wb") as f:
#     f.write(private_key)

# # Export the public key
# public_key = key.publickey().export_key()
# with open(".\\public.pem", "wb") as f:
#     f.write(public_key)