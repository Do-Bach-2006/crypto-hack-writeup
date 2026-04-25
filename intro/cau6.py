text = "label"
key = 13
new_string = ""

for char in text:
   
    new_string += chr(ord(char) ^ key)

print(f"crypto{{{new_string}}}")