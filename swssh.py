#!/usr/bin/evn python
import os
import paramiko

port = 22

print("host ip: ")
host = input()
print("username: ")
username = input()
#username = "manager"

print("key or password (k or p):")
trigger = input()

if(trigger == 'p'):
	print("password: ")
	password = input()
#password = "friend"

print("local file: ")
localFile = input()
#localFile = r'/Users/shaw/desktop/test.scp'

remoteFile ='flash:/' + localFile.split('/')[len(localFile.split('/'))-1]
#remoteFile = r'flash:/test.scp'

ssh = paramiko.Transport((host,port))
privatekeyfile = os.path.expanduser('~/.ssh/id_rsa') 
mykey = paramiko.RSAKey.from_private_key_file( os.path.expanduser('~/.ssh/id_rsa'))   # load key
if(trigger == 'p'):
	ssh.connect(username = username, password = password)           # connect remote switch
else:
	ssh.connect(username = username, pkey = mykey)					#connect remote switch using key

sftp = paramiko.SFTPClient.from_transport(ssh)             # Transport channel used by SFTP
#sftp.get('/etc/passwd','pwd1')                            # download
sftp.put(localFile,remoteFile)                             # upload

sftp.close()
ssh.close()

s = paramiko.SSHClient()                                 
s.load_system_host_keys()                                	# load local host file
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())  	# allow to connect switch that did not exist in know_hosts file
s.connect(host,port,username,password,timeout = 5)           	# connect remote switch

cmd = "activate " + remoteFile
stdin,stdout,stderr = s.exec_command(cmd)        # execute commands
cmd_result = stdout.read(),stderr.read()         # grab the execution results
for line in cmd_result:
        print(line)
