#!/usr/bin/python3

import numpy as np
import csv

#setting
datarawfile = 'datahujan/hujan-makassar.csv'
datasoundingfile = 'datacompile/WAAA'

#open data
datarawopen = open(datarawfile)
datarawall = csv.reader(datarawopen)

for dataraw in datarawall:
	for i in range(len(dataraw)):
		if dataraw[i] == '':
			print(dataraw[1])
			break;
