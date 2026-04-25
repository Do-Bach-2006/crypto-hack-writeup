from pwn import xor

hex_data = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
data = bytes.fromhex(hex_data)

for key in range(256):
    decoded = xor(data, key)
    try:
        text = decoded.decode('utf-8')
        if "crypto{" in text:
            print(f"Success! Key: {key}")
            print(f"Flag: {text}")
    except UnicodeDecodeError:
        pass
