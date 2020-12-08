import glob
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

#setting
data_dir = 'label_raw'
stasiun = 'WAAA'
limit_sandi = ['TEMPO', 'BECMG']
start_date = datetime(2016,1,1)
end_date = datetime(2019,1,1)

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
all_waktu = []
all_hujan = []

while current_date < end_date:
	print('now processing %s'%(current_date))
	hujan = np.nan

	tahun = current_date.strftime('%Y')
	bulan = current_date.strftime('%m')
	hari = current_date.strftime('%d')
	jam = current_date.strftime('%H')
	menit = current_date.strftime('%M')
	identifier_date_str = current_date.strftime('%d/%m/%Y %H:%M:00Z')
	try:
		file_raw = open('%s/%s-%s%s'%(data_dir, stasiun, tahun, bulan))
	except FileNotFoundError:
		#end
		all_waktu.append(current_date)
		all_hujan.append(hujan)
		current_date += timedelta(minutes = 30)
		continue
		
	raw_data = file_raw.read()
	
	current_date += timedelta(minutes = 30)
	date_array, sandi_array = make_array_from_raw(raw_data)
		
	try:
		idx = date_array.index(identifier_date_str)
		focused_sandi = sandi_array[idx]
		if 'RA' in focused_sandi:
			hujan = 1
		else:
			hujan = 0
	except ValueError:
		#end
		all_waktu.append(current_date)
		all_hujan.append(hujan)
		current_date += timedelta(minutes = 30)
		continue
	
	#end
	all_waktu.append(current_date)
	all_hujan.append(hujan)
	current_date += timedelta(minutes = 30)

all_hujan = np.array(all_hujan)
all_data = {'waktu' : all_waktu, 'status hujan' : all_hujan}
df = pd.DataFrame(data=all_data)
df.to_pickle('status_hujan.pkl')
