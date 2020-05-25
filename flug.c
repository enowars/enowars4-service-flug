#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char mystrcmp(char str1[], char str2[]){
    int len=strlen(str1)+1;
    
    printf("len: %d\n", len);
    for (int i=0; i<len; i++){
        if (str1[i]!=str2[i]){
            printf("zadnji char %c\n", str1[i]);
            return str1[i];
        }
    }
    
    return 0;
}

int main2() {
    char str1[]="ENOWARS";
    char str2[]="ENOWARS";
    char zero[]="";
    
    printf("str1: %s\n", str1);
    printf("str2: %s\n", str2);
    
    char S=mystrcmp(zero,str2);
    
    if (!mystrcmp(str1,str2)){
        printf("ENAKA\n");
    } else {
        
        printf("DRUGAČNA\n");
    }
    
    printf("izhod je %d\n", S);
    
    return 0;
}


int check_user(char username[], char password[]){
    FILE* fptr=fopen("database.dtb", "r");
	char username2[1000];
	char password2[1000];
	puts("ha");
	while(fscanf(fptr,"%s%s", username2, password2)){
		printf("DEBUG: cekiram %s\n", username2);
		if(!strcmp(username, username2)){
			puts("you could log in but it is not implemented");
			break;
		}
	}
	
	fclose(fptr);
}

int login(){
    char username[1000];
    char password[1000];
    
    puts("Please input your username");
    scanf("%s\n", username);
    puts("Please input password");
    scanf("%s\n", password);
    
    check_user(username, password);
    
    return 0;
}

int sanitize(char input[]){
	
	return -1;
}

int register_user(){
	char new_user[1000];
	char new_password[1000];
	
	puts("Please input your username");
    scanf("%s\n", new_user);
    puts("Please input password");
    scanf("%s\n", new_password);
	
	//sanitize(new_user);
	//sanitize(new_password);

	FILE* fptr=fopen("database.dtb", "a");
	fprintf(fptr, "%s %s\n", new_user, new_password);
	fclose(fptr);
}


int main() {
    char buff[1000];
    
    puts("Welcome to the airport");
    puts("=========================");
    puts("How can we help you today?");
    puts("Press L if you want to login");
	puts("Press R to register");
    
    scanf("%s", buff);
    
    if(buff[0] == 'L'){
        login();
        
    } else if(buff[0] == 'R') {
		register_user();

	} else {
        puts("ok bye");
        
    }
    
    return 0;
}





























