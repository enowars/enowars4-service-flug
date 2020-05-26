# enowars4-service-flug

Service by
* Urban SUhadolnik (Lightning5)
* Aleks(NOx)


## The concept

TO DO


## Vuln 1

Netcat service


Vuln:

* Buggeg strcmp implementation
* strcmp that returns the last character (It's a feature)


Exploit:
* Insert string of size zero
* Insert string with first character as null character ('\0)

```
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
```

    int main(){
        if (mystrcmp(str1, str2)){
            login();
        
        }
    }
    
## vuln 2

Stack reuse

two consecutive functions would use the same stack => we keak infromation from the first function in the second. (already oriven to work)


## database

    <user1> <password1>
    <user2> <password2>
    
Is there a better way to store usernames and passwords?

Should we hash password so players don't leak their own passwords(yeah people are that stupid)?

Maybe use files


## checker

In progress

## Still to define and do

* socat
* docker (khm khm)
* remote compiling


## Ideas


* Give an airplane ticket through a bar code

