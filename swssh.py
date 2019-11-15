#!/usr/bin/evn python
import os
import paramiko


info1 = [22, '192.168.0.10', 'manager', 'friend']
info2 = [22, '192.168.0.11', 'manager', 'friend']
info3 = []
#files = []

host = {"host1": info1,"host2": info2, "host3": info3}	#dictionary of host names and their corresponding info

folderPath = '/Users/shaw/desktop/swconfig/'	#folder for local files, filename should be the same as hostname

def whatToSend():	#get all the files under the specified folder
	fileList = os.listdir(folderPath)
	#for i in range(len(fileList)):
		#files.append(folderPath + fileList[i])
	return fileList	

def whereToSend(fileName):	#compare the filename with the hostname to find out where to send
	try:
		if fileName.split('.')[0] == 'host1':
			return host['host1']
		elif fileName.split('.')[0] == 'host2':
			return host['host2']
		elif fileName.split('.')[0] == 'host3':
			return host['host3']
	except:
		print('Error')

'''

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
'''

remoteFile = 'flash:/OFrules.scp'

for i in whatToSend(): #send and execute files to switches one by one
	info = whereToSend(i)
	print(info)
	try:
		ssh = paramiko.Transport((info[1],info[0]))
		#privatekeyfile = os.path.expanduser('~/.ssh/id_rsa') 
		#mykey = paramiko.RSAKey.from_private_key_file( os.path.expanduser('~/.ssh/id_rsa'))   # load key

		ssh.connect(username = info[2], password = info[3])           # connect remote switch

		sftp = paramiko.SFTPClient.from_transport(ssh)             # Transport channel used by SFTP
		#sftp.get('/etc/passwd','pwd1')                            # download
		sftp.put(folderPath + i,remoteFile)                             # upload

		sftp.close()
		ssh.close()

		s = paramiko.SSHClient()                                 
		s.load_system_host_keys()                                	# load local host file
		s.set_missing_host_key_policy(paramiko.AutoAddPolicy())  	# allow to connect switch that did not exist in know_hosts file
		s.connect(info[1],info[0],info[2],info[3],timeout = 5)           	# connect remote switch

		cmd = "activate " + remoteFile
		stdin,stdout,stderr = s.exec_command(cmd)        # execute commands
		cmd_result = stdout.read(),stderr.read()         # grab the execution results
		for line in cmd_result:
		        print(line)
	except:
		print("Failed to send...")
