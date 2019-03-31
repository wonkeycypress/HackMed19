#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 19:07:55 2019

@author: harrycooper
"""
import pandas as pd 
import nexmo
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split



df = pd.read_csv('Parkinson_Multiple_Sound_Recording/full_data.csv', sep=",", header=0)  

features = df.iloc[:,0:-1]
target = df.iloc[:,-1]

#print(features)
#print(target)

X_train, X_test, y_train, y_test = train_test_split(features, target, 
                                                    test_size = 0.2, 
                                                    random_state=42)


# Create a k-NN classifier with 7 neighbors: knn
knn = KNeighborsClassifier(n_neighbors = 24)

# Fit the classifier to the training data
knn.fit(X_train,y_train)

# Print the accuracy
print(knn.score(X_test, y_test))


def classify(file):
    tdf = pd.read_csv(file);
    
    #print(tdf.iloc[0,15]);
    
    pred = knn.predict(tdf)
    prob = knn.predict_proba(tdf)
    
    if pred == 0:
        res = "have parkinsons"
    else:
        res = "not have parkinsons"
    
#    print(knn.predict(tdf));
#    print(knn.predict_proba(tdf));
    return (prob, res)

def sendSMS(prob, res):
    client = nexmo.Client(key='21304330', secret='spKzQR0NWIKOvYUY')
    response = client.send_message({'from': 'CMP', 'to': '+447979488684', 
                                    'text': 'Patient X is %.0f percent likely to %s' % (max(prob[0])*100, res)})
    
    response = response['messages'][0]
    
    if response['status'] == '0':
      print('Sent message', response['message-id'])
    
      print('Remaining balance is', response['remaining-balance'])
    else:
      print('Error:', response['error-text'])
  