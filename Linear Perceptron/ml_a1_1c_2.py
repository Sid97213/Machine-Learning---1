# -*- coding: utf-8 -*-
"""ML_A1_1C_2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16CwMjbj6roRiy4wQ0DCdxDqHqCf0BXrv
"""

from random import seed
import numpy as np
import pandas as pd

from google.colab import files
files.upload()

#Standardize dataset
def standardize_data(dataframe):
    target = dataframe["target"]
    dataframe = dataframe.drop(['target'],axis=1)
    mean = dataframe.mean()
    std = dataframe.std()
    dataframe = (dataframe - mean)/std
    dataframe = pd.concat([pd.Series(1,index=dataframe.index,name="bias"),dataframe],axis=1)        #add bias variable
    dataframe = dataframe.join(target)          #join target attr to dataframe
    return dataframe

#Split dataset into training and testing set
def train_test_split(dataframe,split=0.70):
    dataframe = dataframe.sample(frac=1)         #shuffle rows of the dataframe  
    train_size = int(split * len(dataframe))    #print(train_size)
    test_size = len(dataframe) - train_size     #print(test_size)
    train = dataframe[:train_size]              #copy first 70% elements into train
    test = dataframe[-test_size:]               #copy last 30% elements into test
    return train,test

def predict(X,weights):
    activation = X.dot(weights)
    return 1.0 if activation >=0.0 else -1.0

def LP(X,Y,epochs,alpha):
    weights = np.zeros(len(X.columns))
    N = X.shape[0]
    Cost = np.zeros(epochs)
    for i in range(epochs):
        misclass_err=0
        for j in range(0,N):
            X_j = X.iloc[j]
            y_pred = predict(X_j,weights)
            weights = weights + alpha*((Y.iloc[j]-y_pred).T) * X.iloc[j]
            y_pred_new = predict(X_j,weights)
            if(y_pred_new != Y.iloc[j]):
                misclass_err += Y.iloc[j] * (X_j.dot(weights.T)) *-1
        Cost[i]=misclass_err
        if(Cost[i]==0):
            print("Epoch:",i,"Loss: ",misclass_err)
            break
        if(i%10==0):
            print("epoch num:",i,"  loss: ",misclass_err)
    return weights

def calc_accuracy(test,weights):
    N = len(test)
    X = test.loc[:,'bias':'X3']
    Y = test.loc[:,'target']
    Y_pred = X.dot(weights)
    for i in range(len(Y_pred)):
        if(Y_pred.iloc[i]<0):
            Y_pred.iloc[i]=-1
        else:
            Y_pred.iloc[i]=1
    correct=0
    for i in range(len(Y)):
        if(Y_pred.iloc[i]==Y.iloc[i]):
            correct+=1
    return float(correct/N)*100.0

if __name__ == '__main__':
    seed(1)
    dataframe = pd.read_csv('dataset_LP_2.csv', sep=",",header=None)
    dataframe.columns = ["X1","X2","X3","target"]
    
    target = dataframe['target']
    dataframe = dataframe.drop(['target'],axis=1)
    for i in range(len(target)):
        if(target.iloc[i]==0):
            target.iloc[i]=-1
    dataframe = dataframe.join(target)
    dataframe = standardize_data(dataframe)
    train, test = train_test_split(dataframe)
    X = train.loc[:,'bias':'X3']
    Y = train.loc[:,'target']
    
    epochs = 1000
    weights = LP(X,Y,epochs,0.01)
    print("Weights :",weights.T)
    accuracy = calc_accuracy(test,weights)
    print("Accuracy is: ",accuracy,"%")

