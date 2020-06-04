from pwn import *
import sys
p = process("./a.out")


def exploit(username,password):
	pass_test = True

	test_ticket = b'11666315782702852425'
	test_value = 'ENOFLAGENOFLAG='
	must_be_in_menu1 = ['menu','login','register','view ticket','exit']
	must_be_in_view_ticket_menu = ['ticket','id']


	menu1 = p.recv(200).decode('ascii').lower()
	for elem in must_be_in_menu1:
		if elem not in menu1:
			print('failed first test: \'{}\' not in menu'.format(elem))
			pass_test = False

	
	p.sendline(b'3')
	menu_after_view_ticket_global = p.recv(200).decode('ascii')


	for elem in must_be_in_view_ticket_menu:
		if elem not in menu_after_view_ticket_global:
			print('failed second test: {} not in menu'.format(elem))
			pass_test = False

	p.sendline(test_ticket)
	p.recvline()
	retrieve_noise = p.recv(200).decode('ascii').strip()
	print('got noise: {}'.format(retrieve_noise))
	if retrieve_noise != 'ENOFLAGENOFLAG=' or retrieve_noise == '':
		print('failed last test: \'{}\' noises didnt match'.format(retrieve_noise))
		pass_test = False

	if pass_test:
		print('passed')
	else:
		print('not passed')
if __name__ == '__main__':
	exploit(sys.argv[1],sys.argv[2])
