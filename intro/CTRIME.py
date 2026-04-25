#!/usr/bin/env python3
"""
CRIME Attack: Compression Oracle on CTRIME Challenge

STRATEGY (Tấn công oracle nén):
═══════════════════════════════════════════════════════════════════════════════

1. Server compresses: user_input + FLAG trước khi mã hóa bằng AES-CTR

2. CTR mode không che giấu độ dài → ciphertext length = compressed length

3. zlib loại bỏ chuỗi lặp hiệu quả
   - Nếu input khớp với FLAG prefix → nén tốt hơn → ciphertext ngắn hơn
   - Nếu input sai → không khớp → ciphertext dài hơn

4. Tấn công từng byte:
   - Dự đoán ký tự cho phần FLAG hiện tại
   - Nếu ký tự đúng → ciphertext KHÔNG tăng độ dài (hoặc tăng rất ít)
   - Nếu ký tự sai → ciphertext tăng ~2 bytes

5. Lặp lại tiền tố đã đoán → tăng cường tín hiệu nén

Ví dụ:
   "crypto{" → ciphertext: 68 bytes
   "crypto{x" (sai) → ciphertext: 70 bytes (+2) ✗
   "crypto{c" (đúng) → ciphertext: 68 bytes (giống cũ) ✓

═══════════════════════════════════════════════════════════════════════════════
"""

import requests
import string
import time

BASE = "https://aes.cryptohack.org/ctrime/encrypt"
session = requests.Session()

# Order: special chars first (more likely to be wrong), then alphanumeric
ALPHABET = (
    "}"
    + "!"
    + "_"
    + "@"
    + "?"
    + string.ascii_uppercase
    + string.digits
    + string.ascii_lowercase
)


def encrypt(payload_hex: str) -> int:
    """Send payload and return ciphertext LENGTH (not the ciphertext itself)"""
    url = f"{BASE}/{payload_hex}/"
    try:
        r = session.get(url, timeout=10)
        data = r.json()

        if "error" in data:
            print(f"[!] Error: {data['error']}")
            return None

        ciphertext = data["ciphertext"]
        return len(bytes.fromhex(ciphertext))
    except Exception as e:
        print(f"[!] Exception: {e}")
        return None


def bruteforce():
    """
    Brute force the FLAG character by character.

    Key insight: When guess matches FLAG, ciphertext length stays SAME or
    grows very slowly. When guess is wrong, ciphertext grows by ~2 bytes.
    """
    flag = b"crypto{"

    # Get baseline ciphertext length for known prefix
    cipher_len = encrypt(flag.hex())
    print(f"[+] Starting with: {flag.decode()}")
    print(f"[+] Baseline ciphertext length: {cipher_len}\n")

    max_iterations = 100
    iteration = 0

    while flag.endswith(b"}") == False and iteration < max_iterations:
        iteration += 1
        print(f"[*] Position {len(flag) - 7}: {flag.decode(errors='ignore')}?")

        found = False

        # Try each character in the alphabet
        for c in ALPHABET:
            test_payload = flag + c.encode()
            test_len = encrypt(test_payload.hex())

            if test_len is None:
                print(f"  {c}: [ERROR]")
                continue

            # Print result
            diff = test_len - cipher_len
            symbol = "✓" if test_len == cipher_len else ""
            print(f"  {c}: {test_len} bytes (Δ={diff:+d}) {symbol}")

            # KEY: Character is correct if ciphertext length DOESN'T INCREASE
            # (or increases very little due to padding alignment)
            if test_len == cipher_len:
                flag += c.encode()
                print(f"[+] Found: {flag.decode(errors='ignore')}")
                found = True
                break

            # Small delay to avoid rate limiting
            time.sleep(0.5)

        # If no character maintains same length, increment expected length threshold
        # This happens when the flag contains characters not in our alphabet
        if not found:
            print(f"[!] No character matched at this position")
            print(
                f"[!] Incrementing length threshold from {cipher_len} to {cipher_len + 2}"
            )
            cipher_len += 2
            print(f"[!] Trying next round with higher threshold...\n")

            # Give user a chance to manually add the character if needed
            # In the writeup example, they manually added 'E' when stuck at "CRIM"
            print(f"[?] Current flag: {flag.decode(errors='ignore')}")
            print(
                f"[?] If stuck, you might need to manually guess the next character\n"
            )
        else:
            print()  # Newline for readability

    if flag.endswith(b"}"):
        print(f"\n[✓] FLAG FOUND: {flag.decode()}")
    else:
        print(f"\n[!] Incomplete flag: {flag.decode(errors='ignore')}")

    return flag


def bruteforce_with_manual_fallback():
    """
    Enhanced version that allows manual input if automatic detection fails.
    Useful when dealing with rare characters.
    """
    flag = b"crypto{"
    cipher_len = encrypt(flag.hex())

    print(f"[+] Starting: {flag.decode()}")
    print(f"[+] Baseline length: {cipher_len}\n")

    while not flag.endswith(b"}"):
        print(f"[*] Recovering: {flag.decode(errors='ignore')}?")

        found = False
        candidates = []

        for c in ALPHABET:
            test_payload = flag + c.encode()
            test_len = encrypt(test_payload.hex())

            if test_len is None:
                continue

            diff = test_len - cipher_len
            candidates.append((test_len, c, diff))

            if test_len == cipher_len:
                flag += c.encode()
                print(f"[✓] {c} (length maintained)")
                found = True
                break

            time.sleep(0.3)

        if not found:
            # Show top candidates
            candidates.sort()
            print(f"\n[!] No exact match. Top candidates:")
            for length, c, diff in candidates[:5]:
                print(f"    {c}: {length} bytes (Δ={diff:+d})")

            # Increment threshold
            cipher_len += 2
            print(f"[*] Threshold updated to {cipher_len}")

            # Option for manual input
            manual = input(
                "[?] Enter character to add (or press Enter to continue): "
            ).strip()
            if manual:
                flag += manual.encode()
                cipher_len = encrypt(flag.hex())
                print(f"[+] Manual: {flag.decode(errors='ignore')}")
            print()
        else:
            print()

    print(f"\n[✓] FLAG: {flag.decode()}")
    return flag


if __name__ == "__main__":
    print("=" * 80)
    print("CTRIME: Compression Oracle Attack")
    print("=" * 80)
    print("\n[*] Attack Strategy:")
    print("    1. Server compresses: user_input + FLAG")
    print("    2. CTR mode reveals compressed length via ciphertext length")
    print("    3. If input matches FLAG → better compression → same length")
    print("    4. If input wrong → worse compression → length increases ~2 bytes")
    print("    5. We brute force character by character, looking for 'no increase'\n")

    # Use the basic version (set timeout in case of stuck characters)
    flag = bruteforce()

    # Or use manual fallback version if needed:
    # flag = bruteforce_with_manual_fallback()
