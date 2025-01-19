import ping3
import requests
import paramiko
from apscheduler.schedulers.background import BackgroundScheduler
from ResponseParser import ResponseParser
from ResponseStats import ResponseStat
import ResponseStats
from SSHStats import SSHStat
import netdata          #netdata.py is a local file containing all ip addresses and credentials, not in version control for obvious reasons. If it doesn't exist, make it :)
import UFRFix
import argparse
import time
import datetime
import syncping
import concurrent.futures
import eventlogger as el

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def check_devices(args):
    start_time = datetime.datetime.now()
    print(f'\n{start_time.strftime(DATE_FORMAT)}\nChecking devices:')

    ping_result = []
    response = None

    # Pinging the ping list and making a GET-request inside a future to improve execution speed.
    with concurrent.futures.ThreadPoolExecutor() as exec:
        ping_future = exec.submit(syncping.ping_list,netdata.pinglist)
        request_future = exec.submit(requests.get,netdata.readaddress, timeout=15)

        ping_result = ping_future.result()
        response = request_future.result()


    syncping.informative_print(ping_result)
    if not response:
        print('GET-request timed out. Cannot check device reads.')
    else:
        rp = ResponseParser(response.text)
        rp.setIdentifiers(netdata.IDList)
        time_list = rp.getAllTimesAsString()
        print('All monitored devices:')
        ResponseStats.pretty_print(time_list)

        rs =  ResponseStat(rp.getAllTimes())
        maxList = list(map(lambda x: [x[0], rs.fromUnixtoDate(x[1])],rs.differsFromMaxBy(5)))
        print('Devices 30mins behind current max:')
        ResponseStats.pretty_print(maxList)
        if 'device_name' in map(lambda x: x[0],maxList):        # If device differs enough from the max, try to restart the screen instance if option is enabled
            if not args.screen_restart:
                print('Did not restart screen because option "--screen_restart" is not enabled')
            else:
                UFRFix.restartPhoneScreen(netdata.sshost_phone,netdata.sshuser,netdata.sshpwd)
        
        if not args.device_reboot:
                print('Did not reboot any devices because option "--device_reboot" is not enabled')
        else:                         # If any of the registers is not read in a while but the others are, reboot it.
            if 'device_name' in map(lambda x: x[0],maxList):
                UFRFix.rebootDevice(netdata.sshost_reg1,netdata.sshuser,netdata.sshpwd)
        
        if not args.service_restart or args.device_reboot:
                if args.device_reboot:
                    print('Did not restart any services because reboot was already executed on the devices')
                else:
                    print('Did not restart any services because option "--service_restart" is not enabled')
        else:                         # If any of the registers is not read in a while but the others are, restart it.
            if 'device_name' in map(lambda x: x[0],maxList):
                UFRFix.restartService(netdata.sshost_reg1,netdata.sshuser,netdata.sshpwd, 'svc_name')
        


    #End the method execution and print the elapsed time
    elapsed_time = datetime.datetime.now() - start_time
    print(f'Device check over. Time elapsed: {elapsed_time.total_seconds()}s')
    print(f'Start time: {start_time.strftime(DATE_FORMAT)}\n')

def start():
    print('Starting program:')
    el.log_event('Started the program')
    parser = argparse.ArgumentParser(description='A script to monitor devices in a network')
    parser.add_argument('--monitor_freq', type=int, help='The frequency of the device checks, in seconds. Syntax: --monitor_freq=120',default=120)
    parser.add_argument('--screen_restart',action='store_true', help='Enables the screen restart feature')
    parser.add_argument('--service_restart',action='store_true',help='Enables the service restart feature. Restarts the service on the device if it hasn\'t responded in a while')
    parser.add_argument('--device_reboot',action='store_true',help='Enables the service restart feature. Reboots the service on the device if it hasn\'t responded in a while')
    clargs = parser.parse_args()

    print('Starting monitor with parameters:')
    print(f'Frequency: {clargs.monitor_freq}s')
    print(f'Screen restart: {clargs.screen_restart}')
    print(f'Service restart: {clargs.service_restart}')
    print(f'Device reboot: {clargs.device_reboot}')
    if clargs.service_restart and clargs.device_reboot:
        print('NOTE: enabling both "service_restart" and "device_reboot" will not use service restarting if reboot is already executed on the device.')

    timer = BackgroundScheduler()
    timer.start()
    timer.add_job(check_devices,'interval',args=[clargs], seconds = clargs.monitor_freq)
    check_devices(clargs)

    try:
        while True:
            userinput = input()
            if userinput.lower() == 'exit':
                timer.shutdown()
                el.log_event('Stopped the program with exit command')
                return 1
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        el.log_event('Stopped the program due to system interruption')
        timer.shutdown()



start()
