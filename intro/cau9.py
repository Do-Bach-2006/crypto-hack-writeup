from pwn import xor

hex_data = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
data = bytes.fromhex(hex_data)

key = b"myXORkey"

flag = xor(data, key)
print("Flag:", flag.decode())
