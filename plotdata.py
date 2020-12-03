#!/usr/bin/python3

import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import datetime
import csv
import sys
import pycurl
import sys
from scipy.interpolate import Rbf

#setting
link = 'http://weather.uwyo.edu/cgi-bin/sounding?'
savedatadir = 'raw'
stasiunfile = 'stasiun.dat'
failkeyword = "Can't get"
indexkeyword = ['Convective Available Potential Energy:', 'K index:']

#cek argumen
if len(sys.argv) < 2:
	print('argumen tidak lengkap')
	exit()

try:
	int(sys.argv[1])
except ValueError:
	print('argumen tidak valid')
	exit()

if int(sys.argv[1]) > len(indexkeyword) - 1:
	print('argumen tidak valid')
	exit()

plotchoice = int(sys.argv[1])

allstasiun = open(stasiunfile, 'r')
liststasiun = csv.reader(allstasiun)

#collect data
tableplot = []
allstasiun.seek(0)
for stasiun in liststasiun:
	rawdatafile = open(savedatadir+'/'+stasiun[1])
	rawdata = rawdatafile.read()
	rawdataarray = rawdata.split('\n')
	for i in range(len(rawdataarray)):
		if indexkeyword[plotchoice] in rawdataarray[i]:
			#print(rawdataarray[i])
			awal = rawdataarray[i].find(indexkeyword[plotchoice])
			tableplot.append([float(stasiun[-2]), float(stasiun[-1]), float(rawdataarray[i][awal+len(indexkeyword[plotchoice]):])])
			break
tableplot = np.asarray(tableplot)

###########
#plot time#
###########
xi = np.arange(95, 140.02, 0.02)
yi = np.arange(-11, 6.02, 0.02)
X,Y = np.meshgrid(xi,yi)

#Creating the interpolation function and populating the output matrix value
rbf = Rbf(tableplot[1], tableplot[0], tableplot[2], function='inverse')
zi = rbf(X, Y)
print(np.shape(zi))
print(zi, np.max(zi))

fig, ax = plt.subplots()
CS = ax.contour(X, Y, zi, 6,
                 linewidths=np.arange(.5, 4, .5),
                 colors=('r', 'green', 'blue', (1, 1, 0), '#afeeee', '0.5')
                 )
ax.clabel(CS, fontsize=9, inline=1)
ax.set_title('IS IT WORK?')
plt.show()
