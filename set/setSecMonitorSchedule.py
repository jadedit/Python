# pip install apscheduler or python -m pip install apscheduler
# pip install schedule or python -m pip install schedule

import schedule
import time
import os
import datetime
import urllib
import random
from bs4 import BeautifulSoup

def getLogTime():
    return datetime.datetime.now().strftime("%Y%m%d %H%M%S :  ")

def job():
    print("===================================================")
    print(getLogTime() + "Job Name    - setScheduleJob.py")
    print(getLogTime() + "Create Date - 2017-11-02.")
    print("---------------------------------------------------")
    print(getLogTime() + "Start Schedule")
    print(getLogTime() + "Working...")

def getSettradeThailand():
    print(getLogTime() + "Get data from Settrade.")
    os.system("python \"C:\\Python\\set\\setSecURLgrouplistToCsv.py\"")
    time.sleep(10)
    os.system("python \"C:\\Python\\set\\setSecMergeCsv.py\"")

def getUrl():
    url_string = ["http://www.dtac.co.th", "http://www.sanook.com", "https://www.twitter.com", "https://www.facebook.com", "https://www.blognone.com" \
                  , "https://manager.co.th", "http://www.iaumreview.com", "http://siamchart.com/", "https://www.apple.com", "https://www.bualuang.co.th" \
                  , "https://www.facebook.com", "https://www.google.co.th", "http://sritown.com/manga/", "http://www.pantip.com", "https://www.google.com" \
                  , "http://www.ais.co.th"                  ]

    """
    i=0
    for ir in url_string:
        url = ir
        i=i+1
        print(getLogTime() + i.__str__() + " - "+ url)
        time.sleep(1)

        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page, 'lxml')

        table_element_all = soup.findAll('table', class_='table table-info table-hover')
    """
    ir = random.randrange(5) + random.randrange(5)+ random.randrange(4)

    url = url_string[ir]
    print(getLogTime() + ir.__str__())
    print(getLogTime() + url)

    tr = random.randrange(120)
    print(getLogTime() + "Sleep time - " + tr.__str__())
    time.sleep(tr)

    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'lxml')

    table_element_all = soup.findAll('table', class_='table table-info table-hover')
    print(getLogTime() + "Call URL ready.")

# Example
# schedule.every(2).seconds.do(job)
# schedule.every(2).seconds.do(setTrade)
# schedule.every(1).minutes.do(setTrade)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

#------------- MAIN ------------------------------------------------------------------------
job()
#getUrl()
schedule.every(4).minutes.do(getUrl)

# Start Job
schedule.every().day.at("10:02").do(getSettradeThailand)
schedule.every().day.at("10:32").do(getSettradeThailand)
schedule.every().day.at("11:02").do(getSettradeThailand)
schedule.every().day.at("11:32").do(getSettradeThailand)
schedule.every().day.at("12:02").do(getSettradeThailand)
schedule.every().day.at("12:45").do(getSettradeThailand)
schedule.every().day.at("14:33").do(getSettradeThailand)
schedule.every().day.at("15:02").do(getSettradeThailand)
schedule.every().day.at("15:33").do(getSettradeThailand)
schedule.every().day.at("16:03").do(getSettradeThailand)
schedule.every().day.at("16:45").do(getSettradeThailand)

while True:
    schedule.run_pending()
    time.sleep(1)
