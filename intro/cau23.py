from math import gcd
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes, inverse

# ── Given values ──────────────────────────────────────────────────────────────
p = 10699940648196411028170713430726559470427113689721202803392638457920771439452897032229838317321639599506283870585924807089941510579727013041135771337631951
q = 11956676387836512151480744979869173960415735990945471431153245263360714040288733895951317727355037104240049869019766679351362643879028085294045007143623763
n = p * q

vka   = 124641741967121300068241280971408306625050636261192655845274494695382484894973990899018981438824398885984003880665335336872849819983045790478166909381968949910717906136475842568208640203811766079825364974168541198988879036997489130022151352858776555178444457677074095521488219905950926757695656018450299948207
vkakb = 114778245184091677576134046724609868204771151111446457870524843414356897479473739627212552495413311985409829523700919603502616667323311977056345059189257932050632105761365449853358722065048852091755612586569454771946427631498462394616623706064561443106503673008210435922340001958432623802886222040403262923652
vkb   = 6568897840127713147382345832798645667110237168011335640630440006583923102503659273104899584827637961921428677335180620421654712000512310008036693022785945317428066257236409339677041133038317088022368203160674699948914222030034711433252914821805540365972835274052062305301998463475108156010447054013166491083
c     = bytes.fromhex('fef29e5ff72f28160027959474fc462e2a9e0b2d84b1508f7bd0e270bc98fac942e1402aa12db6e6a36fb380e7b53323')

# ── Protocol recap ────────────────────────────────────────────────────────────
#  v     = p * r  mod n          (r random  =>  v is a multiple of p mod n)
#  vka   = v  * k_A  mod n
#  vkakb = vka * k_B  mod n      = v * k_A * k_B  mod n
#  vkb   = vkakb * k_A^-1 mod n  = v * k_B  mod n
#  v_s   = vkb * k_B^-1  mod n   = v        (shared secret)
#  key   = SHA256(long_to_bytes(v))

# ── Vulnerability 1: v is a multiple of p ────────────────────────────────────
# v = p*r  =>  gcd(v, n) = p.
# Multiplying by k_i (coprime to n) preserves that:
#   gcd(vka, n) = gcd(v*k_A, n) = p   (since gcd(k_A, n) = 1 by construction)
# So p leaks directly from any of the three published values.

assert gcd(vka, n) == p,   "unexpected: gcd(vka,n) != p"
assert gcd(vkakb, n) == p, "unexpected: gcd(vkakb,n) != p"
assert gcd(vkb, n) == p,   "unexpected: gcd(vkb,n) != p"
print("[+] p confirmed via gcd(vka, n)")

# ── Vulnerability 2: recover v with CRT ──────────────────────────────────────
# Note: vka * vkb = v^2 * k_A * k_B  and  vkakb = v * k_A * k_B  mod n
# So:  vka * vkb / vkakb = v  mod n  -- but vkakb is not invertible mod n (gcd = p).
#
# Fix: work mod q (where gcd(vkakb, q) = 1):
#   v mod q  =  vka * vkb * inverse(vkakb, q)  mod q
#
# We also know v mod p = 0  (since v = p*r).
# CRT reconstruction:
#   v = p * inverse(p, q) * (v mod q)  mod n

v_mod_q = vka * vkb % q * inverse(vkakb, q) % q
v       = p * inverse(p, q) * v_mod_q % n

assert v % p == 0, "v is not a multiple of p — something went wrong"
print("[+] v recovered via CRT (v ≡ 0 mod p,  v ≡ vka*vkb/vkakb mod q)")

# ── Decrypt ───────────────────────────────────────────────────────────────────
key  = sha256(long_to_bytes(v)).digest()
flag = unpad(AES.new(key, AES.MODE_ECB).decrypt(c), 16)
print(f"\n[+] FLAG: {flag.decode()}")