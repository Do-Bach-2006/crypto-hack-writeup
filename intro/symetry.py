#!/usr/bin/env python3
import requests

BASE = "https://aes.cryptohack.org/symmetry"


def main():
    # Get encrypted flag
    r = requests.get(f"{BASE}/encrypt_flag/")
    data = r.json()

    if "error" in data:
        raise SystemExit(data["error"])

    raw = bytes.fromhex(data["ciphertext"])

    iv = raw[:16]
    ct = raw[16:]

    # OFB encryption and decryption are the same:
    # encrypt(ciphertext, same IV) = plaintext
    r = requests.get(f"{BASE}/encrypt/{ct.hex()}/{iv.hex()}/")
    data = r.json()

    if "error" in data:
        raise SystemExit(data["error"])

    flag = bytes.fromhex(data["ciphertext"])
    print(flag.decode())


if __name__ == "__main__":
    main()
