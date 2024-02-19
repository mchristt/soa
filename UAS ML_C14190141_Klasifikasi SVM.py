import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics

train_data = pd.read_excel('https://imelda.petra.ac.id/public/dataset.xlsx', sheet_name='Klasifikasi.4D')
pd.DataFrame(train_data)
train_data = train_data.fillna(0)
test_data = pd.read_excel('https://imelda.petra.ac.id/public/dataset_test.xlsx', sheet_name='Klasifikasi.4D.test')
pd.DataFrame(test_data)

# #Load dataset
# train_data = pd.read_csv("dataset.csv")
# pd.DataFrame(train_data)
# test_data = pd.read_csv("dataset_test.csv")
# pd.DataFrame(test_data)

#train_data.head()
#test_data.head()
y_train = train_data.pop("NH")

# print the features
print("Features: \n", train_data)

# print the labels
print("Labels: ", y_train)

#split data for accuracy
X_train, X_test, y_train, y_test = train_test_split(train_data, y_train, test_size=0.33, random_state=42)

#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = clf.predict(test_data)
print("Hasil prediksi : \n", y_pred)

#Calculate the prediction accuracy
y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))