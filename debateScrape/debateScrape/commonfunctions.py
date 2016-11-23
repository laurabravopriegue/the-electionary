import datetime as dt
from scrapy.selector import Selector


def list_to_item(any_list):
    for item in any_list:
        return item


def iso_to_datetime(iso_string):
    year = int(iso_string[0:4])
    month = int(iso_string[5:7])
    day = int(iso_string[8:10])
    return dt.date(year, month, day)


# This class is a custom version of scrapy's Selector class
# which enables us to include some of our own functions.
class TranscriptSelector(Selector):
    # Function to get the date of the debate.
    def get_debate_date(self):
        date = self.xpath("//span[@class='docdate']/text()").extract()

        debate_date = list_to_item(date)

        # The date is not in a useful format, so let's change that.
        # Some uninteresting code to do that is below.

        debate_date = debate_date.split()
        word_month = debate_date[0]

        debate_date[1] = debate_date[1].split(',')
        day_no = int(debate_date[1][0])
        year_no = int(debate_date[2])

        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        month_no = int(months.index(word_month) + 1)

        # Finally we use the datetime library to store the date as a date object
        # and then convert that to an ISO format date.
        debate_date = dt.date(year_no, month_no, day_no)
        return debate_date.isoformat()

    def get_debate_name(self):
        name = self.xpath("//span[@class='paperstitle']/text()").extract()
        for name in name:
            return name
