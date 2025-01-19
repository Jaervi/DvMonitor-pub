import os
from datetime import datetime

curpath = os.path.dirname(__file__)
log_file = f'{curpath}/events.log'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def log_event(contents):
    timestamp = datetime.now().strftime(DATE_FORMAT)
    #Check if log file exists, if not create an empty one
    if not os.path.exists(log_file):
        open(log_file, "w").close()
    #Write the contents into the file with the timestamp
    with open(log_file, "a") as file:
        file.write(f'{timestamp} - {contents}\n')