import base64
import codecs
import ssl
import socket
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime, inverse
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import xor
import requests
import hashlib
import string

# Convert string to hex string
hex_str = "crypto".encode().hex()

# Convert hex string to bytes
data_bytes = bytes.fromhex("63727970746f")

# Convert bytes to hex string
hex_from_bytes = data_bytes.hex()

# Convert integer/decimal to bytes
bytes_from_int = long_to_bytes(342391)

# Convert bytes to integer/decimal
int_from_bytes = bytes_to_long(b"test")

# Convert string to base64 string
b64_str = base64.b64encode("crypto".encode()).decode()

# Convert base64 string to bytes
bytes_from_b64 = base64.b64decode("Y3J5cHRv")

# Encode string with rot13
rot13_str = codecs.encode("crypto", "rot_13")

# Decode string with rot13
plain_str = codecs.decode("pelcgb", "rot_13")

# XOR operation between two bytes/strings
xored = xor(b"data", b"key")

# Import a PEM formatted key
with open('example.pem', 'r') as f: pem_key = RSA.importKey(f.read())

# Import an OpenSSH formatted key
with open('id_rsa.pub', 'r') as f: ssh_key = RSA.importKey(f.read())

# Import a CERT (DER) formatted certificate/key
with open('certificate.der', 'rb') as f: cert_key = RSA.importKey(f.read())

# Fetch Transparency logs (Certificate Transparency example)
ct_info = requests.get("https://ct.googleapis.com/logs/eu1/ct/v1/get-sth").json()

# --- Hashing ---
# Calculate SHA256 of a byte string
sha256_hash = hashlib.sha256(b"message").hexdigest()

# --- AES Block Cipher (ECB/CBC) ---
# AES ECB Encryption/Decryption (requires padding)
aes_key = b"16byte_secretkey"
cipher = AES.new(aes_key, AES.MODE_ECB)
encrypted_blocks = cipher.encrypt(pad(b"secret message", AES.block_size))
decrypted_blocks = unpad(cipher.decrypt(encrypted_blocks), AES.block_size)

# AES CBC with IV
iv = b"16byte_random_iv"
cipher_cbc = AES.new(aes_key, AES.MODE_CBC, iv)
encrypted_cbc = cipher_cbc.encrypt(pad(b"secret", AES.block_size))

# --- Mathematical Operations (RSA / Discrete Log) ---
# Generate a large prime (e.g. 512-bit)
p = getPrime(512)
q = getPrime(512)

# Modular Inverse (e.g., finding d in RSA: d = e^-1 mod phi)
d = inverse(65537, (p-1)*(q-1))

# Modular Exponentiation (fast power: base^exp % mod)
cipher_text = pow(1337, 65537, p*q)

# --- Bruteforcing characters ---
# Useful character sets for bruteforcing
charset = string.ascii_letters + string.digits + string.punctuation

import ssl
import socket

# --- TLS Connections & Certificates ---
# Method 1: Using the requests module to verify a connection against a CA PEM 
# and providing a client certificate PEM
# response = requests.get('https://example.com', cert='client_cert.pem', verify='ca_cert.pem')

# Method 2: Manual TLS socket wrapper using the ssl module
# Setting up the TLS context with a CA PEM file to verify the server
# context = ssl.create_default_context(cafile="transparency_afff0345c6f99bf80eab5895458d8eab.pem")

# Wrap a standard socket with the TLS context
# with socket.create_connection(('example.com', 443)) as sock:
#     with context.wrap_socket(sock, server_hostname='example.com') as ssock:
#         print(f"TLS Version: {ssock.version()}")
#         ssock.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")
#         print(ssock.recv(1024))


import requests
response = requests.get('https://example.com', verify='transparency_afff0345c6f99bf80eab5895458d8eab.pem')
print(response.text)

response = requests.get('https://example.com', cert='client_cert.pem', verify='ca_cert.pem')


import ssl
import socket

# 1. Provide the CA PEM to verify the domain you want to connect to
context = ssl.create_default_context(cafile="transparency_afff0345c6f99bf80eab5895458d8eab.pem")

# 2. Connect the regular unencrypted TCP socket
with socket.create_connection(('example.com', 443)) as sock:
    # 3. Layer TLS over the connection securely, providing SNI (Server Name Indication)
    with context.wrap_socket(sock, server_hostname='example.com') as ssock:
        print(f"Connected using {ssock.version()}")

        # 4. Now send your raw encrypted payload
        ssock.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")
        print(ssock.recv(1024))
