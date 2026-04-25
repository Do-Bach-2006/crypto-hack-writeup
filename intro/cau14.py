import hashlib
import requests
from Crypto.PublicKey import RSA

pem = open('transparency_afff0345c6f99bf80eab5895458d8eab.pem', 'r').read()
key = RSA.importKey(pem).public_key()

der = key.exportKey(format='DER')
sha256 = hashlib.sha256(der)
sha256_fingerprint = sha256.hexdigest()

print(f"Public Key SHA256: {sha256_fingerprint}")

# Query crt.sh
out = requests.get(f"https://crt.sh/?spkisha256={sha256_fingerprint}&output=json")
print("crt.sh response status:", out.status_code)
try:
    data = out.json()
    for cert in data:
        name_value = cert.get('name_value', '')
        print("Subdomain found:", name_value)
        # Try fetching the URL
        if "cryptohack.org" in name_value:
            for domain in name_value.split('\n'):
                if "cryptohack.org" in domain:
                    url = f"https://{domain}"
                    print(f"Visiting {url} ...")
                    try:
                        res = requests.get(url)
                        print("Response:", res.text)
                    except Exception as e:
                        print("Failed to visit:", e)
                    break
except Exception as e:
    print("Error parsing JSON:", e)
