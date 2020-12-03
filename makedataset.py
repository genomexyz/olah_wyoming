#!/usr/bin/python3

import numpy as np
import datetime
import csv
import sys
import pycurl
import sys
import glob

#setting
tahun = '2017'
datadir = 'data2017'
stasiunfile = 'stasiun.dat'
compiledir = 'datacompile'
failkeyword = ["Can't get"]
indexkeyword = ['Convective Available Potential Energy:', 'K index:', 'Cross totals index:', 'Vertical totals index:', 
'Lifted index:', 'Showalter index:']
thresholdlen = 100

def checkdatavalid(rawdata):
	valid = True
	for i in range(len(failkeyword)):
		if failkeyword[i] in rawdata:
			valid = False
	for i in range(len(indexkeyword)):
		if not indexkeyword[i] in rawdata:
			valid = False
	if len(rawdata) < thresholdlen:
		valid = False
	return valid

def extractvalue(rawdata):
	listvalue = []
	rawdataarray = rawdata.split('\n')
	for i in range(len(indexkeyword)):
		for j in range(len(rawdataarray)):
			if indexkeyword[i] in rawdataarray[j]:
				awal = rawdataarray[j].find(indexkeyword[i])
				value = float(rawdataarray[j][awal+len(indexkeyword[i]):])
				listvalue.append(value)
				break
	return listvalue

allstasiun = open(stasiunfile, 'r')
liststasiun = csv.reader(allstasiun)


for stasiun in liststasiun:
	print('now processing '+stasiun[1])
	simpandata = open(compiledir+'/'+stasiun[1], 'w')
	listing = glob.glob(datadir+'/'+stasiun[1]+'-*')
	for dataraw in listing:
		print(dataraw)
		datarawopen = open(dataraw)
		extractdataraw = datarawopen.read()
		if not checkdatavalid(extractdataraw):
			datarawopen.close()
			continue
		else:
			valuecol = extractvalue(extractdataraw)
			for i in range(len(valuecol)):
				if i == len(valuecol) - 1:
					simpandata.write(str(valuecol[i]))
				else:
					simpandata.write(str(valuecol[i])+',')
			simpandata.write('\n')
	simpandata.close()

