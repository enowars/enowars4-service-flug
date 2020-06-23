# enowars4-service-flug

Service by
* Urban Suhadolnik (Lightning5)
* Aleksander Mundjar(Aleks, NOx)


## The concept

The idea is that this is a flight booking sistem. User logs in the system and buys a flight for flight and gets a ticket. The inspiration that the first flight tcket booking system gave your a bar code that's actually a pointer on the mainframe itself.
We implementing 3 vulnarabilities:

* Simple strcmp bug when logging in
* Stack reuse vulnarability
* Floating filepointer(the pointer in the mainframe)


## Vuln 1 strcmp
Our own costumn implementation of string.h library. The Library is custom and not compilient with string.h. With this we force the teams to actually fix functions handling strings.

* Buggeg strcmp implementation
* strcmp that returns the last character (It's a feature)


###### Exploit:
Insert string of size zero or a just nsert string with first character as null character ('\0'). (which is actually the same accroding to C standard)

```
    char mystrcmp(char str1[], char str2[]){
        int len=strlen(str1)+1;

        printf("len: %d\n", len);
        for (int i=0; i<len; i++){
            if (str1[i]!=str2[i]){
                p
                return str1[i];
            }
        }

        return 0;
    }
```

    int main(){
        if (mystrcmp(str1, str2)){
            login();
        }
    }
    
## vuln 2 - Stack reuse

Two consecutive functions always use the same stack. If a second function has uninitialsed variables it might happen that some variable value might find itself in an uninitilased varible.

In the first function(login) we load the whole user everytime someone want's to login (we need to check if user exists and their password). Login fails. Function ends. But! Their password stays in freed memory.
The second function has it's stack aligned with the first. Ticket ID can be leaked through one of the uninitialised variables of the second function.
Leaked ticket ID can be used to open a ticket and retrieve tha flag.


## vuln 3 (still just a concept)

Something similar to vuln 2 but a floating file deskrictor.

## Storing users and tickets
For users and tickets we have two folders: users and tickets. All information is stored as files in these two directories.

### ./users
Every user has it's own file with username and password in the first line. In each of all the other lines there is one ticket ID that this user owns.

    <user> <password>
    1 <ticketID_1>
    2 <ticketID_2>
    
    
Is there a better way to store usernames and passwords?

### ./tickets

Every ticket is it's own file in directory ./tickets. Name of the file is `ticketID` inside of the ticket all of the flight information and a FLAG
    
    <origin airport>
    <destination airport>
    <flight number>
    <ticket_text == flag>
    
#### ?
Should we hash passwords so players don't leak their own passwords(yeah people are that stupid)

## serving the service

This a simple c service. The binary served as a server with `socat`.
`socat TCP-LISTEN:7478,nodelay,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./a.out"`

Service is served on TCP port 7478.


## checker (time of writing: 23.6.2020)
- checkser is using pwntools to comunicate with the services.

### Generating username and password code snippet
- Username and password are 25 characters long and contain only lowercase ascii.
```
    def gen_user(self): 
        source = list(string.ascii_lowercase)
        username =''
        for num in range(25):
            rand_int = randrange(25)
            username += source[rand_int]
        return username

    def gen_password(self): 
        source = list(string.ascii_lowercase)
        password =''
        for num in range(25):
            rand_int = randrange(25)
            password += source[rand_int]
        return password
```

### putflag
- Generates random username and random password

- Checks if it can connect to the service, if not it raises the enochecker OfflineException;

```        
        try:
            print('Connecting ...')
            p = remote(self.address,port)
            print("Connection succeded")
        except:
            raise OfflineException("Unable to connect to the service [putflag]")
```
- Registers a user with the newly created credentials
- Logs in with that user
- Creates a new ticket which contains the flag
- It uses the mogodb to fetch the flags.
- Stores the ticket id into mongodb so that getflag can use it.
- If the Creation of user, Registration or Creation of ticket fails the checker raises the BrokenServiceException with the appropriate message for example: Put flag failed [putflag].

- After Registering the user and Logging in, checker stores the credentials in instance of mongodb for further use.



### getflag

- Checks if it can connect to the service, if not it raises the enochecker OfflineException
- Checks if the flag is where the most recent putflag function call put it(using the ticket id the putflag stored in the mongodb), to determin if the flags are a match it uses the mongodb where the most recent flag is stored. If flags don't match the putflag raises the enochecker BrokenServiceException


### putnoise

- Follows exact steps the putflag does but it puts in noise instead of flag.

### getnoise
- Follows exact steps the getflag does but it retrieves and checks the noise instead of flag.

### havoc

- Havoc calls getnoise and putnoise to check if the logic for puting it flags wors without having to actualy put in flags
- Looks for keywords in the different menues of the service and checks if menues are the same as they were at the beginning of the ctf
- It checks the "landing menu", menu when logged in and the "view ticket menu"


### exploit

- The exploit for the first vulnerability which consists of exploiting the faulty logic in the login function. The more accurate explanation is listed in the 'Vuln 1 strcmp' section.


### socat

- socat runs on every vulnerable machine and it wors so that it starts a new process for every incoming connection and every of that processes starts an instance of the vulnerable binary.
- Actual Command used:
``` 
socat TCP-LISTEN:7478,nodelay,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./a.out"
```
## Still to define and do

* docker (khm khm)
* remote compiling


## Ideas


* Give an airplane ticket through a bar code

