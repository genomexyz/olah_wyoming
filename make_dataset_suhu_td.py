import glob
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

#setting
data_dir = 'raw'
indexkeyword = ['1000', '850', '700', '500']
failkeyword = ["Can't get"]
start_date = datetime(2016,1,1)
end_date = datetime(2019,1,1)
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

	data_input = np.zeros((len(indexkeyword)*2))
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
			if indexkeyword[i] in data_raw_array[j][:8]:
				try:
					suhu = data_raw_array[j][17:22]
					dew_point = data_raw_array[j][24:29]
					suhu_float = float(suhu)
					dew_point_float = float(dew_point)
					selisih = suhu_float - dew_point_float
					data_input[i*2] = suhu_float
					data_input[i*2+1] = dew_point_float
				except ValueError:
					break
	print(data_input)
	all_param.append(data_input)
	current_date += timedelta(hours=12)

#save
all_param = np.array(all_param)
np.save('index_param_suhu_td.npy', all_param)
