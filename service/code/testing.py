from pwn import *
import sys
p = process("./a.out")


def exploit(username,password):
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
	print("Putting in flag: Flag{}")
	flag = "hello world"
	p.sendline(b"testflag")
	time.sleep(.1)
	p.recvuntil(b"================\n")
	p.sendlineafter(b"================\n",b"2")
	stdo = p.recvline()
	ticket_id = p.recvline().decode('ascii').split(" ")[1]
	print("The new flag is at index: {}".format(ticket_id))

if __name__ == '__main__':
	exploit(sys.argv[1],sys.argv[2])
