import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

def frekuensi_hujan_bulanan(bulan_cari):
	jam_hujan = np.zeros(48)
	for i in range(len(dataset['waktu'])):
		waktu_ini = dataset['waktu'][i]
		if (waktu_ini.month != bulan_cari):
			continue
		if np.isnan(dataset['status hujan'][i]):
			continue
		index_major = waktu_ini.hour * 2
		if waktu_ini.minute == 0:
			index_minor = 0
		else:
			index_minor = 1
		index = index_major + index_minor
		jam_hujan[index] += dataset['status hujan'][i]
	return jam_hujan

def plot_hujan(filename_save, nama_bulan, angka_bulan):
	jam_hujan = frekuensi_hujan_bulanan(angka_bulan)
	print(jam_hujan)
	plt.ylabel("Rain Occurence Total")
	plt.xlabel("Time")
	plt.plot(np.arange(len(jam_hujan)), jam_hujan)
	plt.title('Rain Occurence Pattern in %s'%(nama_bulan))
	plt.xticks(np.arange(0,48,6), chosen_time_label, rotation=315)
	#plt.show()
	#plt.savefig('jan.png', orientation='landscape', dpi=300)
	fig = plt.gcf()
	fig.set_size_inches((11, 8.5), forward=False)
	fig.savefig(filename_save, dpi=500)
	plt.clf()

dataset = pd.read_pickle("status_hujan.pkl")

# make array of time in a day
time_template = '%s:%s:00'
time_label = []
for i in range(48):
	# WAAA is GMT + 8
	jam = i//2 + 8
	menit = (i%2)*30
	if menit < 10:
		menit = '0'+str(menit)
	else:
		menit = str(menit)
	if jam >= 24:
		jam -= 24
	if jam < 10:
		jam = '0'+str(jam)
	else:
		jam = str(jam)
	waktu = time_template%(jam, menit)
	time_label.append(waktu)
#time_label
chosen_time_label = []
for i in range(0, len(time_label), 6):
	chosen_time_label.append(time_label[i])
print(chosen_time_label)


plt.ylabel("Rain Occurence Total")
plt.xlabel("Time")
jam_hujan = frekuensi_hujan_bulanan(1)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='January')
jam_hujan = frekuensi_hujan_bulanan(2)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='February')
jam_hujan = frekuensi_hujan_bulanan(3)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='March')
jam_hujan = frekuensi_hujan_bulanan(4)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='April')
jam_hujan = frekuensi_hujan_bulanan(5)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='May')
jam_hujan = frekuensi_hujan_bulanan(6)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='June')
jam_hujan = frekuensi_hujan_bulanan(7)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='July')
jam_hujan = frekuensi_hujan_bulanan(8)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='August')
jam_hujan = frekuensi_hujan_bulanan(9)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='September')
jam_hujan = frekuensi_hujan_bulanan(10)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='October')
jam_hujan = frekuensi_hujan_bulanan(11)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='November')
jam_hujan = frekuensi_hujan_bulanan(12)
plt.plot(np.arange(len(jam_hujan)), jam_hujan, label='December')


#ending
plt.xticks(np.arange(0,48,6), chosen_time_label, rotation=315)
plt.legend()
plt.show()
