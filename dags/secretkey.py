import os
import binascii

secret_key = binascii.hexlify(os.urandom(16)).decode()
print(secret_key)