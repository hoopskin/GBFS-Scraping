import json, os, csv

def main():
    companyFolder = "washington_dc_bike_jump_system"
    dataFolder = "data/%s/free_bike_status" % (companyFolder)
    fileList = [dataFolder+"/"+f for f in os.listdir(os.curdir+"/"+dataFolder)]
    fileList.sort()

    outputData = []
    outputHeader = ['timestamp', 'bike_id', "jump_vehicle_name", 'lat', 'lon', 'is_reserved', 'is_disabled', 'jump_ebike_battery_level', 'jump_vehicle_type']
    outputData.append(outputHeader)

    i = 0
    j = len(fileList)
    for fileName in fileList:
        i+=1
        print("%i / %i = %.2f%%\t%s" % (i, j, (i/j)*100, fileName))
        inputData = json.load(open(fileName, 'rt'))
        for bikeData in inputData['data']['bikes']:
            oRow = [fileName[fileName.rindex("/")+1:fileName.index(".")]]
            for header in outputHeader[1:]:
                oRow.append(bikeData[header])
            outputData.append(oRow)

    oWriter = csv.writer(open("combinedData.csv", "wt"), lineterminator='\n')
    for oRow in outputData:
        oWriter.writerow(oRow)

main()
