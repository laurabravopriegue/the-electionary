# Program to show intensity of Trump tweets over time
# as a histogram

import json
import datetime as dt
import time
import matplotlib.pyplot as plt


def text_to_datetime(dateString):
    month = dateString[4:7]
    day = dateString[8:10]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
              "Nov", "Dec"]
    month = int(months.index(month) + 1)
    return dt.date(2016, month, int(day))

with open('trumpStatuses.json', 'r') as f:
    trumpStatuses = json.load(f)

timesList = []

for status in trumpStatuses:
    print status['text']
    print status['created_at']
    dtDate = text_to_datetime(status['created_at'])
    dtDateInt = time.mktime(dtDate.timetuple())
    timesList.append(dtDateInt)

plt.hist(timesList, bins=30)
plt.show()