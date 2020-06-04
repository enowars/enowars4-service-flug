#!/usr/bin/env python3
#socat TCP-LISTEN:1337,nodelay,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./a.out"
from pwn import *
import sys
import time
from enochecker import *
import string
from random import randrange

class Flug_Checker(BaseChecker):

    def __init__(self,username,password):
        self.username = gen_user()
        self.password = gen_password()
        self.ticket_id
        self.noise_id

    flag_count = 1
    noise_count = 1
    havoc_count = 1
    port = 1337
    def gen_user():
        source = list(string.ascii_lowercase)
        username =''
        for num in range(25):
            rand_int = randrange(25)
            username += source[rand_int]
        return username

    def gen_password():
        source = list(string.ascii_lowercase)
        password =''
        for num in range(25):
            rand_int = randrange(25)
            password += source[rand_int]
        return password



    def putflag(self):  # type: () -> None
        try:
            p = remote(self.address,port)
        except:
             raise enochecker.OfflineException
             logger.debug("Connection to the service failed")
        try:
            p.recvuntil("================\n")
            p.sendlineafter("================\n","2")
            p.sendlineafter("Please input your new username:\n",str(self.username))
            p.sendlineafter("Please input your password:\n",str(self.password))
            p.recvuntil("================\n")
            p.sendlineafter("================\n","1")
            p.sendlineafter("Please input your username:\n",str(self.username))
            p.sendlineafter("Please input your password:\n",str(self.password))
            p.recvuntil("================\n")   
            p.sendlineafter("================\n","1")
            time.sleep(.1)
            p.recvuntil("Enter the content of your new ticket\n")
            p.send(str(self.flag))
            time.sleep(.1)
            p.recvuntil("================\n")
            p.sendlineafter("================\n","2")
            stdo = p.recvline()
            self.ticket_id = p.recvline().split(' ')[1]

            flag_count +=1
        except:
            raise enochecker.BrokenServiceException("putflag failed")

    def getflag(self):  # type: () -> None
        try:
            p = remote(self.address,port)
        except:
             raise enochecker.OfflineException
             logger.debug("Connection to the service failed")

        try:
            p.recvuntil("================\n")
            p.sendlineafter("================\n","3")
            p.sendlineafter("Enter the unique id of your ticket",str(self.ticket_id))
            p.recvline()
            flag2 = p.recvline() 
            if flag2 != self.flag:
                raise enochecker.BrokenServiceException("Service mumbels")

        except:
            raise enochecker.BrokenServiceException("getflag failed")

        if self.flag_idx == 0:
            if not self.team_db.get(sha256ify(self.flag), None) == self.flag:
                raise BrokenServiceException("We did not get flag 0 back :/")
        elif self.flag_idx == 1:
            if (
                not self.global_db.get("{}_{}".format(self.address, self.flag), None)
                == "Different place for "
                "different flag_idx"
            ):
                raise BrokenServiceException("Flag 2 was missing. Service is broken.")
        else:
            raise ValueError(
                "Call_idx {} not supported!".format(self.flag_idx)
            )  # Internal error.

    def putnoise(self):  # type: () -> None

        try:
            p = remote(self.address,port)
        except:
             raise enochecker.OfflineException
             logger.debug("Connection to the service failed")
        try:
            p.recvuntil("================\n")
            p.sendlineafter("================\n","2")
            p.sendlineafter("Please input your new username:\n",str(self.username))
            p.sendlineafter("Please input your password:\n",str(self.password))
            p.recvuntil("================\n")
            p.sendlineafter("================\n","1")
            p.sendlineafter("Please input your username:\n",str(self.username))
            p.sendlineafter("Please input your password:\n",str(self.password))
            p.recvuntil("================\n")   
            p.sendlineafter("================\n","1")
            time.sleep(.1)
            p.recvuntil("Enter the content of your new ticket\n")
            p.send(str(self.noise))
            time.sleep(.1)
            p.recvuntil("================\n")
            p.sendlineafter("================\n","2")
            stdo = p.recvline()
            self.noise_id = p.recvline().split(' ')[1]

        except:
            raise enochecker.BrokenServiceException("putnoise failed")


        self.team_db["noise"] = self.noise

    def getnoise(self):  # type: () -> None
        try:
            p = remote(self.address,port)
        except:
             raise enochecker.OfflineException
             logger.debug("Connection to the service failed")

        p.recvuntil("================\n")
        p.sendlineafter("================\n","3")
        p.sendlineafter("Enter the unique id of your ticket",str(self.ticket_id))
        p.recvline()
        noise2 = p.recvline()        
        if noise2 != self.noise:
            raise enochecker.BrokenServiceException('Service mumbles')
        """
        This method retrieves noise in the service.
        The noise to be retrieved is inside self.flag
        The difference between noise and flag is, tht noise does not have to remain secret for other teams.
        This method can be called many times per round. Check how often using flag_idx.
        On error, raise an EnoException.
        :raises EnoException on error
        :return this function can return a result if it wants
                if nothing is returned, the service status is considered okay.
                the preferred way to report errors in the service is by raising an appropriate enoexception
        """
        try:
            assert_equals(self.team_db["noise"], self.noise)
        except KeyError:
            raise BrokenServiceException("Noise not found!")

    def havoc(self):  # type: () -> None
        """
        This method unleashes havoc on the app -> Do whatever you must to prove the service still works. Or not.
        On error, raise an EnoException.
        :raises EnoException on Error
        :return This function can return a result if it wants
                If nothing is returned, the service status is considered okay.
                The preferred way to report Errors in the service is by raising an appropriate EnoException
        """
        self.info("I wanted to inform you: I'm  running <3")
        self.http_get(
            "/"
        )  # This will probably fail, depending on what params you give the script. :)

    def exploit(self):
        #1st vuln
        p = remote(self.address,port)
        p.recvuntil("================\n")
        p.sendlineafter("================\n",'1')
        p.sendlineafter("Please input your username:\n",str(username))
        p.sendlineafter("Please input your password:\n",'\x00')
        p.recvline() #TODO: odstrani ko urban popravi svoje randomly placed printfe
        p.recv(2) 
        check_line = p.recvline()
        if username in check_line:
            print "you got pwnd"
        else:
            print "Sad NOX"
        pass


app = ExampleChecker.service  # This can be used for uswgi.
if __name__ == "__main__":
    run(Flug_Checker)
    # Example params could be: [StoreFlag localhost ENOFLAG 1 ENOFLAG 50 1]
    # exit(ExampleChecker(port=1337).run())


