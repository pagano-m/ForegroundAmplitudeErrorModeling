import paramiko
import getpass
import scp
import os

#sh: sshpass: command not found
def test():
    os.system("sshpass -p Gl0ck@.56GAP scp -o StrictHostKeyChecking=no test2.txt grx40@cedar.computecanada.ca:/home/grx40/scratch/Scale_Factor_Nreg/150MHz_wSpecComplex/NoScafacs/")

#works
def transfer_to(file, location):
    os.system("sshpass -p Gl0ck@.56GAP scp -o StrictHostKeyChecking=no " + str(file) + "grx40@cedar.computecanada.ca:" +str(location))

def transfer_from(file, location):
    os.system("sshpass -p Gl0ck@.56GAP scp -o StrictHostKeyChecking=no " + "grx40@cedar.computecanada.ca:" +str(file) + " " + str(file) )


'''
    #This is not needed. There is a faster more direct way below
password = getpass.getpass()

ssh = paramiko.SSHClient()
                         
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy() )
                         
ssh.connect('cedar.computecanada.ca', username='grx40', password='Gl0ck@.56GAP')
                         
print('IN')

'''
def transfer_files_FAIL(pickup, dropoff):
    host = 'cedar.computecanada.ca'
    password = 'Gl0ck@.56GAP'
    user = 'grx40'
    client = scp.Client(host=host, user=user, password=password)

    # and then
    client.transfer(pickup, dropoff)

from paramiko import SSHClient
from scp import SCPClient

server = '@cedar.computecanada.ca'
username = 'grx40'
password = 'Gl0ck@.56GAP'



#keyfile = os.path.expanduser('/users/michael/.ssh/id_rsa')
#password = keyring.get_password('SSH', keyfile)
#key = paramiko.RSAKey.from_private_key_file('/users/michael/.ssh/id_rsa', password='Gl0ck@.56GAP')
#key = paramiko.RSAKey.from_private_key_file(keyfile, password=password)


'''
    FAILS
ssh = SSHClient()
ssh.load_system_host_keys()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('cedar.computecanada.ca', username = 'grx40', password = 'Gl0ck@.56GAP', pkey=pk)

# SCPCLient takes a paramiko transport as an argument
transport = paramiko.Transport('cedar.computecanada.ca')
transport.connect(username='grx40')
transport.auth_password(username, password)
transport.auth_interactive_dumb(username)

scp = SCPClient(ssh.get_transport())

#scp.put('test.txt', 'test2.txt')
#scp.get('/home/grx40/scratch/Scale_Factor_Nreg/150MHz_wSpecComplex/NoScafacs/make_data_def.sh')

# Uploading the 'test' directory with its content in the
# '/home/user/dump' remote directory
scp.put('test.txt', recursive=True, remote_path='/home/grx40/scratch/Scale_Factor_Nreg/150MHz_wSpecComplex/NoScafacs/')

scp.close()


'''

'''
import os
import paramiko
localpath = 'test.txt'
server = 'cedar.computecanada.ca'
remotepath = '/home/grx40/scratch/Scale_Factor_Nreg/150MHz_wSpecComplex/NoScafacs/'
ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect(server, username=username, password=password)
sftp = ssh.open_sftp()
sftp.put(localpath, remotepath)
sftp.close()
ssh.close()
'''
