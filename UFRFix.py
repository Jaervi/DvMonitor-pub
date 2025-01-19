import paramiko
import ping3
import netdata
import time
import eventlogger as el


#Restarts the specific screen instance in a raspberry pi. Returns 1 if restart was executed, 0 if not. Returns -1 if the device couldn't be found.
def restartPhoneScreen(hostname,username,userpwd):
    delay = ping3.ping(hostname, unit='ms', timeout=10)
    if delay == None:
        print("The device didn't respond. Returning...")
        el.log_event(f'Tried to restart screen at {hostname} but it didn\'t respond fast enough.')
        return -1
    else:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=userpwd)
        stdin, stdout, stderr = ssh.exec_command('screen -ls')
        output = stdout.read().decode('latin-1')
        print(output)
        if ('There is a screen on' in output):
            print('Screen is on, not restarting script')
            ssh.close()
            return 0
        else:
            print("Restarting screen")
            stdin, stdout, stderr = ssh.exec_command(netdata.restartcommand)
            ssh.close()
            el.log_event(f'Restarted phone screen {hostname} with stdout {output.rstrip()}')
            return 1

#Runs 'sudo reboot' on the device     
def rebootDevice(hostname,username,userpwd):
    delay = ping3.ping(hostname, unit='ms', timeout=10)
    if delay == None:
        print("The device didn't respond. Can't restart")
        el.log_event(f'Tried to reboot device {hostname} but it didn\'t respond fast enough')
        return -1
    else:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=userpwd)
        ssh.exec_command(f'echo {netdata.sshpwd} | sudo -S reboot')
        ssh.close()
        el.log_event(f'Rebooted device {hostname}')
        return 1

#Restarts the service on the device
def restartService(hostname,username,userpwd, servicename):
    delay = ping3.ping(hostname, unit='ms', timeout=10)
    if delay == None:
        print(f'The device didn\'t respond. Can\'t restart service {servicename}')
        el.log_event(f'Tried to restart service {servicename} on device {hostname} but it didn\'t respond fast enough')
        return -1
    else:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=userpwd)
        stdin, stdout, stderr = ssh.exec_command(f'echo {netdata.sshpwd} | sudo -S systemctl stop {servicename}')
        time.sleep(6)
        stdin, stdout, stderr = ssh.exec_command(f'echo {netdata.sshpwd} | sudo -S systemctl start {servicename}')
        ssh.close()
        el.log_event(f'Restarted service {servicename} on device {hostname}')
        return 1