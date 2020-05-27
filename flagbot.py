#socat TCP-LISTEN:1337,nodelay.reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./a.out"
from pwn import *
import sys
import time
ip = "127.0.0.1"
port = 1337

def add_flag(name,password,flag):
	p = remote(ip,port)
	p.recvuntil("================\n")
	p.sendlineafter("================\n","2")
	p.sendlineafter("Please input your new username:\n",str(name))
	p.sendlineafter("Please input your password:\n",str(password))
	p.recvuntil("================\n")
	p.sendlineafter("================\n","1")
	p.sendlineafter("Please input your username:\n",str(name))
	p.sendlineafter("Please input your password:\n",str(password))
	p.sendlineafter("================\n","1")
	time.sleep(.1)
	print p.recvuntil("Enter the content of your new ticket\n")
	p.send(str(flag))
	time.sleep(.1)


if __name__ == '__main__':
	add_flag(sys.argv[1],sys.argv[2],sys.argv[3])	




