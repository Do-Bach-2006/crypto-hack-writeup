from Crypto.PublicKey import RSA
from Crypto.Util.asn1 import DerSequence
from Crypto.Util.number import bytes_to_long

with open('2048b-rsa-example-cert_3220bd92e30015fe4fbeb84a755e7ca5.der', 'rb') as f:
    der_data = f.read()


key = RSA.importKey(der_data)
print(f"Modulus (n) dạng Decimal: {key.n}")