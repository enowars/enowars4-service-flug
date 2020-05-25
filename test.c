#include <stdio.h>

int fun1() {

    char str1[]="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    char str2[]="flag";


	return 0;
}

int fun2() {
    
    int a=0;
    int b=0;
    char str[16];
    int c=0;
    
    //str="XXXXXXXXflag";
    scanf("%s[16]", str);
    // str = "AAAAAAAA_______"
    
    printf("%s[16]", str);
    // str= "AAAAAAAAflag"
    
    puts("Hello");
    
    return 0;
}

int fun3() {
    char str1[]="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
    char str2[4];
    
    printf("%s\n", str2);
    
    return 0;
}


int main(){
    //FILE* fptr=fopen("database.dtb", "r");
    
    //char buff[1000];
    
    //fscanf(fptr, "{%s}", buff);
    
    //printf("%s\n", buff);
    
    
    fun1();
    fun3();
    
    
}
