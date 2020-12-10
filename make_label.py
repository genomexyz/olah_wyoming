import glob
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

#setting
data_dir = 'label_raw'
stasiun = 'WAAA'
limit_sandi = ['TEMPO', 'BECMG']
start_date = datetime(2019,1,1)
end_date = datetime(2020,1,1)

def make_array_from_raw(raw_str):
	array = raw_str.split('\n')
	if array[-1] == '':
		array = array[:-1]
	date_array = []
	sandi_array = []
	for i in range(len(array)):
		fragment = array[i].split('\t')
		date_array.append(fragment[0].strip())
		
		sandi = fragment[2].strip()
		for limit in limit_sandi:
			idx = sandi.find(limit)
			if idx != -1:
				break
		sandi = sandi[:idx]
		sandi_array.append(sandi)
	return date_array, sandi_array

current_date = start_date
all_label = []
all_label_pandas = []
while current_date < end_date:
	#end_period = current_date + timedelta(hours = 12)
	end_period = current_date + timedelta(hours = 12)
	status_hujan = np.nan
	while current_date < end_period:
		#build date string for indentifier in the raw data
		#example : 18/01/2016 18:00:00Z
		tahun = current_date.strftime('%Y')
		bulan = current_date.strftime('%m')
		hari = current_date.strftime('%d')
		jam = current_date.strftime('%H')
		menit = current_date.strftime('%M')
		identifier_date_str = current_date.strftime('%d/%m/%Y %H:%M:00Z')
		try:
			file_raw = open('%s/%s-%s%s'%(data_dir, stasiun, tahun, bulan))
		except FileNotFoundError:
			current_date += timedelta(minutes = 30)
			continue
		
		raw_data = file_raw.read()
		
		current_date += timedelta(minutes = 30)
		date_array, sandi_array = make_array_from_raw(raw_data)
		
		try:
			idx = date_array.index(identifier_date_str)
			focused_sandi = sandi_array[idx]
			if 'TS' in focused_sandi:
				status_hujan = 1
			else:
				if np.isnan(status_hujan):
					status_hujan = 0
		except ValueError:
			current_date += timedelta(minutes = 30)
			continue

		#next date
		current_date += timedelta(minutes = 30)

	#append label
	print(current_date, status_hujan)
	all_label.append(status_hujan)
	
	#for 6-hour scheme
#	current_date += timedelta(hours = 6)
#	print('after', current_date)

#save
all_label = np.array(all_label)
np.save('hujan_label_2019.npy', all_label)
