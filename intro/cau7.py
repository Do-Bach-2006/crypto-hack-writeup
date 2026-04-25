from pwn import xor

# Các dữ kiện đề bài cho (dưới dạng hex)
key1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
key2_xor_key3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
flag_xor_all = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

# Chuyển từ hex sang bytes
v1 = bytes.fromhex(key1)
v3 = bytes.fromhex(key2_xor_key3)
v4 = bytes.fromhex(flag_xor_all)

# Thực hiện phép tính: FLAG = v4 ^ v1 ^ v3
# Tính chất XOR cho phép ta XOR liên tiếp nhiều biến
result = xor(v4, v1, v3)

print(f"flag:{result.decode()}")