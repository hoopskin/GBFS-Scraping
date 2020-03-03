import os

folderList = ["data/"+f for f in os.listdir(os.curdir+"/data") if f not in ['.DS_Store']]

for folderName in folderList:
	freeBikePath = folderName+"/free_bike_status"
	try:
		fileList = [freeBikePath+"/"+f for f in os.listdir(os.curdir+"/"+freeBikePath)]
	except(FileNotFoundError):
		continue
	if fileList == []:
		continue
	txt = list(open(fileList[0], 'rt'))[0]

	#if (txt.find("battery") != -1) and (txt.find("lat") != -1):
	#	print(folderName)

	print("%r\t%r\t%s" % (txt.find("battery") != -1, txt.find("lat") != -1, folderName))