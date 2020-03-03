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
    try:
        return {feedDict['name']: feedDict['url'] for feedDict in d['feeds']}
    except(KeyError):
        return {feedDict['name']: feedDict['url'] for feedDict in d['chicago-gbfs']['feeds']}

def discoverData(outputFolder, autoDiscURL):
    try:
        resp = requests.get(autoDiscURL)
        dataURLDict = captureDataURLs(resp.json())
    except(requests.exceptions.ConnectionError):
        print("\trequests.exceptions.ConnectionError")
        print("\t"+autoDiscURL)
        dataURLDict = {}
    except(KeyError):
        print("\tKeyError")
        print("\t"+autoDiscURL)
        dataURLDict = {}
    except(json.decoder.JSONDecodeError):
        print("\tjson.decoder.JSONDecodeError")
        print("\t"+autoDiscURL)
        dataURLDict = {}


    return dataURLDict

def main():
    oFileWriter = csv.writer(open("feedURLData_3.csv", "wt"), lineterminator='\n')
    oFileWriter.writerow(['System ID', 'Feed', 'URL'])
    data = pullFullGBFSList()
    header = data[0]
    data = data[1:]

    systemIdToURL = {row[header.index("System ID")].replace(" ","_"): row[header.index("Auto-Discovery URL")] for row in data if row[header.index("Country Code")] == "US"}


    #Bird DC doesn't exist in the list and doesn't have an auto-discover URL. Need to run manually
    print('bird')
    oFileWriter.writerow(['bird', 'dc', "http://gbfs.bird.co/dc"])

    for systemId, autoDiscURL in systemIdToURL.items():
        print(systemId)
        oFileWriter.writerow([systemId, 'Auto-Discovery', autoDiscURL])
        feedURLDict = discoverData("data/"+systemId, autoDiscURL)
        for feedName, feedURL in feedURLDict.items():
            oFileWriter.writerow([systemId, feedName, feedURL])

main()
