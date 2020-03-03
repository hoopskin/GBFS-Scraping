import csv, os

pruneFolder = "pruned_data"
dateFolderList = [pruneFolder+"/"+f for f in os.listdir(os.curdir+"/"+pruneFolder) if f != ".DS_Store"]
mergeFolderName = "mergedFiles"

os.makedirs(mergeFolderName, exist_ok=True)

def getFileNameList():
	rtn = []
	for folder in dateFolderList:
		#NOTE: Just doing "f" because we don't want the folder paths. Just the CSV names
		rtn.extend([f for f in os.listdir(os.curdir+"/"+folder)])

	return list(set(rtn))

def buildMergedFile(fileName):
	fullData = []
	for folderName in dateFolderList:
		try:
			folderData = list(csv.reader(open(folderName+"/"+fileName, "rt")))
			if fullData != []:
				folderData = folderData[1:]
			fullData.extend(folderData)
		except(FileNotFoundError):
			continue

	csv.writer(open(mergeFolderName+"/"+fileName, "wt"), lineterminator='\n').writerows(fullData)

def main():
	fileNameList = getFileNameList()
	i = 0
	j = len(fileNameList)
	for fileName in fileNameList:
		i+=1
		print("%i / %i = %.2f%%\t%s" % (i, j, (i/j)*100, fileName))
		buildMergedFile(fileName)

main()