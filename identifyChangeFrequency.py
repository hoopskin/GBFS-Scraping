import os, datetime, json

def levenshteinDistance(s1,s2):
	"""Returns the Levenshtein distance between two strings. Used to check how close they are to each other"""
	if len(s1) > len(s2):
		s1,s2 = s2,s1
	distances = range(len(s1) + 1)
	for index2,char2 in enumerate(s2):
		newDistances = [index2+1]
		for index1,char1 in enumerate(s1):
			if char1 == char2:
				newDistances.append(distances[index1])
			else:
				newDistances.append(1 + min((distances[index1],
											 distances[index1+1],
											 newDistances[-1])))
		distances = newDistances
	return distances[-1]

def whatIsEditDistance(s1, s2): 
	# Find lengths of given strings 
	m = len(s1) 
	n = len(s2) 
	# If difference between lengths is more than 1, 
	# then strings can't be at one distance 
	count = 0	# Count of isEditDistanceOne 
	i = 0
	j = 0
	while i < m and j < n: 
		# If current characters dont match 
		if s1[i] != s2[j]: 
			# If length of one string is 
			# more, then only possible edit 
			# is to remove a character 
			if m > n: 
				i+=1
			elif m < n: 
				j+=1
			else:	# If lengths of both strings is same 
				i+=1
				j+=1
			# Increment count of edits 
			count+=1
		else:	# if current characters match 
			i+=1
			j+=1
	# if last character is extra in any string 
	if i < m or j < n: 
		count+=1
	return count

systemIdList = ["data/"+f for f in os.listdir(os.curdir+"/data")]

for systemId in systemIdList:
	feedList = [systemId+"/"+f for f in os.listdir(os.curdir+"/"+systemId)]
	if (systemId+"/free_bike_status" not in feedList) and (systemId+"/dc" not in feedList):
		continue
	else:
		feedList = [systemId+"/free_bike_status", systemId+"/dc"]
	for feed in feedList:
		try:
			fileList = [feed+"/"+f for f in os.listdir(os.curdir+"/"+feed)]
		except(Exception):
			continue
		
		fileList.sort()

		fileDistList = []

		for secondIdx in range(1, len(fileList)):
			print(feed)
			firstIdx = secondIdx - 1

			firstText = json.load(open(fileList[firstIdx], 'rt'))
			secondText = json.load(open(fileList[secondIdx], 'rt'))

			#If 'data' doesn't exist, SKIP!
			if ("data" not in firstText.keys()) or ("data" not in secondText.keys()):
				continue

			#fileDistList.append(levenshteinDistance(str(firstText['data']), str(secondText['data'])))
			#fileDistList.append(str(firstText['data']) == str(secondText['data']))
			fileDistList.append(whatIsEditDistance(str(firstText['data']), str(secondText['data'])))
			print(fileDistList)
