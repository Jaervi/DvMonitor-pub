from datetime import datetime as dt
import time

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def pretty_print(input_list):
        for entry in input_list:
            print(f'{entry[0]}: {entry[1]}')
        print('\n')

class ResponseStat():
    entries = []

    def __init__(self, list):
        self.entries = list
    
    #Returns the average time of the entries
    def entryAverage(self):
        if len(self.entries) == 0:
            print('Tried to get average of an empty list. Returning 0.')
            return 0.0
        else:
            filtered = list(filter(lambda y: y[1].hour != 0 ,self.entries))
            numList = list(map(lambda x: self.toUnixTime(x[1]),filtered))
            return sum(numList) / len(numList)

    #Returns a list of entries which differ from the current/the average/the latest time by the specified minutes 
    def differsBy(self,mins):
        unixMap = list(map(lambda x: [x[0], self.toUnixTime(x[1])],self.entries))
        return list(filter(lambda y: self.toUnixTime(dt.now())-y[1] > mins*60 ,unixMap))
    def differsFromAvgBy(self,mins):
        unixMap = list(map(lambda x: [x[0], self.toUnixTime(x[1])],self.entries))
        return list(filter(lambda y: self.entryAverage()-y[1] > mins*60 ,unixMap))
    def differsFromMaxBy(self,mins):
        unixMap = list(map(lambda x: [x[0], self.toUnixTime(x[1])],self.entries))
        return list(filter(lambda y: self.latestEntry()-y[1] > mins*60 ,unixMap))

    #Returns the latest entry in the list
    def latestEntry(self):
        return max(map(lambda x: self.toUnixTime(x[1]),self.entries))

    #Converts a datetime object to Unix time
    def toUnixTime(self, date_time):
        return time.mktime(date_time.timetuple())
    
    #Converts a Unix timestamp to a string in DATE_FORMAT
    def fromUnixtoDate(self,unix_time):
        date = dt.fromtimestamp(unix_time)
        return date.strftime(DATE_FORMAT)