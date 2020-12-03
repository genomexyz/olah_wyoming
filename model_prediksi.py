import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LassoLars, BayesianRidge
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.metrics import mean_absolute_error, confusion_matrix

#setting
param_file = 'index_param.npy'
label_file = 'hujan_label.npy'
test_len = 400

all_param = np.load(param_file)
all_label = np.load(label_file)

param = []
label = []
for i in range(len(all_param)):
	if np.isnan(all_param[i]).any() or np.isnan(all_label[i]):
		continue
	param.append(all_param[i])
	label.append(all_label[i])

param = np.array(param)
label = np.array(label)
print(param, np.shape(param))

param_training = param[:-test_len]
label_training = label[:-test_len]

param_test = param[-test_len:]
label_test = label[-test_len:]

clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
clf.fit(param_training, label_training)

prediksi = clf.predict(param_test)
print(prediksi)
print(accuracy_score(label_test, prediksi))
#|        X      |predicted tidak_hujan| predicted hujan|
#|obs tidak hujan| correct_negative    | false_alarm    |
#|obs hujan      | miss                | hit            |
print(confusion_matrix(label_test, prediksi))
