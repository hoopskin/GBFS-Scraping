import requests, os, csv, time, json, datetime

def pullFullGBFSList():
    resp = requests.get("https://raw.githubusercontent.com/NABSA/gbfs/master/systems.csv")
    data = list(csv.reader(resp.text.split("\n")))
    data = [row for row in data if len(row) == len(data[0])]

    return data

def captureDataURLs(d):
    #We need to jump into data and maybe into an 'en'
    #print(d.keys())
    d = d['data']
    try:
        d = d['en']
    except(KeyError):
        pass

    #print(d.keys())
    return {feedDict['name']: feedDict['url'] for feedDict in d['feeds']}

def captureFeed(outputFolder, feedURL, checkForSkipping=False, buildFolders=True):
    if (checkForSkipping):
        try:
            if (len(os.listdir(os.curdir+"/"+outputFolder)) == 0):
                #This has failed before. SKIP!
                print("\tSkipping!")
                return "Error"
        except(FileNotFoundError):
            #This foler hasn't been made because the system failed. SKIP!
            print("\tSkipping!")
            return "Error"

    try:
        resp = requests.get(feedURL)
        data = resp.json()
    except(KeyboardInterrupt):
        exit()
    except(Exception):
        print("\tERROR!")
        return "Error"

    if "error" in data.keys():
        print("\tERROR!")
        return "Error"
    nowDtStr = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d_%H_%M_%S")
    if buildFolders:
        os.makedirs(outputFolder, exist_ok=True)
    json.dump(data, open(outputFolder+"/"+nowDtStr+".json", "wt"))
    return "Success"

def discoverData(outputFolder, autoDiscURL):
    try:
        resp = requests.get(autoDiscURL)
    except(Exception):
        return "Error"
    dataURLDict = captureDataURLs(resp.json())

    for feedName, feedURL in dataURLDict.items():
        print("\t"+feedName)
        os.makedirs(outputFolder+"/"+feedName, exist_ok=True)
        if captureFeed(outputFolder+"/"+feedName, feedURL) == "Error":
            return "Error"

    return "Success"

def detFreqDataDict(urlCsvData):
    header = urlCsvData[0]
    urlCsvData = [row for row in urlCsvData[1:] if row[header.index("Feed")] != 'Auto-Discovery']

    #{'h/m/l': [['sysId', 'feedId', 'URL'], [...]]}
    rtn = {"High": [], "Medium": [], "Low": []}

    lowFeeds = ['gbfs', 'system_information', 'system_hours', 'system_calendar', 'system_regions', 'system_pricing_plans', 'system_alerts', 'system regions']
    mediumFeeds = ['station_status', 'station_information']
    highFeeds = ['dc', 'free_bike_status']

    for row in urlCsvData:
        feedId = row[header.index("Feed")]
        if feedId in lowFeeds:
            rtn['Low'].append(row)
        elif feedId in mediumFeeds:
            rtn['Medium'].append(row)
        elif feedId in highFeeds:
            rtn['High'].append(row)
        else:
            print("WARN: Found [%s] Feed. Placing in Low" % (feedId))

    return rtn

def pullGroup(lowIdx, medIdx, highIdx, curFreq, dataList):
    for systemId, feedId, feedURL in dataList:
        print("%i\t%i\t%i\t| %s - %s" % (lowIdx+1, medIdx+1, highIdx+1, systemId, feedId))
        captureFeed("data/"+systemId+"/"+feedId, feedURL)

def main_pullAll():
    data = pullFullGBFSList()
    header = data[0]
    data = data[1:]

    systemIdToURL = {row[header.index("System ID")].replace(" ","_"): row[header.index("Auto-Discovery URL")] for row in data if row[header.index("Country Code")] == "US"}


    #Bird DC doesn't exist in the list and doesn't have an auto-discover URL. Need to run manually
    print("bird")
    print("\tdc")
    os.makedirs("data/bird/dc", exist_ok=True)
    captureFeed("data/bird/dc", "http://gbfs.bird.co/dc", checkForSkipping=False)

    for systemId, autoDiscURL in systemIdToURL.items():
        print(systemId+"\t"+autoDiscURL)
        os.makedirs("data/"+systemId, exist_ok=True)
        discoverData("data/"+systemId, autoDiscURL)

def main_highFreqPull():
    #Read in URL CSV
    #urlCsvData = list(csv.reader(open("feedURLData.csv", "rt")))
    #urlCsvData = list(csv.reader(open("feedURLData_2.csv", "rt")))
    urlCsvData = list(csv.reader(open("feedURLData_3.csv", "rt")))

    #Figure out which are going to 'high', 'med', and 'low' frequency
    freqDataDict = detFreqDataDict(urlCsvData)

    #Start pulling in that style
    #Let's start with just 10 concurrent circles of pulls.

    for lowFreqIdx in range(100):
        for medFreqIdx in range(10):
            for highFreqIdx in range(10):
                startDT = datetime.datetime.now()
                pullGroup(lowFreqIdx, medFreqIdx, highFreqIdx, 'High', freqDataDict['High'])
                print("Finished %s in %i seconds" % ('High', (datetime.datetime.now()-startDT).seconds))
            startDT = datetime.datetime.now()
            pullGroup(lowFreqIdx, medFreqIdx, highFreqIdx, 'Medium', freqDataDict['Medium'])
            print("Finished %s in %i seconds" % ('Medium', (datetime.datetime.now()-startDT).seconds))
        startDT = datetime.datetime.now()
        pullGroup(lowFreqIdx, medFreqIdx, highFreqIdx, 'Low', freqDataDict['Low'])
        print("Finished %s in %i seconds" % ('Low', (datetime.datetime.now()-startDT).seconds))

def main():
    if True:
        main_highFreqPull()
    else:
        main_pullAll()

while True:
    print("")
    print(datetime.datetime.now())
    print("")
    main()
