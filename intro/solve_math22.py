from pwn import *
import json

HOST = "socket.cryptohack.org"
PORT = 13403


def recv_json_string_after_prefix(r, prefix: bytes) -> str:
    r.recvuntil(prefix)
    line = r.recvline().decode().strip()
    return json.loads(line)  # removes surrounding quotes


def recv_hex_after_prefix(r, prefix: bytes) -> int:
    s = recv_json_string_after_prefix(r, prefix)
    return int(s, 16)


def recv_json_obj(r):
    while True:
        line = r.recvline().decode(errors="ignore").strip()
        if not line:
            continue
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            print(f"[debug] skipping non-json line: {line!r}")


def json_send(r, obj):
    r.sendline(json.dumps(obj).encode())


while True:
    r = remote(HOST, PORT)

    # Prime generated: "0x...."
    q = recv_hex_after_prefix(r, b"Prime generated: ")
    print(f"[+] q = {q}")

    r.recvuntil(b"Send integers (g,n) such that pow(g,q,n) = 1: ")

    g = q + 1
    n = q * q
    json_send(r, {"g": hex(g), "n": hex(n)})

    # Generated my public key: "0x...."
    h = recv_hex_after_prefix(r, b"Generated my public key: ")
    print(f"[+] h = {h}")

    r.recvuntil(b"What is my private key: ")

    # rare ambiguous case
    if h == 1:
        print("[!] h == 1, retrying")
        r.close()
        continue

    x = (h - 1) // q
    print(f"[+] recovered x = {x}")

    json_send(r, {"x": hex(x)})

    result = recv_json_obj(r)
    print(result)

    r.close()
    break
