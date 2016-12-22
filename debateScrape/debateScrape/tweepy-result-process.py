# Program to show intensity of Trump tweets over time
# as a histogram

import json
import datetime as dt
import time
import matplotlib.pyplot as plt


def text_to_datetime(date_string):
    month = date_string[4:7]
    day = date_string[8:10]
    hour = date_string[11:13]
    minute = date_string[14:16]
    second = date_string[17:19]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
              "Nov", "Dec"]
    month = int(months.index(month) + 1)
    return dt.datetime(year=2016, month=month, day=int(day), hour=int(hour), minute=int(minute), second=int(second))


with open('trumpStatusesSample.json', 'r') as f:
    trumpStatuses = json.load(f)

timesList = []

for status in trumpStatuses:
    print status['text']
    print status['created_at']
    dtDate = text_to_datetime(status['created_at'])
    print dtDate.isoformat()


    # Plot a histogram
    # plt.hist(timesList, bins=30)
    # plt.show()
