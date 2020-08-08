# -*- coding: utf-8 -*-
"""Copy of Hospital Readmission.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PTx5ujk3Xo-eVwrsgDo2QvgweM3m1_1C
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from google.colab import files
uploaded = files.upload()

import io
df1 = pd.read_csv(io.BytesIO(uploaded['hospital_patients.csv']))

df1.head()

df1.dtypes

df1 = df1.drop(columns = ['encounter_id', 'patient_nbr', 'admission_type_id', 'discharge_disposition_id', 'admission_source_id'])
df1.head()

"""# Data Cleaning and Churning"""

df1 = df1.replace('?', np.nan)

df1.apply(lambda x: sum(x.isnull()),axis = 0)

df1.shape

df1 = df1.drop(columns = ['weight', 'payer_code', 'medical_specialty'])
df1.head()

df1.apply(lambda x: sum(x.isnull()),axis = 0)

df1["race"].value_counts()

df1['race'].fillna('Caucasian', inplace = True)

df1.apply(lambda x: sum(x.isnull()),axis = 0)

df1 = df1.replace(np.nan, 0)
df1.apply(lambda x: sum(x.isnull()),axis = 0)

df1.dtypes

df1.describe()

#Discover outliers with a visualization technique
import seaborn as sns
sns.boxplot(x = df1['num_lab_procedures'])

"""'time_in_hospital', 'num_lab_procedures',	'num_procedures',	'num_medications',	'number_outpatient',	'number_emergency',	'number_inpatient',	'number_diagnoses'"""

sns.boxplot(x = df1['time_in_hospital'])

sns.boxplot(x = df1['num_medications'])

Q1 = df1[['time_in_hospital', 'num_lab_procedures',	'num_procedures',	'num_medications',	'number_outpatient',	'number_emergency',	'number_inpatient',	'number_diagnoses']].quantile(0.25)
Q3 = df1[['time_in_hospital', 'num_lab_procedures',	'num_procedures',	'num_medications',	'number_outpatient',	'number_emergency',	'number_inpatient',	'number_diagnoses']].quantile(0.75)
IQR = Q3 - Q1
print(IQR)

data = df1[~((df1 < (Q1 - 1.5*IQR)) | (df1 >(Q3 + 1.5*IQR))).any(axis = 1)]
data.shape

sns.boxplot(x = data['num_medications'])

sns.boxplot(x = data['num_lab_procedures'])

"""# Exploratory Data Analysis"""

data["readmitted"].value_counts()

data["age"].value_counts()

data.columns

#data = data.drop(columns = ['insulin', 'num_medications', 'number_diagnoses', 'age', 'change', 'diabetesMed'])
data.head()

data['race'].hist(bins = 10)

data['gender'].hist(bins = 10)

data['gender'] = data['gender'].replace('Unknown/Invalid', 'Female')

data['gender'].hist(bins = 10)

data['time_in_hospital'].hist(bins = 10)

data['num_lab_procedures'].hist(bins = 10)

data['metformin'].hist(bins = 10)

data['glyburide'].hist(bins = 10)

data['glipizide'].hist(bins = 10)

data.boxplot(column = 'time_in_hospital')

data['insulin'].hist(bins = 10)

data.boxplot(column = 'number_diagnoses')

data['change'].hist(bins = 10)

data.boxplot(column = 'num_lab_procedures')

data.hist(column = "readmitted", by= "gender", bins = 10)

data.hist(column = "readmitted", by= "glyburide", bins = 10)

data.hist(column = "readmitted", by= "glipizide", bins = 10)

data.hist(column = "readmitted", by= "repaglinide", bins = 10)

data.hist(column = "readmitted", by= "A1Cresult", bins = 10)

data.hist(column = "readmitted", by= "insulin", bins = 10)

data.hist(column = "readmitted", by= "change", bins = 10)

data.shape

data.hist(column = "readmitted", by= "glimepiride", bins = 10)

data = data.drop(columns = ['number_outpatient', 'number_emergency'])
data.head()

data.corr()

"""# Encoding"""

# Import label encoder 
from sklearn import preprocessing 
  
# label_encoder object knows how to understand word labels. 
label_encoder = preprocessing.LabelEncoder() 
  
# Encode labels in column 'species'. 
data['gender']= label_encoder.fit_transform(data['gender']) 
  
data['gender'].unique() 
#Female = 0, Male = 1

data['readmitted']= label_encoder.fit_transform(data['readmitted']) 
data['readmitted'].unique()

data['glyburide']= label_encoder.fit_transform(data['glyburide']) 
  
data['glyburide'].unique()

data['glipizide']= label_encoder.fit_transform(data['glipizide']) 
  
data['glipizide'].unique()

data['A1Cresult']= label_encoder.fit_transform(data['A1Cresult']) 
  
data['A1Cresult'].unique()

data['glimepiride']= label_encoder.fit_transform(data['glimepiride']) 
  
data['glimepiride'].unique()

data['repaglinide']= label_encoder.fit_transform(data['repaglinide']) 
  
data['repaglinide'].unique()

data.head()

data['insulin']= label_encoder.fit_transform(data['insulin']) 
  
data['insulin'].unique()

data['change']= label_encoder.fit_transform(data['change']) 
  
data['change'].unique()

"""# ANN Classifier"""

x = data[['gender', 'time_in_hospital', 'num_lab_procedures', 'glyburide', 'glipizide', 'glimepiride','A1Cresult', 'repaglinide', 'insulin', 'change']]
x

x = x.values
x

y = data.iloc[:,-1].values
from keras.utils import np_utils
y = np_utils.to_categorical(y)
y.shape

"""# Standard Scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

x = sc.fit_transform(x)
print(y)
print(x)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

import keras
from keras.models import Sequential
from keras.layers import Dense

model = Sequential()

print('x_train shape = ', x_train.shape)
print('y_train shape = ', y_train.shape)

#input Layer
model.add(Dense(input_dim = 10, init = 'uniform',activation = 'relu', output_dim = 30))

#Hidden Layer 1
model.add(Dense(output_dim = 10, init = 'uniform',activation = 'relu'))

#Hidden Layer 2
model.add(Dense(output_dim = 7, init = 'uniform',activation = 'relu'))

#Hidden Layer 3
model.add(Dense(output_dim = 10, init = 'uniform',activation = 'relu'))

#Hidden Layer 4
model.add(Dense(output_dim = 4, init = 'uniform',activation = 'relu'))

#Output Layer
model.add(Dense(output_dim = 3, init = 'uniform', activation = 'softmax'))

model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy', 'mse'])

model.fit(x_train, y_train, epochs = 300, batch_size = 10)

"""from sklearn.model_selection import cross_val_score

from keras.wrappers.scikit_learn import KerasClassifier

from sklearn.model_selection import KFold

estimator = KerasClassifier(build_fn=baseline_model(), epochs=50, batch_size=5, verbose=0)

kfold = KFold(n_splits=10, shuffle=True)

results = cross_val_score(estimator, x, y, cv=kfold)

print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
"""

y_pred = model.predict(x_test)
y_pre d

y_test

def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=10, activation='relu'))
	model.add(Dense(3, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
estimator = KerasClassifier(build_fn=baseline_model, epochs=50, batch_size=15, verbose=0)
kfold = KFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, x_train, y_train, cv=kfold)
print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

"""# Random Forest"""

x = data[['gender', 'time_in_hospital', 'num_lab_procedures', 'glyburide', 'glipizide', 'glimepiride','A1Cresult', 'repaglinide', 'insulin', 'change']]
y = data.iloc[:,-1].values
#from keras.utils import np_utils
#y = np_utils.to_categorical(y)
#y.shape

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

x = sc.fit_transform(x)
print(y)
print(x)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

from sklearn.ensemble import RandomForestClassifier
rmf = RandomForestClassifier(max_depth = 100, random_state = 0)
rmf_clf = rmf.fit(x_train, y_train)

#Print cross validation score for Random Forest Classifier
from sklearn.model_selection import cross_val_score, cross_val_predict
rmf_clf_acc = cross_val_score(rmf_clf, x_train, y_train, cv=10, scoring = 'accuracy', n_jobs = -1)
rmf_proba = cross_val_predict(rmf_clf, x_train, y_train, cv=10, method = 'predict_proba')
rmf_clf_scores = rmf_proba[:, 1]

rmf_clf_acc