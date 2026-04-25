from Crypto.PublicKey import RSA

# Chuỗi key của Bruce (bạn copy nguyên dòng từ đề bài vào đây)
with open("bruce_rsa_6e7ecd53b443a97013397b1a1ea30e14.pub" , "r") as f:
    ssh_key_string = f.read()

# Import trực tiếp
key = RSA.importKey(ssh_key_string)

# Trích xuất Modulus n
print(f"Modulus n (Decimal): {key.n}")