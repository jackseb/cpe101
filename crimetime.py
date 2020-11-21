"""
crimetime.py
CPE 101
Section: 3
Name: Jack Sebasco
Cal Poly Username: jsebasco
"""




"""
Implementation requirements:
1) -> specifying return types in function declaration
2) Crime object
    attrs:
        crime_id as read from crimes.tsv
        category as read from crimes.tsv
        day_of_week as read from times.tsv
        month modified from times.tsv to be a full word
        hour modified from times.tsv to be in AM/PM format
    __init__(self,crime_id, category):
        other attrs initialize to None
    __eq__(self,other):
        True if id of 2 crime objects is the same, false otherwise
    __repr__(self):
        tab between attributes with a newline character at the end
3) create_crimes(lines) -> list
4) sort_crimes(crimes) -> list
5) set_crimetime(crime, day_of_week, month, hour)
6) update_crimes(crimes, lines)
7) find_crime(crimes, crime_id) -> Crime
Output
1) robberies.tsv
2) print the following stats:
    NUMBER OF PROCESSED ROBERIES: _
    DAY WITH MOST ROBBERIES: _
    MONTH WITH MOST ROBBERIES: _
    HOUR WITH MOST ROBBERIES: _
"""

from sys import argv
from copy import copy
from calendar import month_name

crimeFile = argv[1]
timeFile = argv[2]

def main():
    crimeLines, timeLines = [], []
    with open(crimeFile,"r+") as crimeFileOpen:
        crimeLines = crimeFileOpen.readlines()
    with open(timeFile,"r+") as timeFileOpen:
        timeLines = timeFileOpen.readlines()
    robberies = create_crimes(crimeLines)
    sorted_robberies = sort_crimes(robberies)
    update_crimes(sorted_robberies, timeLines)
    get_crime_stats(sorted_robberies)
    gen_output_file(sorted_robberies)

class Crime:
    def __init__(self, crime_id, category):
        self.crime_id = int(crime_id)
        self.category = category
        self.day_of_week = None
        self.month = None
        self.hour = None
    def __eq__(self,other):
        try: 
            return self.crime_id == other.crime_id
        except AttributeError as e:
            if "NoneType" in str(e):
                return False
            else:
                raise AttributeError(e)
    def __repr__(self):
        return f"{self.crime_id}\t{self.category}\t{self.day_of_week}\t{self.month}\t{self.hour}\n"

def create_crimes(lines)->list:
    crimes = []
    IDS = set()
    for line in lines[1:]:
        crime_id, category, _  = line.split("\t")
        if crime_id not in IDS and category == "ROBBERY":
            crimes.append(Crime(crime_id, category))
            IDS.add(crime_id)
    return crimes
    
def sort_crimes(crimes)->list:
    sorted_crimes = copy(crimes)
    i = 0
    while i < len(sorted_crimes) - 1:
        j, _min = i , i 
        while j < len(sorted_crimes):
            _min = _min if sorted_crimes[j].crime_id >= sorted_crimes[_min].crime_id else j 
            j += 1
        sorted_crimes[i], sorted_crimes[_min] = sorted_crimes[_min], sorted_crimes[i]
        i += 1
    return sorted_crimes

def set_crimetime(crime, day_of_week, month, hour):
    crime.day_of_week = day_of_week
    crime.month = month_name[int(month)]
    crime.hour = convert_time(hour)

def update_crimes(crimes, lines):
    for line in lines[1:]:
        crime_id, day_of_week, date, time  = line.split("\t")
        crime = find_crime(crimes, int(crime_id))
        if crime != None:
            month = date.split("/")[0].strip()
            hour = time.split(":")[0].strip()
            set_crimetime(crime, day_of_week.strip(), month, hour)
    
def find_crime(crimes, crime_id)->Crime:
    # Binary search
    i, j = 0, len(crimes)
    while i < j:
        m = (i + j)//2
        if crimes[m].crime_id > crime_id:
            j = m
        elif crimes[m].crime_id < crime_id:
            i = m + 1
        else:
            return crimes[m]

def convert_time(time_24)->str:
    time_24 = int(time_24)
    if -1 < time_24 < 25:
        suffix = "PM" if time_24 > 11 else "AM" 
        time_12 = time_24 % 12 if time_24 % 12 != 0 else 12
        return f"{time_12}{suffix}"
    else:
        return None

def gen_output_file(crimes, fname = "robberies.tsv"):
    with open(fname,"w+") as out:
        out.writelines(["ID\tCategory\tDayOfWeek\tMonth\tHour\n"]+[c.__repr__() for c in crimes])

def align_right(str_list, padding = " "):
    r_length = max([len(r) for r in str_list])
    for i in range(len(str_list)):
        str_list[i] = padding * (r_length - len(str_list[i])) + str_list[i]

def maxRobberiesByAttribute(crimes,attribute)->str:
    cache = {}
    for crime in crimes:
        cache[getattr(crime,attribute)] = cache[getattr(crime,attribute)] + 1 if getattr(crime,attribute) in cache else 1
    return max(cache, key=cache.get)

def get_crime_stats(crimes):
    question = [
        "NUMBER OF PROCESSED ROBBERIES: ",
        "DAY WITH MOST ROBBERIES: ",
        "MONTH WITH MOST ROBBERIES: ",
        "HOUR WITH MOST ROBBERIES: "
    ]
    answer = [
        len(crimes),
        maxRobberiesByAttribute(crimes, 'day_of_week'),
        maxRobberiesByAttribute(crimes, 'month'),
        maxRobberiesByAttribute(crimes, 'hour')
    ]
    align_right(question)
    for i in range(len(question)):
        print(f"{question[i]}{answer[i]}")

if __name__ == "__main__":
    main()
