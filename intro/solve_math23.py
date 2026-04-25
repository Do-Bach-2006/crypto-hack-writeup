from math import gcd

DATA = bytes.fromhex(
    "372f0e88f6f7189da7c06ed49e87e0664b988ecbee583586dfd1c6af99bf2034"
    "5ae7442012c6807b3493d8936f5b48e553f614754deb3da6230fa1e16a8d5953"
    "a94c886699fc2bf409556264d5dced76a1780a90fd22f3701fdbcb183ddab404"
    "6affdc4dc6379090f79f4cd50673b24d0b08458cdbe509d60a4ad88a7b4e2921"
)

N = int(
    "7fe8cafec59886e9318830f33747cafd200588406e7c42741859e15994ab6241"
    "0438991ab5d9fc94f386219e3c27d6ffc73754f791e7b2c565611f8fe5054dd1"
    "32b8c4f3eadcf1180cd8f2a3cc756b06996f2d5b67c390adcba9d444697b13d1"
    "2b2badfc3c7d5459df16a047ca25f4d18570cd6fa727aed46394576cfdb56b41",
    16
)

e = 0x10001

c = int(
    "5233da71cc1dc1c5f21039f51eb51c80657e1af217d563aa25a8104a4e84a423"
    "79040ecdfdd5afa191156ccb40b6f188f4ad96c58922428c4c0bc17fd5384456"
    "853e139afde40c3f95988879629297f48d0efa6b335716a4c24bfee36f714d34"
    "a4e810a9689e93a0af8502528844ae578100b0188a2790518c695c095c9d677b",
    16
)

# Convert leaked fixed-point plaintext to integer
m = int.from_bytes(DATA, "big")

# Since m^65536 ≡ 1 (mod N), take repeated square roots of 1.
# For this challenge, 2^8 is the right level to get a nontrivial square root of 1.
a = pow(m, 2**8, N)

p = gcd(a - 1, N)
q = gcd(a + 1, N)

assert p * q == N
assert p != 1 and q != 1

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

flag_int = pow(c, d, N)
flag = flag_int.to_bytes((flag_int.bit_length() + 7) // 8, "big")

print(f"p = {p}")
print(f"q = {q}")
print(flag.decode())
