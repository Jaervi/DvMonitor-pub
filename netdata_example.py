readaddress = ''    # The address of the website containing device read information
sshost_reg1 = ''    # IP addresses for the registers
sshost_reg2 = ''    # ^^
sshost_reg3 = ''    # ^^ 
sshost_reg4 = ''    # ^^ 
sshost_phone = ''   # IP address for the device with the restartable screen 
sshpwd = ''         # The SSH password of the devices. If there are multiple credentials, tweak the source code accordingly
sshuser = ''        # The SSH username. If there are multiple credentials, tweak the source code accordingly
restartcommand = '' # The command to restart the screen instance on the device specified by sshost_phone

IDList = []         # List of device names present in the site specified by readaddress
pinglist = []       # List of IP addresses to be pinged
