import os, json, csv
from haversine import haversine, Unit

#Overall the thought is that we'd append to a few(?) CSVs the data from "data" folder.
#Then afterwards it could be deleted

#We'll only do "free_bike_status" since it's our only High Freq (other than "dc")
#Also starting on just "austin_scooter_jump_system"

def convertBikeListToDict(prevJson, curJson, nextJson):
    prevDict, curDict, nextDict = {}, {}, {}

    keysToPull = ["lat", "lon", "is_reserved", "is_disabled", "jump_vehicle_type", "jump_ebike_battery_level", "jump_vehicle_name"]

    for rtnDict, bikeList in zip([prevDict, curDict, nextDict], [prevJson, curJson, nextJson]):
        for bike in bikeList:
            rtnDict[bike['bike_id']] = {}
            for k in keysToPull:
                rtnDict[bike['bike_id']][k] = bike[k]

    return prevDict, curDict, nextDict

def hasAnyChange(prevBikeData, curBikeData, nextBikeData):
    rtn = False
    for k in curBikeData:
        if prevBikeData[k] == curBikeData[k] == nextBikeData[k]:
            pass
        else:
            rtn = True
            break

    return rtn

def main():
    projectFolder = "austin_scooter_jump_system"
    dataFolder = "free_bike_status"

    fileList = ["data/"+projectFolder+"/"+dataFolder+"/"+f for f in os.listdir(os.curdir+"/data/"+projectFolder+"/"+dataFolder)]
    fileList.sort()

    outputWriter = csv.writer(open(projectFolder+"__"+dataFolder+".csv", "wt"), lineterminator='\n')
    outputHeader = ["bike_id", "lat", "lon", "is_reserved", "is_disabled", \
                    "jump_vehicle_type", "jump_ebike_battery_level", "jump_vehicle_name", \
                    "prev_lat", "prev_lon", "prev_jump_ebike_battery_level", "next_lat", \
                    "next_lon", "next_jump_ebike_battery_level", "prev_haversine", "next_haversine", \
                    "prev_timestamp", "cur_timestamp", "next_timestamp"]

    outputWriter.writerow(outputHeader)

    for curIdx in range(1, len(fileList)-1):
        print(curIdx)
        prevIdx = curIdx-1
        nextIdx = curIdx+1

        prevJson = json.load(open(fileList[prevIdx], 'rt'))['data']['bikes']
        curJson = json.load(open(fileList[curIdx], 'rt'))['data']['bikes']
        nextJson = json.load(open(fileList[nextIdx], 'rt'))['data']['bikes']

        prevDict, curDict, nextDict = convertBikeListToDict(prevJson, curJson, nextJson)

        for bikeId, curBikeData in curDict.items():
            #try:
            #    if not hasAnyChange(prevDict[bikeId], curBikeData, nextDict[bikeId]):
            #        continue
            #except(KeyError):
            #    pass
            oRow = [bikeId]
            for oHeader in outputHeader[1:8]:
                oRow.append(curBikeData[oHeader])

            try:
                oRow.append(prevDict[bikeId]['lat'])
                oRow.append(prevDict[bikeId]['lon'])
                oRow.append(prevDict[bikeId]['jump_ebike_battery_level'])
            except(KeyError):
                oRow.extend(['', '', ''])

            try:
                oRow.append(nextDict[bikeId]['lat'])
                oRow.append(nextDict[bikeId]['lon'])
                oRow.append(nextDict[bikeId]['jump_ebike_battery_level'])
            except(KeyError):
                oRow.extend(['', '', ''])


            curPoint = (curBikeData['lat'], curBikeData['lon'])

            try:
                prevPoint = (prevDict[bikeId]['lat'], prevDict[bikeId]['lon'])
                oRow.append(haversine(prevPoint, curPoint, unit=Unit.MILES))
            except(KeyError):
                oRow.append("")

            try:
                nextPoint = (nextDict[bikeId]['lat'], nextDict[bikeId]['lon'])
                oRow.append(haversine(curPoint, nextPoint, unit=Unit.MILES))
            except(KeyError):
                oRow.append("")

            startFilterIdx = len(projectFolder)+len(dataFolder)+len("data/")+2

            oRow.extend([fileList[prevIdx][startFilterIdx:-5], fileList[curIdx][startFilterIdx:-5], fileList[nextIdx][startFilterIdx:-5]])

            outputWriter.writerow(oRow)

main()
