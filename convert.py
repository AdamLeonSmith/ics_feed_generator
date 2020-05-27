#!/usr/bin/python3
from datetime import datetime, timedelta
from icalendar import Calendar, Event, Alarm
import csv

def get_start_time(date, slot):
    _t = e['UTC slot'].replace(' UTC', '')
    print(_t)
    if(len(_t) > 3):
        hrs = int(_t[0:2])
        mins = int(_t[2:4])
    else:
        hrs = int(_t[0:1])
        mins = int(_t[1:2])

    print(hrs)
    print(mins)
    date = date + timedelta(hours=hrs, minutes=mins)
    return date


cal = Calendar()
with open('in.csv', 'rt') as csvfile:
    print("Reading file")
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    n = -1
    for row in reader:
        n = n + 1
        print(n)
        if n == 2:
            keys = row
        if n > 2:
            e = dict(zip(keys, row))
            print(keys)
            if e['Registration'] is not "" and e['Host'] is not "":
                event = Event()
                event.add('summary', e['Affiliation'] + e['Project'])
                print(e['date'])

                start_date = datetime.strptime(e['date'] + '+0000', "%Y-%m-%d%z")
                start_time = get_start_time(start_date, e['UTC slot'])
                print('start time: ' + str(start_time))

                event.add('dtstart', start_time)
                event.add('dtend',  start_time + timedelta(hours=2))
                event.add('location', e['Registration'] )
                event.add('description', 'Host: ' + e['Host'] + "\nPlease refer to the registration URL for the connection details: " + e['Registration'])
                print(event)
                alarm = Alarm()
                alarm.add("ACTION", "DISPLAY")
                alarm.add("TRIGGER", start_time - timedelta(days=10))
                alarm.add("SUMMARY", "72 hours remain to submit materials for " + e['Affiliation'] + e['Project'])
                event.add_component(alarm)
                cal.add_component(event)

f = open('wg3_meetings.ics', 'wb')
f.write(cal.to_ical())
f.close()
