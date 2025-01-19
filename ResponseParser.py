import re
from datetime import datetime as dt
from datetime import time as tm


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class ResponseParser():
    body = ''
    identifiers = []        #A List of the titles to be searched for

    def __init__(self, body):
        self.body = body
    #Adds a title to the list
    def addIdentifier(self, identifier):
        self.identifiers.append(identifier)
    #Sets the title list 
    def setIdentifiers(self, list):
        self.identifiers = list

    #Given an ID, searches the corresponding timestamp from the body of the request
    #Makes a request to a known address to fetch the html file and parses the required fields from the file 
    def getTimeFromID(self, ID):
        #Handle invalid IDs
        if(self.body.find(ID) == -1):
            print(f'The ID "{ID}" was not found in the request. Returning current time')
            return self.defaultTime()
        else:
            text = self.body[self.body.find(ID):self.body.find('</h2>',self.body.find(ID))]     #Split the string to only contain relevant information
            match = re.search(r'\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2}',text)                 #Regex to search for the date
            if match == None:  
                return self.defaultTime()
            else:
                return dt.strptime(match.group(),DATE_FORMAT)       #Returns a datetime object corresponding to the date text

    #Returns the times of the identifier list values as a list
    def getAllTimes(self):
        arr = map(lambda x: [x, self.getTimeFromID(x)], self.identifiers)
        return list(arr)
    
    #Returns the times of the values in the identifier list as a list in string format
    def getAllTimesAsString(self):
        arr = map(lambda x: [x, self.timeToString(self.getTimeFromID(x))], self.identifiers)
        return list(arr)

    #Converts a datetime to a string in DATE_FORMAT 
    def timeToString(self, time):
        return dt.strftime(time,DATE_FORMAT)

    #Converts a string of DATE_FORMAT to a datetime
    def stringToTime(self, string):
        return dt.strptime(string,DATE_FORMAT)
    
    #Returns today at 0:00 as a datetime object
    def defaultTime(self):
        return dt.combine(dt.now(), tm(0,0))
    
