#!/usr/bin/env python3
import requests

BASE = "https://aes.cryptohack.org/lazy_cbc"


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def main():
    # Any 16-byte plaintext block is fine
    plaintext = b"A" * 16

    # Ask server to encrypt it
    r = requests.get(f"{BASE}/encrypt/{plaintext.hex()}/")
    c0 = bytes.fromhex(r.json()["ciphertext"])

    # Build malicious ciphertext:
    # C0 || 0-block || C0
    forged = c0 + bytes(16) + c0

    # Send to receive endpoint.
    # It will fail ASCII decoding and leak decrypted plaintext hex.
    r = requests.get(f"{BASE}/receive/{forged.hex()}/")
    err = r.json()["error"]

    leaked_hex = err.split(": ")[1]
    leaked = bytes.fromhex(leaked_hex)

    p0 = leaked[:16]
    p2 = leaked[32:48]

    key = xor(p0, p2)

    print("[+] recovered key:", key.hex())

    # Use recovered key to get flag
    r = requests.get(f"{BASE}/get_flag/{key.hex()}/")
    flag = bytes.fromhex(r.json()["plaintext"])

    print("[+] flag:", flag.decode())


if __name__ == "__main__":
    main()
