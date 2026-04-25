import requests

BASE_URL = "https://aes.cryptohack.org/ecbcbcwtf"

def get_encrypted_flag():
    url = f"{BASE_URL}/encrypt_flag/"
    response = requests.get(url)
    return response.json()['ciphertext']

def decrypt_block_via_api(hex_block):
    url = f"{BASE_URL}/decrypt/{hex_block}/"
    response = requests.get(url)
    return response.json()['plaintext']

def xor(b1, b2):
    # XORs two byte objects together
    return bytes([a ^ b for a, b in zip(b1, b2)])

print("[-] Fetching the full ciphertext...")
full_hex = get_encrypted_flag()
full_bytes = bytes.fromhex(full_hex)

# Split into 16-byte blocks
blocks = [full_bytes[i:i+16] for i in range(0, len(full_bytes), 16)]

iv = blocks[0]
ciphertext_blocks = blocks[1:]

print(f"[-] Found IV and {len(ciphertext_blocks)} ciphertext blocks.")
print("[-] Starting the API decryption loop...\n")

flag = b""
prev_block = iv

# Here is your loop! It will only run as many times as there are blocks (usually ~2)
for i, block in enumerate(ciphertext_blocks):
    print(f"[*] Sending block {i+1} to API...")
    
    # 1. Request -> get HEX from server
    decrypted_hex = decrypt_block_via_api(block.hex())
    
    # 2. HEX -> Bytes
    decrypted_bytes = bytes.fromhex(decrypted_hex)
    
    # 3. XOR with the previous ciphertext block (or IV for the first round)
    plaintext_bytes = xor(decrypted_bytes, prev_block)
    
    # Add to our final flag
    flag += plaintext_bytes
    
    print(f"    [+] Plaintext chunk: {plaintext_bytes}")
    
    # Set the current block as the 'previous' block for the next loop iteration
    prev_block = block

print("\n[🎉] Final Flag Decoded:")
print(flag.decode('utf-8', errors='ignore'))