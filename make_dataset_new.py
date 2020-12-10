import glob
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

#setting
data_dir = 'raw'
indexkeyword = ['Convective Available Potential Energy:', 'K index:', 'Cross totals index:', 'Vertical totals index:', 
'Lifted index:', 'Showalter index:']
failkeyword = ["Can't get"]
start_date = datetime(2019,1,1)
end_date = datetime(2020,1,1)
thresholdlen = 100
stasiun = 'WAAA'

def checkdatavalid(rawdata):
	valid = True
	for i in range(len(failkeyword)):
		if failkeyword[i] in rawdata:
			valid = False
	return valid

current_date = start_date
all_param = []
all_param_pandas = []
while current_date < end_date:
	tahun = current_date.strftime('%Y')
	bulan = current_date.strftime('%m')
	hari = current_date.strftime('%d')
	jam = current_date.strftime('%H')
	data_raw_filename = '%s/%s-%s%s%s%s'%(data_dir, stasiun, tahun, bulan, hari, jam)
	print('processing %s'%(data_raw_filename))

	data_input = np.zeros((len(indexkeyword)))
	data_input[:] = np.nan

	try:
		data_raw_open = open(data_raw_filename)
		data_raw = data_raw_open.read()
		data_raw_open.close()
	except FileNotFoundError:
		all_param.append(data_input)
		print('data not found, continue...')
		current_date += timedelta(hours=12)
		continue

	if not checkdatavalid(data_raw):
		all_param.append(data_input)
		print('data broken, continue...')
		current_date += timedelta(hours=12)
		data_raw_open.close()
		continue

	data_raw_array = data_raw.split('\n')
	for i in range(len(indexkeyword)):
		for j in range(len(data_raw_array)):
			if indexkeyword[i] in data_raw_array[j]:
				awal = data_raw_array[j].find(indexkeyword[i])
				try:
					value = float(data_raw_array[j][awal+len(indexkeyword[i]):])
				except ValueError:
					value = np.nan
				data_input[i] = value
				break
	print(data_input)
	all_param.append(data_input)
	current_date += timedelta(hours=12)

#save
all_param = np.array(all_param)
np.save('index_param_2019.npy', all_param)
