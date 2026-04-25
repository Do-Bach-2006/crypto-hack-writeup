#!/usr/bin/env python3
import requests

BASE = "https://aes.cryptohack.org/flipping_cookie"


def main():
    data = requests.get(f"{BASE}/get_cookie/").json()
    cookie = bytes.fromhex(data["cookie"])

    iv = bytearray(cookie[:16])
    ciphertext = cookie[16:]

    old = b"False"
    new = b"True;"

    offset = len(b"admin=")

    for i in range(len(old)):
        iv[offset + i] ^= old[i] ^ new[i]

    res = requests.get(f"{BASE}/check_admin/{ciphertext.hex()}/{bytes(iv).hex()}/")

    print(res.json())


if __name__ == "__main__":
    main()
