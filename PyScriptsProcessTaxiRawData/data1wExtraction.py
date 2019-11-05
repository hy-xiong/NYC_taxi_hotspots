'''
Created on Apr 18, 2016

@author: hxiong
'''

import csv, os
import datetime as dt

taxi = ["yellow_tripdata", "green_tripdata"]
year = 2015
month = 1
srcDir = r'C:\Users\hxiong\Desktop\TaxiData'
fileName = "{0:s}_{1:d}-{2:02d}.csv".format(taxi[0], year, month)
dstDir = r'C:\Users\hxiong\Desktop\TaxiData1w'

csv_pickupTime_colNum = 1
csv_dropoffTime_colNum = 2
csv_pickupLat_colNum = 5
csv_pickupLon_colNum = 6
csv_dropoffLat_colNum = 9
csv_dropoffLon_colNum = 10

timeInterval = dt.timedelta(hours = 3)
start_datetime = dt.datetime(year, month, 1, 0, 0, 0) + dt.timedelta(days = 7 - dt.datetime(year, month, 1, 0, 0, 0).weekday())
end_datatime = start_datetime + dt.timedelta(days = 7)


pickup_Records = [] # 1 record: [lat, lon, datetime]
dropoff_Records = [] # 1 record: [lat, lon, datetime]
with open(os.path.join(srcDir, fileName), 'rb') as csvfile:
    r = csv.reader(csvfile, delimiter=',', quotechar='|')
    r.next()
    for row in r:
        pickupTime = dt.datetime.strptime(row[csv_pickupTime_colNum], '%Y-%m-%d %H:%M:%S')
        dropoffTime = dt.datetime.strptime(row[csv_dropoffTime_colNum], '%Y-%m-%d %H:%M:%S')
        if(pickupTime > start_datetime and pickupTime < end_datatime):
            pickup_Records.append([float(row[csv_pickupLat_colNum]), float(row[csv_pickupLon_colNum]), pickupTime])
        if(dropoffTime > start_datetime and dropoffTime < end_datatime):
            dropoff_Records.append([float(row[csv_dropoffLat_colNum]), float(row[csv_dropoffLon_colNum]), dropoffTime])

def writeCsv(dstDir, fileName, data):
    with open(os.path.join(dstDir, fileName), 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["lat", "lon", "dateTime"])
        for row in data:
            spamwriter.writerow([row[0], row[1], row[2].strftime('%Y-%m-%d %H:%M:%S')])

writeCsv(dstDir, 'pickup_%s_to_%s.csv' % (start_datetime.strftime('%Y_%m_%d'), end_datatime.strftime('%Y_%m_%d')), pickup_Records)
writeCsv(dstDir, 'dropoff_%s_to_%s.csv' % (start_datetime.strftime('%Y_%m_%d'), end_datatime.strftime('%Y_%m_%d')), dropoff_Records)