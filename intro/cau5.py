import base64

encrypted_messenge = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"

base64_messege = base64.b64encode(bytes.fromhex(encrypted_messenge))

print(base64_messege)
