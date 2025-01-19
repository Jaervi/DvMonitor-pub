import paramiko
import netdata

class SSHStat():
    hostname = ''
    username = ''
    userpwd = ''
    contents = ''

    def __init__(self,name,user,pwd):
        self.hostname = name
        self.username = user
        self.userpwd = pwd

    #Executes the specified command in the device
    def execcmd(self,cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname, username=self.username, password=self.userpwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        self.contents = stdout.read().decode('latin-1')
        ssh.close()

    def isWorking(self):
        if len(self.contents) == 0:
            print("isWorking called for empty contents. Returning true.")
            return True
        else:
            return 'Reader Not connected!' not in self.contents
    