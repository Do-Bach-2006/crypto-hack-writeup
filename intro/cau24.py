import requests
import hashlib
from Crypto.Cipher import AES

# The base URL for this specific challenge
BASE_URL = "https://aes.cryptohack.org/passwords_as_keys/"

def get_encrypted_flag():
    """Calls the encrypt_flag endpoint to get the ciphertext."""
    url = f"{BASE_URL}/encrypt_flag/"
    response = requests.get(url)
    return response.json()['ciphertext']

def decrypt_via_api(ciphertext, key_hex):
    """Calls the decrypt endpoint with a specific ciphertext and hex key."""
    url = f"{BASE_URL}/decrypt/{ciphertext}/{key_hex}/"
    response = requests.get(url)
    return response.json()['plaintext']

def local_decrypt(ciphertext, key_bytes):
    """Local implementation of the server's decryption logic."""
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    try:
        return cipher.decrypt(ciphertext)
    except Exception:
        return None


ciphertext = get_encrypted_flag()
print(f"Target Ciphertext: {ciphertext}")
ciphertext = bytes.fromhex(ciphertext)

with open("wordlist.txt", "r") as f:
    for line in f:
        word = line.strip()
        key_hash = hashlib.md5(word.encode()).digest()
        result = local_decrypt(ciphertext, key_hash)

        if result == None:
            print("no")
            continue
        
        

        result = result.hex()


        byte_result = bytes.fromhex(result)
        print("gettin something !")
        if b"crypto" in byte_result:
            print(f"Found flag: {byte_result}")
            break
        