#!/usr/bin/python3
from datetime import datetime, timedelta
from icalendar import Calendar, Event, Alarm
import csv

def get_start_time(date, slot):
    _t = e['UTC slot'].replace(' UTC', '')
    print(_t)
    if _t == "0":
        hrs = 0
        mins = 0
    elif(len(_t) > 3):
        hrs = int(_t[0:2])
        mins = int(_t[2:4])
    else:
        hrs = int(_t[0:1])
        mins = int(_t[1:2])

    print(hrs)
    print(mins)
    date = date + timedelta(hours=hrs, minutes=mins)
    return date

slugs = {'ISO/IEC JTC 1/SC 42/WG 3':'wg3',
            'ISO/IEC JTC 1/SC 42/JWG 2':'jwg2'}

for _slug in slugs:
    slug = slugs[_slug]
    cal = Calendar()
    cal.add('prodid', '-//Dragonfly//ISO_Meetings' + slug + '//')
    cal.add('version', '2.0')

    with open('in.csv', 'rt') as csvfile:
        print("Reading file")
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        event_count = 0
        n = -1
        for row in reader:
            n = n + 1
            if n == 2:
                keys = row
                print("Keys: " + str(keys))
            if n > 2:
                e = dict(zip(keys, row))

                if e['Registration'] != "" and e['Host'] != "" and e['Affiliation'] == _slug:
                    print("Criteria met")
                    event = Event()
                    event.add('summary', e['Affiliation'] + e['Project'])
                    print(e['date'])
                    mins = 120
                    if e['dur [min]'] != "":
                        mins = int(e['dur [min]'])
                        print("meeting len " + str(mins))

                    start_date = datetime.strptime(e['date'] + '+0000', "%Y-%m-%d%z")
                    start_time = get_start_time(start_date, e['UTC slot'])
                    print('start time: ' + str(start_time))
                    event.add('dtstamp', datetime.now())
                    event.add('uid', slug + start_time.isoformat())
                    event.add('dtstart', start_time)
                    event.add('dtend',  start_time + timedelta(minutes=mins))
                    event.add('location', e['Registration'] )
                    event.add('description', 'Host: ' + e['Host'] + "\nPlease refer to the registration URL for the connection details: " + e['Registration'])
                    print(event)

                    event_count = event_count + 1
                    cal.add_component(event)

    f = open(slug + '_meetings.ics', 'wb')
    f.write(cal.to_ical())
    f.close()
    print("Added events: ", event_count)
