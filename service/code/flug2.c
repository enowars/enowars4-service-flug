#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <time.h>
#include <fcntl.h>
#include <ctype.h>
#include <dirent.h>
#define BUFF_LEN 200
#define STR_(X)
#define STR(X) STR_(X)
#define MAXDATA 1000
#define llong long long

int strlen(char str[]){
    int i=0;
    while(str[i] != '\0'){
        i++;
    }
    
    return i;
}

char strcmp(char str1[], char str2[]){
    int len=strlen(str1)+1;
    
    for (int i=0; i<len; i++){
        if (str1[i]!=str2[i]){
            return str1[i];
        }
    }
    
    return 0;
}

int strcpy(char str1[], char str2[]){
    int i=0;
    while(str2[i] != '\0'){
        str1[i]=str2[i];
        i++;
    }
    str1[i]='\0';
    
    return 0;
}

int strcat(char str1[], char str2[]){
    while(*str1 != '\0'){
        str1++;
    }
    int i=0;
    while(str2[i] != '\0'){
        str1[i]=str2[i];
        i++;
    }
    str1[i]='\0';
    
    return 0;
}

int sanitize(char* str1){
    int len1=strlen(str1)+1;
    char* str2= (char *)malloc(len1);
    
    int i2=0;
    for(int i1=0; i1<len1; i1++){
        if(!isspace(str1[i1])){
            str2[i2]=str1[i1];
            i2++;
        }
    }
    
    strcpy(str1, str2);
    
    return -1;
}

int register_user(){
	char new_username[BUFF_LEN + 1];
    char new_password[BUFF_LEN + 1];
    
    puts("Please input your new username:");
    scanf("%" STR(BUFF_LEN) "s", new_username);
    puts("Please input your password:");
    scanf("%" STR(BUFF_LEN) "s", new_password);

    int is_file_here;

    char new_user_file[BUFF_LEN + 13];
    strcpy(new_user_file, "../../users/");
    strcat(new_user_file, new_username);

    is_file_here = access(new_user_file, F_OK);

    if(is_file_here == 0){
        puts("User already exists");
        return -1;
    }
    FILE* userfile=fopen(new_user_file, "w");
    fprintf(userfile, "%s %s\n", new_username, new_password);
    fclose(userfile);
}


unsigned long long random_64_bit(){
    int fd;
    unsigned llong  rand;
    
    fd = open("/dev/urandom", O_RDONLY);
    read(fd, &rand, sizeof(unsigned long long));
    close(fd);
    
    return rand;
}

int count_lines(char path[]){
    FILE * fp = fopen(path, "r"); 
    int count = 0;
    char c;

    if (fp == NULL) { 
        puts("Sorry, this user doesn't exist"); 
        return -1; 
    } 

    for (c = getc(fp); c != EOF; c = getc(fp)) {
        if (c == '\n')  
            count = count + 1; 
    }

    fclose(fp);
    return count; 
}

int list_users(){
    DIR *d;
    struct dirent *dir;
    d = opendir("../../users");
    if (d){
        while ((dir = readdir(d)) != NULL){
            if(!strcmp(dir->d_name,".") || !strcmp(dir->d_name,"..")){
                continue;
            }
            printf("%s\n", dir->d_name);

        }
        closedir(d);
    }
    return(0);    
}


int add_ticket(char username[]){
    unsigned long long  random = random_64_bit();
    char path[BUFF_LEN+13];

    strcpy(path,"../../users/");
    strcat(path,username);

    int lines = count_lines(path);

    if (lines != -1){

        FILE * userfile = fopen(path,"a+");

        fprintf(userfile,"%d %llu\n",lines,random);
        printf("loaded a new ticket on index %d\n",lines);
        fclose(userfile);

        char tickets_path[BUFF_LEN +13];
        char stringify_random[20];

        sprintf(stringify_random,"%llu",(unsigned long long)random);
        strcpy(tickets_path,"../../tickets/");
        strcat(tickets_path,stringify_random);

        FILE * tickets_file = fopen(tickets_path,"w");
        char ticket_text[201]; 

        puts("Enter the content of your new ticket");
        getc(stdin); //flush stdin so we can use fgets insted of scanf since scanf cant take in spaces.
        fgets(ticket_text,200,stdin);
        fprintf(tickets_file,"%s\n",ticket_text);
        fclose(tickets_file);

    }else{
        return 0;
    }
}

int view_ticket(){

    char id[20];
    puts("Enter the unique id of your ticket");
    scanf("%20s",id);

    char path[40];
    strcpy(path,"../../tickets/");
    strcat(path,id);

    FILE * ticket = fopen(path,"r");
    if (ticket == NULL){
        puts("That is not a valid id");
        return 1;
    }

    char data[MAXDATA];
    puts("The contents of your ticket:");

    while (fgets(data, MAXDATA, ticket) != NULL){
        
        printf("%s", data);
    }

    fclose(ticket);
}


int print_menu1(){
    puts("Welcome to the airport");
    puts("======================");
    puts("How can we help you today?");
    puts("The menu");
    puts("================");
	puts("1: login");
    puts("2: register");
    puts("3: view ticket");
    puts("4: view flight bookings");
    puts("5: exit");
    puts("================");
    
}


int print_menu2(char usename[]){
    puts("\n");
    printf("welcome %s\n",usename);
    puts("The menu");
    puts("================");
    puts("1: buy ticket");
    puts("2: view my tickets");
    puts("3: view ticket");
    puts("4: logout");
    puts("================");

}


int view_my_tickets(char username[]){
    char path[BUFF_LEN + 14];
    strcpy(path,"../../users/");
    strcat(path,username);
    FILE * tickets = fopen(path,"r");

    if(tickets == NULL){
        puts("something went really wrong! This should not happen");
        return 1;
    }

    char data[MAXDATA];
    while (fgets(data, MAXDATA, tickets) != NULL){
        printf("%s", data);
    }

    fclose(tickets); 
}


int login(){
    char username_put_in[BUFF_LEN + 1];
    char password_put_in[BUFF_LEN + 1];
    //https://www.youtube.com/watch?v=t-wFKNy0MZQ
    char username[BUFF_LEN + 1];
    char password[BUFF_LEN + 1];
    
    
    puts("Please input your username:");
    scanf("%" STR(BUFF_LEN) "s", username_put_in);
    puts("Please input your password:");
    scanf("%" STR(BUFF_LEN) "s", password_put_in);
    
    if(!sanitize(username_put_in) || !sanitize(password_put_in)){
        exit(0);
    }
    
    char user_file_path[BUFF_LEN + 13];
    strcpy(user_file_path, "../../users/");
    strcat(user_file_path, username_put_in);
    
    
    FILE* fptr=fopen(user_file_path, "r");
    if(!fptr){
        puts("username does not exist");
        
        return -1;
    }
    
    fscanf(fptr, "%s %s", username, password);
    
    if(strcmp(password_put_in, password)){
        puts("password is wrong");
        return -1;
    }
    //TODO: nov meni za add ticket
    //TODO: while loop za logiko ko si loged in idk.
    
    //TODO meybi v svojo funkcijo
    char Input[8];
    while (1){
        print_menu2(username);
        scanf("%3s",Input);

        if(Input[0] == '1'){
            add_ticket(username);

        }else if(Input[0] == '2'){
            view_my_tickets(username);

        }else if(Input[0] == '3'){
            view_ticket();

        }else if(Input[0] == '4'){
            return 0;

        }else{
            puts("Invalid option try again");

        }

    }
    
    puts("password is ok");
    puts("you could log in but it is not implemented");
    
    fclose(fptr);
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

        } else if(S[0] == '3'){
            view_ticket();

        } else if(S[0] == '4'){
            list_users();

        } else if(S[0] == '5'){
            puts("Bye");
            exit(0);

        } else {
            puts("choose again");
            
        }
        sleep(0.5);
        puts("\n");
        
    }   
	return 0;
}
