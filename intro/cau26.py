import requests
import string
import time

# Use a session to keep the connection alive (FASTER and more stable)
session = requests.Session()
BASE_URL = "https://aes.cryptohack.org/ecb_oracle/encrypt/"

# Optimized alphabet: flags are usually lowercase, numbers, or underscores
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz_{}" + string.ascii_uppercase

def get_encryption(plaintext_hex):
    url = f"{BASE_URL}{plaintext_hex}/"
    retries = 0
    
    while retries < 5: # Stop trying after 5 consecutive failures
        try:
            r = session.get(url, timeout=5)
            
            if r.status_code == 429:
                print("\n[!] Rate limited. Sleeping for 10s...")
                time.sleep(10)
                continue
                
            # If the server returns a 500 or 502 error, it will print it here
            if r.status_code != 200:
                print(f"\n[!] URL requested: {url}")
                print(f"[!] Server returned status code: {r.status_code}")
                print(f"[!] Server response: {r.text[:100]}...")
                time.sleep(3)
                retries += 1
                continue
                
            return r.json()['ciphertext']
            
        except Exception as e:
            # NOW it will tell us what the error actually is!
            print(f"\n[!] Request failed: {e}")
            time.sleep(2)
            retries += 1
            
    print("\n[!] Fatal Error: Could not connect to server after 5 attempts. Exiting.")
    exit(1)
def solve():
    # RESUME point
    found_flag = "crypto{p3n6u1n" 
    
    print(f"[!] Resuming from: {found_flag}")

    while not found_flag.endswith("}"):
        # Calculate padding
        padding_len = (-len(found_flag) - 1) % 16
        if padding_len == 0:
            padding_len = 16
            
        padding = "a" * padding_len
        
        # Get target block
        target_hex = get_encryption(padding.encode().hex())
        
        # Calculate how many blocks to look at
        num_blocks = (len(found_flag) + padding_len) // 16 + 1
        target_chunk = target_hex[:num_blocks * 32]
        
        found_next = False
        
        # Iterate through our optimized alphabet
        for char in ALPHABET:
            print(f"Testing: {found_flag + char}", end="\r")
            
            payload = (padding + found_flag + char).encode().hex()
            guess_hex = get_encryption(payload)
            
            if guess_hex[:num_blocks * 32] == target_chunk:
                found_flag += char
                found_next = True
                break
        
        if not found_next:
            print("\n[!] Character not found in alphabet. Trying full printable set...")
            for char in string.printable:
                if char in ALPHABET: continue # skip what we tried
                payload = (padding + found_flag + char).encode().hex()
                if get_encryption(payload)[:num_blocks * 32] == target_chunk:
                    found_flag += char
                    found_next = True
                    break
            
            if not found_next:
                print("\n[!] Total failure. Check block alignment.")
                break

    print(f"\n\n[🎉] FLAG FOUND: {found_flag}")

if __name__ == "__main__":
    solve()