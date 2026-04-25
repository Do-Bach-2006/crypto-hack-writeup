#!/usr/bin/env python3
import requests
import string
import time

BASE = "https://aes.cryptohack.org/ctrime/encrypt"

alphabet = (
    "}"
    + "!"
    + "_"
    + "@"
    + "?"
    + string.ascii_uppercase
    + string.digits
    + string.ascii_lowercase
)

session = requests.Session()


def encrypt(payload: bytes) -> bytes:
    r = session.get(f"{BASE}/{payload.hex()}/", timeout=10)
    data = r.json()

    if "error" in data:
        raise SystemExit(data["error"])

    return bytes.fromhex(data["ciphertext"])


def main():
    flag = b"crypto{"

    # Current compressed ciphertext length for known prefix
    current_len = len(encrypt(flag))

    while not flag.endswith(b"}"):
        found = False

        for c in alphabet:
            guess = flag + c.encode()
            guess_len = len(encrypt(guess))

            print(c, guess_len)

            # Correct guess usually keeps compressed length unchanged
            if guess_len == current_len:
                flag = guess
                current_len = guess_len
                found = True

                print("[+] flag =", flag.decode())
                break

            time.sleep(0.2)

        # Sometimes zlib length increases by 2 at a boundary.
        # Then continue from the new baseline.
        if not found:
            current_len += 2
            print("[*] compression boundary, new target len =", current_len)

    print("[+] final:", flag.decode())


if __name__ == "__main__":
    main()
