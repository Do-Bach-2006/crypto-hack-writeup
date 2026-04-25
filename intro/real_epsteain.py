#!/usr/bin/env python3
import mpmath as mp

mp.mp.dps = 120

ct = 1350995397927355657956786955603012410260017344805998076702828160316695004588429433

PRIMES = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    103,
]

known = "crypto{" + "?" * 15 + "}"

scale = mp.mpf(16) ** 64

known_sum = mp.mpf(0)
unknown_roots = []

for i, c in enumerate(known):
    root = mp.sqrt(PRIMES[i])

    if c == "?":
        unknown_roots.append(root)
    else:
        known_sum += ord(c) * root

target = mp.mpf(ct) / scale - known_sum

# We want:
#   x0*sqrt(p0) + x1*sqrt(p1) + ... = target
#
# So PSLQ searches for:
#   a0*sqrt(p0) + ... + an*target = 0
#
# The result should be:
#   [-x0, -x1, ..., -x14, 1]

relation = mp.pslq(
    unknown_roots + [target], tol=mp.mpf("1e-70"), maxcoeff=10000, maxsteps=10000
)

print("relation =", relation)

coeffs = relation[:-1]
last = relation[-1]

middle = "".join(chr(int(-c / last)) for c in coeffs)
flag = "crypto{" + middle + "}"

print(flag)
