#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#define BUFF_LEN 200
#define STR_(X)
#define STR(X) STR_(X)


char mystrcmp(char str1[], char str2[]){
    int len=strlen(str1)+1;
    
    printf("we got: %s\n and: %s", str1, str2);
    
    printf("len: %d\n", len);
    for (int i=0; i<len; i++){
        if (str1[i]!=str2[i]){
            printf("zadnji char %c\n", str1[i]);
            return str1[i];
        }
    }
    
    return 0;
}


int register_user(){
	char new_username[BUFF_LEN + 1];
    char new_password[BUFF_LEN + 1];
    
    puts("Please input your new username:");
    scanf("%" STR(BUFF_LEN) "s", new_username);
    puts("Please input your password:");
    scanf("%" STR(BUFF_LEN) "s", new_password);
    
    char new_user_file[BUFF_LEN + 7];
    strcpy(new_user_file, "users/");
    strcat(new_user_file, new_username);
    
    //prevert mormo če user že obstaja
    
    FILE* userfile=fopen(new_user_file, "w");
    fprintf(userfile, "%s %s\n", new_username, new_password);
    
    fclose(userfile);
}


long random_64_bit(){
    srand(time(NULL));
    uint64_t random_num = (((uint64_t) rand() <<  0) & 0x00000000FFFFFFFFull) | (((uint64_t) rand() << 32) & 0xFFFFFFFF00000000ull);
    return random_num;
}

int count_lines(char path[]){
    FILE * fp = fopen(path, "r"); 
    int count = 0;
    char c;

    if (fp == NULL) { 
        puts("Sorry, this user doesn't exist"); 
        fclose(fp);
        return -1; 
    } 
  
    for (c = getc(fp); c != EOF; c = getc(fp)) {
        if (c == '\n')  
            count = count + 1; 
    }
    fclose(fp); 
    return count; 
}

int add_ticket(){
    uint64_t random = random_64_bit();
    char username[BUFF_LEN +1];
    char path[BUFF_LEN+7];


    puts("please enter your username:");
    scanf("%" STR(BUFF_LEN) "s", username);
    // preveri ce login, URABN NARED LOGIN
    strcpy(path,"users/");
    strcat(path,username);
    int lines = count_lines(path);

    if (lines != -1){
        FILE * userfile = fopen(path,"a+");
        fprintf(userfile,"%d %ld\n",lines,random);
        printf("loaded a new ticket on index %d",lines);
        fclose(userfile);

        char tickets_path[BUFF_LEN +7];
        char stringify_random[20];

        sprintf(stringify_random,"%ld",(uint64_t)random);
        strcpy(tickets_path,"tickets/");
        strcat(tickets_path,stringify_random);

        FILE * tickets_file = fopen(tickets_path,"w");
        //urban bo pisal not kar bo hotu
        char test[]="test";
        char test2[]="testing";

        fprintf(tickets_file,"%s %s\n",test,test2);
        fclose(tickets_file);
    }else{
        return 0;
    }
}

int view_ticket(){
    char username[BUFF_LEN +1];
    char path[BUFF_LEN+7];
    int id;
    char ticket[20];
    int index;
   
    puts("please enter your username:");
    scanf("%" STR(BUFF_LEN) "s", username);
    puts("please enter the index:");
    scanf("%3s",&index);
    //preverimo ce je logged in kot ta user

}

int login(){
    char username_put_in[BUFF_LEN + 1];
    char password_put_in[BUFF_LEN + 1];
    char username[BUFF_LEN + 1];
    char password[BUFF_LEN + 1];
    
    
    puts("Please input your username:");
    scanf("%" STR(BUFF_LEN) "s", username_put_in);
    puts("Please input your password:");
    scanf("%" STR(BUFF_LEN) "s", password_put_in);
    
    char user_file_path[BUFF_LEN + 7];
    strcpy(user_file_path, "users/");
    strcat(user_file_path, username_put_in);
    
    printf("%s\n",user_file_path);
    
    FILE* fptr=fopen(user_file_path, "r");
    if(!fptr){
        puts("username does not exist");
        
        return -1;
    }
    
    
    fscanf(fptr, "%s %s", username, password);
    
    printf("dtb_user: %s\n dtb_password: %s\n",username,password);
    
    
    if(!mystrcmp(password_put_in, password)){
        puts("password is ok");
        puts("you could log in but it is not implemented");
    } else {
        puts("password is wrong");
        
    }
    
    fclose(fptr);
}

int print_menu1(){
    puts("Welcome to the airport");
    puts("======================");
    puts("How can we help you today?");
    puts("The menu");
    puts("================");
	puts("1: login");
    puts("2: register");
    puts("3: add ticket");
    puts("4: view ticket");
    puts("5: exit");
    puts("================");
    
    
}


int main(){
    char S[8];
    
    
    while(1){
        print_menu1();
        scanf("%3s", S);
        if(S[0] == '1'){ //login
            login();
            
        } else if(S[0] == '2'){ //register
            register_user();
            
        }else if(S[0] == '3'){
            add_ticket();
        } else if(S[0] == '4'){
            puts("your could view a ticket here but it is not implemented");
            
        } else if(S[0] == '4'){
            puts("Bye");
            exit(0);
        } else {
            puts("chose again");
            
        }
        sleep(0.5);
        puts("\n\n");
        
    }
        
	return 0;
}
