#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <time.h>
#include <fcntl.h>
#include <ctype.h>
#include <dirent.h>
#include <sys/stat.h>
#define BUFF_LEN 200
#define STR_(X)
#define STR(X) STR_(X)
#define MAXDATA 1000
#define llong long long

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
    puts("5: anonymous");
    puts("6: about");
    puts("7: exit");
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

int about(){
    puts("Welcome to service flug made by Urban(Lightning5) and Aleks(NOx)");
    puts("There are two vulnerabilities in the service");
    puts("If there are any questions find us on IRC\n");
    puts("Have fun :)");
    
    sleep(5);
}

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

//TODO sanitize is not used in the right way at line 300
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
    strcpy(new_user_file, "../users/");
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
    d = opendir("../users");
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
    char * path= (char*)malloc(BUFF_LEN+13);

    strcpy(path,"../users/");
    strcat(path,username);

    int lines = count_lines(path);

    if (lines != -1){

        FILE * userfile = fopen(path,"a"); //TODO popravi
        fprintf(userfile,"%d %llu\n",lines,random);
        printf("loaded a new ticket on index %d\n",lines);
        fclose(userfile);

        char * tickets_path = (char*)malloc(BUFF_LEN +13);
        char * stringify_random= (char*)malloc(20);

        sprintf(stringify_random,"%llu",(unsigned long long)random);
        strcpy(tickets_path,"../tickets/");
        strcat(tickets_path,stringify_random);

        FILE * tickets_file = fopen(tickets_path,"w");

        puts("Please input origin airport");
        char origin[96];
        scanf("%80s", origin);
        sanitize(origin);
        puts("Please input destination airport");
        char destination[96];
        scanf("%80s", destination);
        sanitize(destination);
        //potem spremeni v int
        llong fl;
        if(!origin){
            scanf("%lld", &fl);
        }
        puts("Enter the content of your new ticket");
        char * ticket_text=(char*)malloc(201); //ticket onformation
        getc(stdin); //flush stdin so we can use fgets insted of scanf since scanf cant take in spaces.
        fgets(ticket_text,200,stdin);
        fprintf(tickets_file,"%s\n%s\n%llu\n%s\n",origin,destination,fl,ticket_text);
        fclose(tickets_file);
        printf("\nYour new ticket ID is:\n%llu", random);
        fflush(stdin);
        free(path);
        free(tickets_path);
        free(stringify_random);
        free(ticket_text);
    }else{
        return 0;
    }
}

int view_ticket(){

    char id[20];
    puts("Enter the unique id of your ticket");
    scanf("%20s",id);

    char path[40];
    strcpy(path,"../tickets/");
    strcat(path,id);

    FILE * ticket = fopen(path,"r");
    if (ticket == NULL){
        puts("That is not a valid id");
        return 1;
    }

    char data[MAXDATA];
    puts("The contents of your ticket:");

    while (fgets(data, MAXDATA, ticket) != NULL){
        
        printf("%s", data); //TODO make it nice later
    }

    fclose(ticket);
}

int check_anon_user(){
    if( access( "../users/Anonymous", F_OK ) != -1 ) {
        // user exists
        return 0;
    } else {
        // file doesn't exist
        unsigned llong random = random_64_bit();
        char stringify_random[20];
        sprintf(stringify_random,"%llu",(unsigned long long)random);

        FILE* userfile=fopen("../users/Anonymous", "w");
        fprintf(userfile, "%s %s\n", "Anonymous", stringify_random);
        fclose(userfile);
        return -1;
    }
    
}

int view_my_tickets(char username[]){
    char path[BUFF_LEN + 14];
    strcpy(path,"../users/");
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

int logged_in(char username[]){
//TODO meybi v svojo funkcijo
    char Input[8];
    
    while (1){
        print_menu2(username);
        if(!scanf("%3s",Input)){
            exit(-1);
        }

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
            printf("%s",Input);

        }

    }
    
}

int login(){
    llong ticket; //TODO hide for CTF

    char * username_put_in = (char *)malloc(BUFF_LEN + 1);
    char * password_put_in =  (char *)malloc(BUFF_LEN + 1);
    //https://www.youtube.com/watch?v=t-wFKNy0MZQ
    
    char * username= (char *)malloc(BUFF_LEN + 1);
    char password[BUFF_LEN+1];
//    char * password= (char *)malloc(BUFF_LEN + 1);
    

    puts("Please input your username:");
    scanf("%" STR(BUFF_LEN) "s", username_put_in);
    puts("Please input your password:");
    scanf("%" STR(BUFF_LEN) "s", password_put_in);
    
    if(!sanitize(username_put_in) || !sanitize(password_put_in)){
        exit(0);
    }
    
    char *  user_file_path= (char*)calloc(BUFF_LEN + 13,sizeof(char));
    strcpy(user_file_path, "../users/");
    strcat(user_file_path, username_put_in);
    
    
    FILE* fptr=fopen(user_file_path, "r");
    if(!fptr){
        puts("username does not exist");
        
        return -1;
    }
    
    fscanf(fptr, "%s %s %*d %llu", username, password, &ticket);
    
    if(strcmp(password_put_in, password)){
        puts("password is wrong");
        return -1;
    }
    //TODO: nov meni za add ticket
    //TODO: while loop za logiko ko si loged in idk.
    puts("password is ok");
    
    logged_in(username);
    //freeda je bila moja kraljica
    //https://www.youtube.com/watch?v=52d_JutxYLA
    //https://www.youtube.com/watch?v=k14Ybe4lTHw
    free(username);
    free(username_put_in);
    free(password_put_in);
    free(user_file_path);
    
    fclose(fptr);
}

int initdb(){
    //check and create user db
    DIR* dir = opendir("../users/");
    if (!dir) {
 //no folder
        mkdir("../users/", 0777);
    } else {
        closedir(dir);
    }
    
    dir = opendir("../tickets/");
    if (!dir) {
 //no folder
        mkdir("../tickets/", 0777);
    } else {
        closedir(dir);
    }
    
}

int main(){
    initdb();
    char S[8];
    alarm(20);
    
    while(1){
        print_menu1();
        if (!scanf("%3s", S)){
            exit(-1);
        }

        if(S[0] == '1'){ //login
            login();

        } else if(S[0] == '2'){ //register
            register_user();

        } else if(S[0] == '3'){
            view_ticket();

        } else if(S[0] == '4'){
            list_users();

        } else if(S[0] == '7'){
            puts("Bye");
            exit(0);
        } else if(S[0] == '5'){
            check_anon_user();
            add_ticket("Anonymous");
        } else if(S[0] == '6') {
            about();
        } else {
            puts("choose again");
            
        }
        sleep(0.5);
        puts("\n");
        
    }   
	return 0;
}
