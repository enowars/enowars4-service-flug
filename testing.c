#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
int main(){
    char buff[201];
    scanf("%200s",buff);
    printf("%s",buff);
}