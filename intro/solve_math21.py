from hashlib import sha1
from sympy.ntheory.residue_ntheory import discrete_log
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

p = 173754216895752892448109692432341061254596347285717132408796456167143559
D = 529
s = 23

Gx = 29394812077144852405795385333766317269085018265469771684226884125940148
Gy = 94108086667844986046802106544375316173742538919949485639896613738390948

Ax = 155781055760279718382374741001148850818103179141959728567110540865590463
Ay = 73794785561346677848810778233901832813072697504335306937799336126503714

Bx = 171226959585314864221294077932510094779925634276949970785138593200069419
By = 54353971839516652938533335476115503436865545966356461292708042305317630

iv = bytes.fromhex("64bc75c8b38017e1397c46f85d4e332b")
ct = bytes.fromhex(
    "13e4d200708b786d8f7c3bd2dc5de0201f0d7879192e6603d7c5d6b963e1df2943e3ff75f7fda9c30a92171bbbc5acbf"
)

# Map points to F_p^*
g = (Gx + s * Gy) % p
au = (Ax + s * Ay) % p
bu = (Bx + s * By) % p

# Recover Alice private key
na = discrete_log(p, au, g)

# Shared element in multiplicative representation
u = pow(bu, na, p)

# Recover x-coordinate from u = x + 23y and u^-1 = x - 23y
shared_secret = ((u + pow(u, -1, p)) * pow(2, -1, p)) % p

# AES key derivation
key = sha1(str(shared_secret).encode("ascii")).digest()[:16]

cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
dec = cipher.decryptor()
pt = dec.update(ct) + dec.finalize()

# PKCS#7 unpad
padlen = pt[-1]
print(pt[:-padlen].decode())
