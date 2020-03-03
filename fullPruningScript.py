import pandas as pd
import numpy as np
import os, json, datetime, hashlib

thisRunFolderName = datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d__%H_%M_%S")
os.makedirs("pruned_data/"+thisRunFolderName)

print("Starting...")
projNames = ["data/"+projectFolder for projectFolder in os.listdir(os.curdir+"/data")]
projNames.sort()

print("Building Data Folder List...")
folderList = []
pruneList = []
for projName in projNames:
    for dataFolder in os.listdir(os.curdir+"/"+projName):
        folderList.append(projName+"/"+dataFolder)

for folder in folderList:
    if folder.find(".DS_Store") != -1:
        continue
    touchedFileList = []
    print("%i / %i = %.2f%%\t%s" % (folderList.index(folder), len(folderList), (folderList.index(folder)/len(folderList))*100, folder))
    print("\tBuilding Data List...")
    dataList = []
    fileList = os.listdir(os.curdir+'/'+folder)
    for fileName in fileList:
        print("\t\tBuilding Data List %i / %i = %.2f%%" % (fileList.index(fileName), len(fileList), (fileList.index(fileName)/len(fileList))*100))
        filePath = folder+"/"+fileName
        touchedFileList.append(filePath)
        j = json.load(open(filePath, 'rt'))['data']
        if (type(j) == type(None)):
            continue
        if (len(list(j.keys())) == 1):
            j = j[list(j.keys())[0]]
        if j == []:
            continue
        try:
            dataList.append(pd.DataFrame.from_dict(j))
        except(ValueError):
            dataList.append(pd.DataFrame.from_dict({k: [v] for k, v in j.items()}))
        dataList[-1]['timestamp_str'] = fileName[:-5]
    if len(dataList) == 0:
        #userInput = input("\tDelete %i touched files (%.2fMB) [Y/n]: " % (len(touchedFileList), sum([os.stat(f).st_size for f in touchedFileList])/1024/1000))
        userInput = "Y"
        print("\tDelete touched files [Y/n]: Y")
        if userInput.strip().upper() == "Y":
            mbSize = sum([os.stat(f).st_size for f in touchedFileList])/1024/1000
            for fileToDeleteIdx in range(len(touchedFileList)):
                print("\t\tDeleting Files [%.2fMB]: %i / %i = %.2f%%" % (mbSize, fileToDeleteIdx, len(touchedFileList), (fileToDeleteIdx/len(touchedFileList))*100))
                os.remove(touchedFileList[fileToDeleteIdx])
        continue

    #Wait... can't we just do drop_duplicates instead of hashing? Yes. Yes we can
    print("\tCombining Data List...")
    fullDf = pd.concat(dataList).reset_index(drop=True)
    for colName in fullDf.columns:
        fullDf[colName] = fullDf[colName].astype(str)

    preSize = fullDf.shape[0]
    fullDf.drop_duplicates(fullDf.columns[:-1], inplace=True)
    postSize = fullDf.shape[0]
    print("\tRemoved Duplicates (%i -> %i = %.2f%%)" % (preSize, postSize, ((preSize-postSize)/preSize)*100))

    outputFileName = folder[folder.index("/")+1:].replace("/","__")+".csv"
    fullDf.to_csv("pruned_data/"+thisRunFolderName+"/"+outputFileName, index=False)
    pruneList.append(folder)

    #userInput = input("\tDelete %i touched files (%.2fMB) [Y/n]: " % (len(touchedFileList), sum([os.stat(f).st_size for f in touchedFileList])/1024/1000))
    userInput = "Y"
    print("\tDelete touched files [Y/n]: Y")
    if userInput.strip().upper() == "Y":
        mbSize = sum([os.stat(f).st_size for f in touchedFileList])/1024/1000
        for fileToDeleteIdx in range(len(touchedFileList)):
            print("\t\tDeleting Files [%.2fMB]: %i / %i = %.2f%%" % (mbSize, fileToDeleteIdx, len(touchedFileList), (fileToDeleteIdx/len(touchedFileList))*100))
            os.remove(touchedFileList[fileToDeleteIdx])
