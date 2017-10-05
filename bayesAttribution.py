# value_counts() only works with column in dataframe
#iterate through value_counts Series, use iteritems()

from collections import OrderedDict
import csv
import pandas as pd
import numpy as np

testFile = "Q2Paths.csv"

def openPaths(str1):
	openFile = pd.read_csv(str1, header=0)
	# lastCol = openFile.iloc[:,-1]
	return openFile

def dfCount(str1):
	totalCol = len(str1.columns)
	pathCol = totalCol - 4
	return pathCol

# Sets number of touchpoints as a number at the end of dataframe
def setTP1(dataframe=str):
	dataframe['touchPoints'] = dataframe.count(axis=1)-3

def setTP2(dataframe):
	dataframe['touchPoints'] = dataframe.count(axis=1)-2

# calculate the number of channel specific occurrences controlling for number of touchpoints and the location in path
def chanCountbyPath(tpCount=int, pathNo=int, channel=None):
	if pathNo > tpCount:
		return "Error: Path specified is greater than number of touchpoints."
	elif channel==None:
		prob = df[df['touchPoints']==tpCount]['Path '+str(pathNo)].value_counts()
	else:
		prob = df[(df['touchPoints']==tpCount)&(df['Path '+str(pathNo)]==channel)]['Path '+str(pathNo)].value_counts()
	return prob

# find unique values in a column of the dataframe; returns ndarray without NAN
def unqValues(col=str):
	unq = df[col].unique()
	unq = unq[pd.notnull(unq)]
	return unq

#creates list of Series for each path
def countInPath(tpCount=int):
	count = [df[df['touchPoints']==tpCount]['Path '+str(n)].value_counts() for n in range(1, tpCount+1)]
	return count

#turns pd.Series to lists
def StoL(series):
	l = series.tolist()
	return l

# returns dataframe of value_counts based on number of touchpoints and channels that occur; will need to be modified based on csv input
def pathProb(tpCount=int, breakpoint=int):
	subdf1 = df[df['touchPoints']==tpCount] 
	# subdf1 = subdf1.loc[:,'Conversions':'Path ' + str(tpCount)]
	# setTP2(subdf1)
	# subdf1 = subdf1[subdf1['touchPoints']==tpCount]
	subdfFirst = subdf1.loc[:,'Path 1':'Path ' + str(tpCount-breakpoint)]
	subdfFirstT = [tuple(i) for i in subdfFirst.values]

	subdfSecond = subdf1.loc[:, 'Path ' + str(tpCount-breakpoint+1):'Path '+str(tpCount)]
	subdfSecondT = [tuple(i) for i in subdfSecond.values]

	dfT = pd.DataFrame({'Path Combination 1': subdfFirstT, 'Path Combination 2': subdfSecondT})
	return [subdf1, dfT]

# returns total number of conversions in data set
def tpDictConversions(d):
	conversions = 0
	for i, j in d.items():
		conversions = d[i] + conversions
	return conversions

# calculates when 95% of conversions is reached in the dictionary of touchpoints to conversions
def cPercentage(d):
	cp = 0
	conv = tpDictConversions(d)
	convTar = conv*0.95
	for a, b in d.items():
		print(a,b)
		if cp > convTar:
			return [a, cp]
			break
		else:
			cp += b

df = openPaths(testFile)
setTP1(df)	

# total number of paths in columns, and total number of rows
dfCol = dfCount(df)
dfRows = len(df)

#dictionary where touchpoints # are keys, and conversions are values
uniqueTP = unqValues("touchPoints")
dictdfCount = pd.DataFrame()
dictdfValues = pd.DataFrame()
dictdfCount['touchPoints'] = unqValues('touchPoints')
dictdfValues['touchPoints'] = unqValues('touchPoints')
cCount = [df.loc[df['touchPoints']==i, 'Conversions'].sum() for i in unqValues('touchPoints')]
cValues = [df.loc[df['touchPoints']==i, 'Conversion Value'].sum() for i in unqValues('touchPoints')]

# dictionary of conversions & values
dictdfCount['Conversions'] = cCount
dictdfValues['Values'] = cValues

tpDictCount = dict(zip(dictdfCount.touchPoints, dictdfCount.Conversions))
tpDictValues = dict(zip(dictdfCount.touchPoints, dictdfValues.Values))
#dictionary stop
# 
def unqValues1(col=str):
	unq = subdfFirstT[col].unique()
	unq = unq[pd.notnull(unq)]
	return unq

# # Need to revise hardocde temptp; possibly all junk code
# temptp=5
# subdf1 = df[df['touchPoints']==temptp]
# subdfFirst = subdf1.loc[:,'Conversions':'Path ' + str(temptp)]
# subdfFirstT = pd.DataFrame()
# subdfFirstT['Conversions'] = subdfFirst['Conversions']
# x= [tuple(i) for i in subdfFirst.loc[:, 'Path 1':'Path '+str(temptp)].values]
# subdfFirstT['Paths']=x
# pValues = [[i,subdfFirstT.loc[subdfFirstT['Paths']==i, 'Conversions'].sum()] for i in unqValues1('Paths')]
# export = pValues
# print(pValues)

conversions = tpDictConversions(tpDictCount)
# print((tpDictCount))

# for i, j in tpDictCount.items():
# 	# print(i,j)
# 	seriesPaths = pathProb(i, i-1)[1]
# 	# print(seriesPaths)
# 	tpSeries = seriesPaths['Path Combination 1'].value_counts()
# 	# print(tpSeries)
# 	for one, two in tpSeries.iteritems():
# 		pTps = j/i
# 		#i = touchpoints; one =channel; two = ; valueee = actual value of that channel
# 		valueee = ((int(two)/j)*tpDictValues[i])*pTps
# 		# print(i, one, two, valueee)

tpDictValues = OrderedDict(sorted(tpDictValues.items()))
tpDictCount = OrderedDict(sorted(tpDictCount.items()))

# print(df[(df['Path 1']=='PaidSearch')&(df['Path 2']=='OrganicSearch')].sum())

##Shows the touch point and number of conversions to achieve a certain percentage of efficiency
# print(cPercentage(tpDictCount))

# print(df[df['touchPoints']==2]['Path 1'].value_counts())

attribution_value = []
touch_points = []
channel1 = []
channel_count_in_tp_by_pos = []
for i, j in tpDictCount.items():
	if i < 300:
		for p in range(i):
			tpSeries = df[df['touchPoints']==i]['Path '+ str(p+1)].value_counts()
			# print(tpSeries)
			for one, two in tpSeries.iteritems():
				pTps = 1/i
				#one = channel; i = touch points; 

				valueee = ((two/j)*tpDictValues[i])*pTps
				# print(two, j, tpDictValues[i], pTps, valueee)	
				touch_points.append(i)
				channel1.append(one)
				channel_count_in_tp_by_pos.append(two)
				attribution_value.append(valueee)
	else:
		break
sumDf = pd.DataFrame()
sumDf['Touch Points'] = touch_points
sumDf['Channel'] = channel1
sumDf['Channel Count in TP by Pos'] = channel_count_in_tp_by_pos
sumDf['Value'] = attribution_value

# print(sumDf)

def unqValues1(col=str):
	unq = sumDf[col].unique()
	unq = unq[pd.notnull(unq)]
	return unq

# export = [[i, sumDf.loc[sumDf['Channel']==i, 'Value'].sum()] for i in unqValues1('Channel')]

# for i in abc:
# 	path = path+1
# 	for channel, rows in i.iteritems():
		# print(path, channel, (rows/dfg))

# subdf = df[df.columns[-5:-1]].stack().value_counts(

# print(df[(df['touchPoints']==4)]['Path 1'].value_counts())

# matrix of touchpoints to be exported as csv
# m = [[i, tpDict[i], tpDict[i]/conversions] for i, j in tpDict.items()]

# # Writes the touchpoints # to percentage in csv
# with open('final.csv', 'w', newline='') as f:
# 	writer = csv.writer(f)
# 	writer.writerows(export)