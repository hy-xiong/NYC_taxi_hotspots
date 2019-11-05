'''
Created on Apr 19, 2016

@author: finix429
'''

import arcpy, os, shapefile
from arcpy.sa import *
from json import dumps

srcRoot = r'D:\Dropbox\Homework\GeoVisualization\Prj'
srcCsvDir = os.path.join(srcRoot, 'Data', 'TaxiData1w_3hSplit')
boundaryShapefile = os.path.join(srcRoot, 'Data', 'nyc', 'NYC_Boundary.shp')
jsonFolder = os.path.join(srcRoot, 'json')

sratchRoot = r'C:\Users\Finix\Desktop\prj'
tempFolder = os.path.join(sratchRoot, 'temp')
tempGDB = os.path.join(sratchRoot, 'temp.gdb')


fileNamePrefixs = ["Dropoff", "Pickup"]
NClass = 7

arcpy.CheckOutExtension("Spatial")
arcpy.env.extent = arcpy.Describe(boundaryShapefile).extent
csvfiles = os.listdir(srcCsvDir)

def shp2json(shpFile, dstDir):
    reader = shapefile.Reader(shpFile)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    jbuffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        jbuffer.append(dict(type="Feature", geometry=geom, properties=atr)) 
    # write the GeoJSON file
    geojson = open(os.path.join(dstDir, "%s.json" % os.path.basename(shpFile).split('.')[0]), "w")
    geojson.write(dumps({"type": "FeatureCollection", "features": jbuffer}, indent=2) + "\n")

for fileNamePrefix in fileNamePrefixs:
    kernelDensityRasterFileList = []
    for fileBasename in os.listdir(srcCsvDir):
        if fileNamePrefix in fileBasename:
            csvPath = os.path.join(srcCsvDir, fileBasename)
            csvLayer = os.path.join(tempFolder, '%s.lyr' % fileBasename.split('.')[0])
            csvPrjShapfile = os.path.join(tempGDB, '%s_prj' % fileBasename.split('.')[0])
            csvPrjLayer = os.path.join(tempFolder, '%s_prj.lyr' % fileBasename.split('.')[0])
            withinBoundaryPtsShapefile = os.path.join(tempGDB, '%s_within' % fileBasename.split('.')[0])
            kernelRaster = os.path.join(tempGDB, '%s_KD' % fileBasename.split('.')[0])
            kernelRasterWithin = os.path.join(tempGDB, '%s_KD_wihtin' % fileBasename.split('.')[0])
            files = [csvPrjShapfile, withinBoundaryPtsShapefile, kernelRaster, kernelRasterWithin]
            for f in files:
                if arcpy.Exists(f):
                    arcpy.Delete_management(f)
            sp_geo = arcpy.SpatialReference(4326) # WGS 84
            sp_prj = arcpy.SpatialReference(3857) # WGS 84 Web mercator
            arcpy.MakeXYEventLayer_management(csvPath, 'lat', 'lon', csvLayer, sp_geo)
            arcpy.Project_management(csvLayer, csvPrjShapfile, sp_prj)
            arcpy.MakeFeatureLayer_management(csvPrjShapfile, csvPrjLayer)
            arcpy.SelectLayerByLocation_management(csvPrjLayer, "WITHIN", boundaryShapefile)
            arcpy.FeatureClassToFeatureClass_conversion(csvPrjLayer, os.path.dirname(withinBoundaryPtsShapefile), os.path.basename(withinBoundaryPtsShapefile))
            outKD = KernelDensity(withinBoundaryPtsShapefile, None, 30)
            outKD.save(kernelRaster)
            outExtractedRaster = ExtractByMask(kernelRaster, boundaryShapefile)
            outExtractedRaster.save(kernelRasterWithin)
            kernelDensityRasterFileList.append(kernelRasterWithin)
    minRasterValueList = [float(arcpy.GetRasterProperties_management(raster, "MINIMUM").getOutput(0)) for raster in kernelDensityRasterFileList]
    maxRasterValueList = [float(arcpy.GetRasterProperties_management(raster, "MAXIMUM").getOutput(0)) for raster in kernelDensityRasterFileList]
    minV = min(minRasterValueList)
    maxV = max(maxRasterValueList)
    print "Min value for {0:s} is: {1:.3f}\nMax value for {0:s} is: {2:.3f}".format(fileNamePrefix, minV, maxV)
    interval = (maxV - minV) * 1.0 / NClass
    breakPt =[minV + interval * i for i in xrange(1, NClass)]
    print "Interval break value for:\n%s\nare:\n" % '\n'.join(kernelDensityRasterFileList),'\n'.join("{0:.3f}".format(v) for v in breakPt), "\n"
    for i in xrange(len(kernelDensityRasterFileList)):
        rasterRemapRange = []
        startClassIndex = 0
        endClassIndex = 0
        for breakptV in breakPt:
            if(breakptV < minRasterValueList[i]):
                startClassIndex += 1
            if(breakptV < maxRasterValueList[i]):
                endClassIndex += 1
        for j in xrange(startClassIndex, endClassIndex + 1):
            if(j == startClassIndex):
                rasterRemapRange.append([minRasterValueList[i] - 1.0, breakPt[j], j + 1])
            elif(j == endClassIndex):
                rasterRemapRange.append([breakPt[j-1], maxRasterValueList[i] + 1.0, j + 1])
            else:
                rasterRemapRange.append([breakPt[j-1], breakPt[j], j + 1])
#         print "{0}'s reclassification break is:\n{1}".format(kernelDensityRasterFileList[i], '\n'.join(str(l) for l in rasterRemapRange)), '\n'
        outReclassify = Reclassify(kernelDensityRasterFileList[i], "Value", RemapRange(rasterRemapRange), "NODATA")
        RecRaster = os.path.join(tempGDB, "{0}_Rec".format(kernelDensityRasterFileList[i]))
        if(arcpy.Exists(RecRaster)):
            arcpy.Delete_management(RecRaster)
        outReclassify.save(RecRaster)
        RecShp = os.path.join(tempFolder, "{0}.shp".format(os.path.basename(RecRaster)))
        if(arcpy.Exists(RecShp)):
            arcpy.Delete_management(RecShp)
        arcpy.RasterToPolygon_conversion(RecRaster, RecShp, "SIMPLIFY", "Value")
        RecShpUprj = os.path.join(tempFolder, "{0}_unprj.shp".format(os.path.basename(RecRaster)))
        if(arcpy.Exists(RecShpUprj)):
            arcpy.Delete_management(RecShpUprj)
        arcpy.Project_management(RecShp, RecShpUprj, sp_geo)
        shp2json(RecShpUprj, jsonFolder)
    with open(os.path.join(sratchRoot, 'RecReport_%s.txt' % fileNamePrefix), 'w') as f:
        f.write('Class breaks are:\n')
        valueList = [minV]
        valueList.extend(breakPt)
        valueList.append(maxV)
        f.writelines(['%.3f\n' % v for v in valueList])
        f.write('\nFor each kernel density map:\n')
        for i in xrange(len(kernelDensityRasterFileList)):
            f.writelines(['%s\n' % os.path.basename(kernelDensityRasterFileList[i]), 'MaxV:%.3f\n' % maxRasterValueList[i], 'MinV:%.3f\n' % minRasterValueList[i]])
    print "\n\n"