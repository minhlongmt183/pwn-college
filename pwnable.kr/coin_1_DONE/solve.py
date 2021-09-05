# gửi lên pwnabler.kr server và run với lệnh python2 solve.py
# flag: b1NaRy_S34rch1nG_1s_3asy_p3asy

from pwn import *

c = remote(0 , 9007)

c.recvuntil(b'- Ready? starting in 3 sec... -')
count_num = 0
while count_num < 100:
    # print("count_num = {}".format(count_num))
    c.recvuntil(b'N=')

    l = c.recv().decode('utf-8').split(' ')


    N = int(l[0])
    C = int(l[1][2:-1])

    array = list(range(N))

    l = 0
    r = N 


    while C > 0:
        mid = l + (r - l) // 2
        num = mid - l

        # print("C = {}".format(C))
        # print("l: {} - mid: {} - r: {}".format(l, mid, r))
        # print("num: {}\n\n".format(num))

        inp1 = ''.join(str(i) + ' ' for i in array[l:mid])
        inp1 = inp1[:-1]

        # print("[+] sendline {}".format(inp1))
        c.sendline(inp1.encode())
        C -= 1

        # print("[+] recvline")
        recv_line = c.recv()
        # print(recv_line)
        total = int(recv_line.decode('utf-8')[:-1])
        if total < num * 10:
            r = mid
        else:
            l = mid

    if mid > l:
        inp1 = str(array[l])
    else:
        inp1 = str(array[mid])

    c.sendline(inp1.encode())
    print c.recvline()
    count_num += 1

    
print(c.recv())
c.interactive()

 