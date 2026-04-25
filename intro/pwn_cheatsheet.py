from pwn import *

# ==============================================================
# PWNTOOLS AND GDB CHEATSHEET
# ==============================================================

# --- 1. Exploit Context Configuration ---
# Set architecture and OS context (vital for shellcraft and alignment)
context.update(arch='i386', os='linux')
# Shorthand for 64-bit binaries:
context.arch = 'amd64'

# --- 2. Connections ---
# Start a local process
p = process('./vuln_binary')

# Connect to a remote service via netcat
r = remote('192.168.1.10', 1337)

# Connect to a process through SSH
# s = ssh(host='10.10.10.10', user='ctf', password='password')
# p = s.process('./vuln_binary')

# --- 3. GDB Integration (Debugging) ---
# Attach GDB to a running process dynamically
# (Often requires a terminal multiplexer like tmux context.terminal=['tmux', 'splitw', '-h'])
# This allows you to set breakpoints before continuing.
gdb.attach(p, '''
    b main
    c
''')

# You can also start the process inside GDB directly
# p = gdb.debug('./vuln_binary', 'b main\nc\n')

# --- 4. Sending and Receiving Data ---
# Receive exactly n bytes
data = p.recv(1024)

# Receive until a specific string is found (e.g., prompt)
msg = p.recvuntil(b"Password: ")

# Send data without a trailing newline
p.send(b"A" * 64)

# Send data with a trailing newline
p.sendline(b"A" * 64)

# Print everything it receives, great for debugging IO
# p.recvall()

# Go to interactive mode (gives you terminal access once shell is popped)
p.interactive()

# --- 5. Data Packing & Unpacking ---
# Pack 32-bit (p32) and 64-bit (p64) little-endian integers into byte strings
payload = p32(0xdeadbeef) + p64(0xcafebabe)

# Unpack 32-bit and 64-bit bytes back to integers (must be exactly 4 or 8 bytes)
value32 = u32(b"ABCD")
value64 = u64(b"ABCDEFGH")

# --- 6. ELF Parsing and ROP ---
# Read symbols, got tables, strings from the binary easily
elf = ELF('./vuln_binary')

# Automatically get the address of a function (e.g., 'win' function)
win_addr = elf.symbols['win']

# Using the ROP module to build gadgets (automatically finds gadgets)
rop = ROP(elf)
rop.call('win', [0xdeadbeef, 0xcafebabe])
# payload += rop.chain()

# Address of libc functions if libc is provided
# libc = ELF('./libc.so.6')
# libc.address = leaked_libc_base
# system_addr = libc.symbols['system']

# --- 7. Writing Shellcode ---
# Generate simple assembly shellcode (arch must be set via context)
shellcode = asm(shellcraft.sh())

# --- 8. Finding Overwrite Offsets (Cyclic Patterns) ---
# Create a 100-byte De Bruijn sequence to send as payload to see where it crashes
pattern = cyclic(100)

# Once it crashes and you see the instruction pointer (EIP/RIP) overwritten 
# by a sequence like 0x6161616a (for example "jaaa"), you can find the offset:
offset = cyclic_find(0x6161616a) # Returns integer index to the buffer
