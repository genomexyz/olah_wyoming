import numpy as np
import datetime
import csv
import sys
import pycurl
import sys

#setting
link = 'http://weather.uwyo.edu/cgi-bin/sounding?'
savedatadir = 'raw_wiii'
stasiunfile = 'stasiun.dat'
failkeyword = "Can't get"
TYPE = 'TEXT%3ALIST'

#contoh
#http://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR=2019&MONTH=02&FROM=0512&TO=0512&STNM=96737

#t = ContentCallback()
#curlObj = pycurl.Curl()
#curlObj.setopt(curlObj.URL, alamatweb)
#curlObj.setopt(curlObj.WRITEFUNCTION, t.content_callback)
#curlObj.perform()
#curlObj.close()

#array = t.contents

class ContentCallback:
	def __init__(self):
		self.contents = ''

	def content_callback(self, buf):
		self.contents = self.contents + buf.decode('utf-8')

allstasiun = open(stasiunfile, 'r')
liststasiun = csv.reader(allstasiun)

#sekarang = datetime.datetime.utcnow()
#tahunsekarang = sekarang.strftime('%Y')
#bulansekarang = sekarang.strftime('%m')
#harisekarang = sekarang.strftime('%d')
#jamsekarang = sekarang.strftime('%H')

if len(sys.argv) < 5:
	print('argument tidak lengkap')
	exit()

tahunsekarang = sys.argv[1]
bulansekarang = sys.argv[2]
harisekarang = sys.argv[3]
jamsekarang = sys.argv[4]

#jam selection
jamsekarangint = int(jamsekarang)
if jamsekarangint < 13:
	jam = '00'
else:
	jam = '12'


print(tahunsekarang, bulansekarang, harisekarang, jamsekarang)
for stasiun in liststasiun:
	waktu = tahunsekarang+'-'+bulansekarang+'-'+harisekarang+' '+jamsekarang+'\n'
	query = link
	query += 'TYPE='+TYPE+'&STNM='+stasiun[0]+'&YEAR='+tahunsekarang+'&MONTH='+bulansekarang+'&FROM='+harisekarang+jam+\
	'&TO='+harisekarang+jam
	savedata = open(savedatadir+'/'+stasiun[1]+'-'+tahunsekarang+bulansekarang+harisekarang+jamsekarang, 'w')

	t = ContentCallback()
	curlObj = pycurl.Curl()
	curlObj.setopt(curlObj.URL, query)
	curlObj.setopt(curlObj.WRITEFUNCTION, t.content_callback)
	curlObj.perform()
	curlObj.close()

	dataall = t.contents
	savedata.write(waktu+dataall)
	savedata.close()

	print(query)
