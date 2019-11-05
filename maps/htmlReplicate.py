import datetime as dt
import shutil

filePrefix = ["Dropoff", "Pickup"]
startDt = dt.datetime(2015, 1, 5, 0, 0, 0)
endDt = dt.datetime(2015, 1, 12, 0, 0, 0)
timeInterval = dt.timedelta(hours = 3)
htmlTemplate = "template.html"

for prefix in filePrefix:
    currentTime = startDt
    while(currentTime < endDt):
        htmlfile = '%s_%04d_%02d_%02d_%02dhr.html' % (prefix, currentTime.year, currentTime.month, currentTime.day, currentTime.hour)
        jsonfile = '%s_%04d_%02d_%02d_%02dhr_KD_wihtin_Rec_unprj.json' % (prefix, currentTime.year, currentTime.month, currentTime.day, currentTime.hour)
        shutil.copyfile(htmlTemplate, htmlfile)
        with open(htmlfile, 'r') as rd:
            content = rd.readlines()
        content[21] = "\t\tvar srcJson = \"jsonData/%s\"\n" % jsonfile
        with open(htmlfile, 'w') as wr:
            wr.writelines(content)
        currentTime += timeInterval
