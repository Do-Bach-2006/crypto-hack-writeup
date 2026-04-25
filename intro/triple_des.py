#!/usr/bin/env python3
import requests
from Crypto.Util.Padding import unpad

BASE = "https://aes.cryptohack.org/triple_des"

K1 = bytes.fromhex("0101010101010101")
K2 = bytes.fromhex("FEFEFEFEFEFEFEFE")

# Valid 2-key 3DES format: K1 || K2 || K1
key = K1 + K2 + K1
key_hex = key.hex()


def get_json(url):
    r = requests.get(url)
    data = r.json()
    print(data)

    if "error" in data:
        raise SystemExit(data["error"])

    return data


def main():
    # Step 1: encrypt the flag
    data = get_json(f"{BASE}/encrypt_flag/{key_hex}/")
    ct = data["ciphertext"]

    # Step 2: encrypt the ciphertext again with the same weak key
    data = get_json(f"{BASE}/encrypt/{key_hex}/{ct}/")
    pt = bytes.fromhex(data["ciphertext"])

    # Step 3: remove PKCS#7 padding
    flag = unpad(pt, 8)

    print(flag.decode())


if __name__ == "__main__":
    main()
