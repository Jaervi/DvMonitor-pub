# DvMonitor

## DvMonitor is a simple program to monitor devices in a network. 
### Main features:

- Ping a list of IP-addresses and show the ping results
- Fetch NFC-read data from a website and restart corresponding devices/features if necessary
- Restart Linux devices (Raspberry Pi:s) when certain criteria is met

### Command-line arguments
The features can be toggled with command-line arguments. The arguments are as follows:

``` 
  --monitor_freq=[time_in_seconds]  // The frequency of how often the devices are checked. Defaults to 120 if left empty. Example syntax: --monitor_freq=240
  --screen_restart                  // When enabled, the program restarts a screen instance in a specific device if the instance has terminated
  --service_restart                 // When enabled, the program restarts systemd services on selected devices
  --device_reboot                   // When enabled, the program reboots a device when certain criteria is met
```
Please note that enabling both "service_restart" and "device_reboot" will not use service restarting if reboot is already executed on a device.
Values below __20 seconds__ are __not recommended__ for --monitor_freq

### Importing data into the program

All user-specific data will be stored in a local file called `netdata.py`. The file must be made manually for each device, it doesn't exist in version control. To get started, the repository contains a base file called `netdata_example.py`. Some tweaks to the source code might be necessary depending on the device configuration.

### Quick start guide

The program was made and tested with Python 3.12.4. Support for earlier versions is not quaranteed

- Download the source code
- In the download folder, create a virtual environment:
  ```
  $ python -m venv myenv
  ```
- Activate the environment
  
    On Windows
    
    ```
    $ myenv\Scripts\activate
    ```
    On Unix or MacOS
    
    ```
    $ source myenv/bin/activate
    ```

- Install the program dependencies

  ```
  pip install -r requirements.txt
  ```

- Setup the `netdata.py` file, below are the contents of `netdata_example.py`. To have the program work "out-of-the-box", the following fields must be filled inside `netdata.py`.

  ```python
  readaddress = ''    # The address of the website containing device read information
  sshost_reg1 = ''    # IP addresses for the registers
  sshost_reg2 = ''    # ^^
  sshost_reg3 = ''    # ^^ 
  sshost_reg4 = ''    # ^^ 
  sshost_dev5 = ''   # IP address for the device with the restartable screen 
  sshpwd = ''         # The SSH password of the devices. If there are multiple credentials, tweak the source code accordingly
  sshuser = ''        # The SSH username. If there are multiple credentials, tweak the source code accordingly
  restartcommand = '' # The command to restart the screen instance on the device specified by sshost_phone
  
  IDList = []         # List of device names present in the site specified by readaddress
  pinglist = []       # List of IP addresses to be pinged

  ```

- Run the program

  - Only list the device information (default interval 120 seconds)
    
    ```
    python dvmonitor.py
    ```
  - Also restart the screen and set the interval to 240 seconds
    
    ```
    python dvmonitor.py --monitor_freq=240 --screen_restart
    ```
  - Run with all features enabled using service_restart instead of device_reboot, checking devices every 5 minutes
    
    ```
    python dvmonitor.py --monitor_freq=300 --screen_restart --service_restart
    ```

- To exit the program type 'exit' into the console. If a device check is running, the input might not go through. Wait ~10s and try again

#### NOTE:
This project is a tool made by me at a previous workplace of mine primarily for personal use.
Therefore this version of the project has all company specific data changed to generic names but no functionality has been changed. 
So it doesn't quite work out of the box but no major changes would be required to do so, logic is virtually unchanged
