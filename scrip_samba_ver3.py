#!/usr/bin/python3.4

import os

VERMELHO = '\033[31m'
VERDE = '\033[32m'               
AMARELO = '\033[33m'                  
AZUL = '\033[34m'                     
MAGENTA = '\033[35m'                 
CIANO = '\033[36m'
CINZA_CLARO = '\033[37m'          
BRANCO = '\033[38m'
FUNDO_AZ = '\033[44;1;37m'
NORMAL = '\033[0;0m'

setVarOp1 = 0
setVarOp2 = 0
setVarOp3 = 0

os.system('clear')
print('\n', FUNDO_AZ, 'Iniciando scrip de instalação e configuração Servidor Samba...', NORMAL, '\n')

smb = os.system('ls /etc/samba > /dev/null 2> /dev/null')
if smb != 0:
	print(CINZA_CLARO,'Instalando Samba...\n', NORMAL)
	os.system('apt-get update > /dev/null')
	os.system('apt-get install samba samba-common -y --force-yes')	
	os.system('mv /etc/samba/smb.conf /etc/samba/smb.conf.bak')

	#### [global]

	wg = input('\nGrupo de trabalho? default [WORKGROUP]: ')
	if wg == '':
		wg = 'WORKGROUP'

	glob = ['[global]',
			'workgroup = %s' %wg,
			'server string = Samba Server %v',
			'netbios name = debian',
			'security = user',
			'map to guest = bad user',
			'dns proxy = no']

	for i in range(0, len(glob), 1):
		if i != 0:
			glob[i] = glob[i].replace('[', '')
			glob[i] = glob[i].replace(']', '')
			os.system('echo %s >> /etc/samba/smb.conf' %glob[i])	
		else:
			os.system('echo %s >> /etc/samba/smb.conf' %glob[i])
else:
	os.system('date +%d-%m-%Y_%H:%M:%S | xargs -I@ cp /etc/samba/smb.conf /etc/samba/smb.conf.@')


#### Samba Shares

while True:
	print(MAGENTA, '\nTipo de compartilhamento Samba:\n', NORMAL)
	print('1. Anônimo (Sem usuário e senha)')
	print('2. Usuário local (Com autenticação p/ diretório(s) compartilhado)')
	print('3. Usuário local (Com autenticação p/ acesso a sua home)')
	print('4. Sair\n')
	x = int(input('Opção: '))
	print('\r')

	# Compartilhamento anônimo

	if x == 1:	
		setVarOp1 = 1	
		nameShare = input('Nome para compartilhamento? default [anonymous]: ')
		if nameShare == '':
			nameShare = 'anonymous'

		dir = input('Diretório compartilhado? default [/home/shares/anonynous]: ')
		if dir == '':
			dir = '/home/shares/anonymous'

		os.system('mkdir -p %s' %dir)
		os.system('chown -R root:users %s' %dir)
		os.system('chmod -R ug+rwx,o+rx-w %s' %dir)

		share = ['[%s]' %nameShare,
		  		'path = %s' %dir,  		
		  		'force group = users',
		  		'create mask = 0660',
		  		'directory mask = 0771',
		  		'browsable = yes',
		  		'writable = yes',
		  		'guest ok = yes']


		os.system('echo '' >> /etc/samba/smb.conf')	
		for i in range(0, len(share), 1):
			if i != 0:
				share[i] = share[i].replace('[', '')
				share[i] = share[i].replace(']', '')
				os.system('echo %s >> /etc/samba/smb.conf' %share[i])	
			else:
				os.system('echo %s >> /etc/samba/smb.conf' %share[i])

		print('\r')			

	# Com autenticação p/ diretório(s) compartilhado

	elif x == 2:
		setVarOp2 = 1
		nameShare = input('Nome para compartilhamento? default [win]: ')
		if nameShare == '':
			nameShare = 'win'

		dir = input('Diretório compartilhado? default [/home/shares/win]: ')
		if dir == '':
			dir = '/home/shares/win'

		os.system('mkdir -p %s' %dir)
		os.system('chown -R root:users %s' %dir)
		os.system('chmod -R ug+rwx,o+rx-w %s' %dir)

		share = ['[%s]' %nameShare,
				'comment = All Users',
		  		'path = %s' %dir,  
		  		'valid users = @users',
		  		'force group = users',
		  		'create mask = 0660',
		  		'directory mask = 0771',
		  		'writable = yes']
		  		
		os.system('echo '' >> /etc/samba/smb.conf')	
		for i in range(0, len(share), 1):
			if i != 0:
				share[i] = share[i].replace('[', '')
				share[i] = share[i].replace(']', '')
				os.system('echo %s >> /etc/samba/smb.conf' %share[i])	
			else:
				os.system('echo %s >> /etc/samba/smb.conf' %share[i])

		print('\r')			

	# Com autenticação p/ acesso a sua home

	elif x == 3:
		setVarOp3 = 1

		d = os.system('grep homes /etc/samba/smb.conf > /dev/null 2> /dev/null')
		if d != 0:
			setVar = 1
			share = ['[homes]',
			  		'comment = Home Directories', 
			  		'browseable = no', 
			  		'valid users = %S',
			  		'writable = yes',		
			  		'create mask = 0700',
			  		'directory mask = 0700']

			os.system('echo '' >> /etc/samba/smb.conf')	
			for i in range(0, len(share), 1):
				if i != 0:
					share[i] = share[i].replace('[', '')
					share[i] = share[i].replace(']', '')
					os.system('echo %s >> /etc/samba/smb.conf' %share[i])	
				else:
					os.system('echo %s >> /etc/samba/smb.conf' %share[i])
		else:
			print(VERMELHO, '\nCompartilhamento para home de usuário local já criado!!!\n\n', NORMAL)
						

	# Sair

	elif x == 4:
		break

	# Opção inválida para compartilhamento

	else:
		print('\nOpção inválida para compartilhamento, tente novamente...')
		continue

	op = input('Criar outro compartilhamento Samba? (s/N): ')
	if op == '':
		op = 'n'

	if op != 's' and op != 'S':
		print('\r')
		os.system('/etc/init.d/samba restart')
		break

#### Usuário samba

if setVarOp2 != 0 or setVarOp3 != 0:	
# if setVarOp2 != 0:	
	while True:	
		userSMB = input('\nNome para usuário samba? ')
		x = os.system('grep %s /etc/passwd > /dev/null' %userSMB)
# em shell script
# grep aluno /etc/passwd| cut -d: -f1
		
		print('\r')

		if x == 0:	# Se usuário já existir
			os.system('addgroup %s users' %userSMB)	# Add usuário que já existe ao grupo 'users'
			print('\r')
			os.system('smbpasswd -a %s' %userSMB)   # Add senha no samba
		else:
			os.system('useradd %s -m -G users' %userSMB)
			os.system('passwd %s' %userSMB)
			print('\r')
			os.system('smbpasswd -a %s' %userSMB)   # Add senha no samba

		op = input('\nAdicionar outro usuário? (s/N): ')
		if op == '':
			op = 'n'

		if op != 's' and op != 'S':
			break

print(AMARELO, '\nBye...', NORMAL)
print('\r')
