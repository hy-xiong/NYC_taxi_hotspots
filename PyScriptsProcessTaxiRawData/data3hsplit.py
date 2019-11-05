import csv, collections, os
import operator as op
import datetime as dt

def readTaxiRecords(taxicsv):
    records = []
    with open(taxicsv, 'rb') as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='|')
        r.next()
        for row in r:
            lat = float(row[0])
            lon = float(row[1])
            if(lat != 0.0 and lon != 0.0):
                records.append([lat, lon, dt.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')])
    return records

def categorizeTaxiTime(taxiDataList, startTime, endTime, timeInterval):
    categorizedTaxiData = collections.defaultdict(list)
    sortedTaxiDataList = sorted(taxiDataList, key = op.itemgetter(2))
    currentTime = startTime
    for taxiRecord in sortedTaxiDataList:
        if taxiRecord[2] > currentTime:
            while(taxiRecord[2] > currentTime + timeInterval):
                currentTime += timeInterval
            if(currentTime < endTime):
                categorizedTaxiData[currentTime].append(taxiRecord)
    return categorizedTaxiData

def writeCategorizedTaxiDataToCsv(categorizedRecords, dstfolder, safeFileNamePrefix):
    for key, taxiRecordList in categorizedRecords.iteritems():
        safeFileName = '%s_%04d_%02d_%02d_%02dhr.csv' % (safeFileNamePrefix, key.year, key.month, key.day, key.hour)
        with open(os.path.join(dstfolder, safeFileName), 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["lon", "lat", "dateTime"])
            for taxiRecord in taxiRecordList:
                spamwriter.writerow([taxiRecord[1], taxiRecord[0], taxiRecord[2].strftime('%Y-%m-%d %H:%M:%S')])
    
srcDir = r'C:\Users\finix429\Desktop\TaxiData1w'
dstDir = r'C:\Users\finix429\Desktop\TaxiData1w_3hSplit'
pickupcsv = 'pickup_2015_01_05_to_2015_01_12.csv'
dropoffcsv = 'dropoff_2015_01_05_to_2015_01_12.csv'

timeInterval = dt.timedelta(hours = 3)
start_datetime = dt.datetime(2015, 1, 5, 0, 0, 0)
end_datatime = dt.datetime(2015, 1, 12, 0, 0, 0)

pickup_Records = readTaxiRecords(os.path.join(srcDir, pickupcsv)) # 1 record: [lat, lon, datetime]
dropoff_Records = readTaxiRecords(os.path.join(srcDir, dropoffcsv)) # 1 record: [lat, lon, datetime]

categorizedPickupRecords = categorizeTaxiTime(pickup_Records, start_datetime, end_datatime, timeInterval)
writeCategorizedTaxiDataToCsv(categorizedPickupRecords, dstDir, 'Pickup')
categorizedDropoffRecords = categorizeTaxiTime(dropoff_Records, start_datetime, end_datatime, timeInterval)
writeCategorizedTaxiDataToCsv(categorizedDropoffRecords, dstDir, 'Dropoff')
