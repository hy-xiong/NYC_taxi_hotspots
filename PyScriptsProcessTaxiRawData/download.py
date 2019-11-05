import urllib2, time

def timer(stTime, edTime):
    """Convert elapsed time from seconds to h:m:s format"""
    hour, remain = divmod(edTime - stTime, 3600)
    minute, second = divmod(remain, 60)
    return "{0:d}:{1:d}:{2:.2f}".format(int(hour),int(minute), second)

site = "https://storage.googleapis.com/tlc-trip-data/2015/"
taxi = ["yellow_tripdata", "green_tripdata"]
year = 2015
stMonth = 12
Months = 1

for m in xrange(stMonth, stMonth + Months):
    st = time.time()
    fileName = "{0:s}_{1:d}-{2:02d}.csv".format(taxi[0], year, m)
    url = "{0:s}{1:s}".format(site, fileName)
    print "Start downloading %s" % fileName
    f = urllib2.urlopen(url)
    data = f.read()
    with open(fileName, 'wb') as fdata:
        fdata.write(data)
    print "Download Complete. %s" % timer(st, time.time())


