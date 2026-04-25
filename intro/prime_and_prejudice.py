#!/usr/bin/env python3
import json
import socket
from math import gcd

from sympy import isprime, nextprime, primerange
from sympy.ntheory.modular import crt
from sympy.functions.combinatorial.numbers import kronecker_symbol


HOST = "socket.cryptohack.org"
PORT = 13385

BASES = list(primerange(2, 64))


def generate_basis(n):
    basis = [True] * n
    for i in range(3, int(n**0.5) + 1, 2):
        if basis[i]:
            basis[i * i :: 2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, n, 2) if basis[i]]


def server_miller_rabin(n, b=64):
    basis = generate_basis(b)

    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for base in basis:
        x = pow(base, s, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                break
        else:
            return False

    return True


def backtrack(S, X, M, i=0):
    if i == len(S):
        res = crt(M, X)

        if res is None:
            return None, None

        z, m = res
        return int(z), int(m)

    modulus = 4 * BASES[i]

    for residue in S[i]:
        res = crt(M + [modulus], X + [residue])

        if res is None:
            continue

        z, m = backtrack(S, X + [residue], M + [modulus], i + 1)

        if z is not None:
            return z, m

    return None, None


def generate_pseudoprime(min_bits=601):
    """
    Generate composite:

        n = p1 * p2 * p3

    where:

        p2 = k2 * (p1 - 1) + 1
        p3 = k3 * (p1 - 1) + 1

    This construction makes n pass Miller-Rabin for the fixed bases.
    """

    k2 = int(nextprime(BASES[-1]))  # 67

    while True:
        k3 = int(nextprime(k2))  # 71, then 73, 79, ...

        while True:
            if gcd(k2, k3) == 1:
                break
            k3 = int(nextprime(k3))

        print(f"[*] trying k2={k2}, k3={k3}")

        X = [
            pow(-k3, -1, k2),
            pow(-k2, -1, k3),
        ]

        M = [k2, k3]

        S = []

        for a in BASES:
            Sa = set()

            for r in range(1, 4 * a, 2):
                if int(kronecker_symbol(a, r)) == -1:
                    Sa.add(r)

            good = set(Sa)

            for ki in M:
                filtered = set()

                for s in Sa:
                    value = (pow(ki, -1, 4 * a) * (s + ki - 1)) % (4 * a)
                    filtered.add(value)

                good &= filtered

            if not good:
                break

            S.append(list(good))

        if len(S) != len(BASES):
            k2 = k3
            continue

        z, m = backtrack(S, X, M)

        if z is None:
            k2 = k3
            continue

        print("[+] found residue class")

        i = (2 ** (min_bits // 3)) // m

        while True:
            p1 = z + i * m
            p2 = k2 * (p1 - 1) + 1
            p3 = k3 * (p1 - 1) + 1

            if isprime(p1) and isprime(p2) and isprime(p3):
                n = p1 * p2 * p3

                if 600 < n.bit_length() <= 900:
                    assert server_miller_rabin(n, 64)
                    return n, p1, p2, p3

            i += 1


def recv_json(f):
    return json.loads(f.readline().decode())


def send_json(f, obj):
    f.write(json.dumps(obj).encode() + b"\n")
    f.flush()
    return recv_json(f)


def main():
    n, p1, p2, p3 = generate_pseudoprime()

    print("[+] n =", n)
    print("[+] p1 =", p1)
    print("[+] p2 =", p2)
    print("[+] p3 =", p3)
    print("[+] bits =", n.bit_length())
    print("[+] passes server MR =", server_miller_rabin(n, 64))

    # Use one factor as base.
    # gcd(base, n) != 1, so Fermat does not apply.
    base = p1

    x = pow(base, n - 1, n)
    print("[+] local x =", x)

    s = socket.create_connection((HOST, PORT))
    f = s.makefile("rwb")

    print(f.readline().decode().strip())

    res = send_json(
        f,
        {
            "prime": n,
            "base": base,
        },
    )

    print(res)


if __name__ == "__main__":
    main()
