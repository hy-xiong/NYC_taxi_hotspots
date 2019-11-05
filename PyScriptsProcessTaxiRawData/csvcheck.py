import csv

csv_pickupTime_colNum = 1
csv_dropoffTime_colNum = 2
csv_pickupLat_colNum = 5
csv_pickupLon_colNum = 6
csv_dropoffLat_colNum = 9
csv_dropoffLon_colNum = 10
cline = 1
lines = 3

with open('yellow_tripdata_2015-01.csv', 'rb') as csvfile:
    r = csv.reader(csvfile, delimiter=',', quotechar='|')
    print r.next()
    for row in r:
        if cline < lines:
            print row
            cline += 1
        else:
            break
