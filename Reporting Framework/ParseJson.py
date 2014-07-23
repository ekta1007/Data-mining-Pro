# Author : Ekta Grover, 08/04/2014
#  Paser to feed the aggregated numbers for the reporting & simulation framework

import json
import csv
import urllib2 , urllib
from pprint import pprint
from dateutil import rrule, parser
import simplejson
import urllib2
import simplejson
import requests


def date_range(start_date,end_date) :
    dates = list(rrule.rrule(rrule.DAILY, dtstart=parser.parse(start_date), until=parser.parse(end_date)))
    date_range=[]
    for i in range(0,len(dates)):
        date_range.append(str(dates[i]).split(" ")[0])
    return date_range
# storing list of all dates
start_date,end_date='2014-03-01','2014-04-07'
date_range=date_range(start_date,end_date)

# write this data to the csv file
filehandle="C:/Users/Ekta.Grover/Desktop/Simulation_DataFeed1.csv"
label_exchange=['Mopub','Smaato','Nexage','Google-Adx']
domain=['nyc','ams','wdc','hkg']
exchange=['mopub','smaato','nexage','googleadx']


with open (filehandle,"wb") as outfile:
    mywriter = csv.writer(outfile)
    head = ("Day","Exchange", "Bid Requests", "Bid response" , "Bids wons" , "No bids", "Total spent on win bids")
    mywriter.writerow(head)
    for i in range(0,len(exchange)) :
        for day in date_range:
            url="http://"+domain[i]+"-dsp.adnear.net/platform/api.php?act=redisanalytics-bidder&date="+day+"&ex="+exchange[i]
            r = requests.get(url)
            data =r.json()
            #print data
            mywriter.writerow([day,exchange[i],data["bidrequests"], data["bids"], data["wonbids"],data["nobids"],float(data["amt.wonbids"])/float(100000)])
print 'Finished writing the csv file '
