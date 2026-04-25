#!/usr/bin/env python3
import requests

BASE = "https://aes.cryptohack.org/bean_counter"

PNG_HEADER = bytes.fromhex("89504e470d0a1a0a0000000d49484452")


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def main():
    r = requests.get(f"{BASE}/encrypt/")
    data = r.json()

    if "error" in data:
        raise SystemExit(data["error"])

    ct = bytes.fromhex(data["encrypted"])

    # First 16 bytes of any PNG are known
    keystream = xor(ct[:16], PNG_HEADER)

    # Same keystream block is reused for every block
    pt = bytearray()

    for i in range(0, len(ct), 16):
        block = ct[i : i + 16]
        pt += xor(block, keystream[: len(block)])

    with open("bean_flag.png", "wb") as f:
        f.write(pt)

    print("[+] wrote bean_flag.png")


if __name__ == "__main__":
    main()
