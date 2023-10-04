import numpy as np
import datetime
import csv
import sys
import pycurl
import sys

#setting
link = 'http://aviation.bmkg.go.id/latest/metar.php?i=%s&y=%s&m=%s'
savedatadir = 'label_raw'
failkeyword = "Can't get"

class ContentCallback:
	def __init__(self):
		self.contents = ''

	def content_callback(self, buf):
		self.contents = self.contents + buf.decode('utf-8')


if len(sys.argv) < 4:
	print('argument tidak lengkap')
	print('usage: python collect_label.py stasiun tahun bulan')
	exit()

stasiun = sys.argv[1]
tahun = sys.argv[2]
bulan = sys.argv[3]

query = link%(stasiun, tahun, bulan)
savedata = open('%s/%s-%s%s'%(savedatadir, stasiun, tahun, bulan), 'w')

t = ContentCallback()
curlObj = pycurl.Curl()
curlObj.setopt(curlObj.URL, query)
curlObj.setopt(curlObj.WRITEFUNCTION, t.content_callback)
curlObj.setopt(curlObj.HTTPHEADER, ['Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'])
curlObj.setopt(curlObj.USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
curlObj.setopt(pycurl.ENCODING, "gzip,deflate")
curlObj.perform()
curlObj.close()

dataall = t.contents
print('cek data', dataall)
savedata.write(dataall)
savedata.close()

print(query)
