import numpy as np
from sklearn import svm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from data_prep import *
from sklearn import metrics
from sklearn import preprocessing

def svm_model(test_size):

    X = pd.read_csv("dataset_scaled.csv")
    Y = pd.read_csv("target.csv")

    # Droping the index column
    X.drop(X.columns[[0]], axis=1, inplace=True)
    Y.drop(Y.columns[[0]], axis=1, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size= test_size, random_state=42)  
    # 'rbf' value is the gaussian kernel, 'C' is the coefficient used for regularization during training	
    # model_rbf = svm.SVC(kernel='rbf',C=2.0)

    model_linear = svm.LinearSVC(C=1.0) # 1, 2, 4


    model_linear.fit(X_train,y_train.values.ravel())
    weights_linear =model_linear.coef_

    Y_predicted = model_linear.predict(X_test)

    accuracy = metrics.accuracy_score(y_test,Y_predicted)
    print ("accuracy = "+str(round(accuracy * 100,2))+"%")


    print(f'coefficient-linear-kernel: {weights_linear}')

    # bias_rbf = model_rbf.intercept_

    # Y_predicted = weights_rbf.predict(X_test)

    return  weights_linear

def random_forest(test_size):
    
    X = pd.read_csv("dataset_scaled.csv")
    Y = pd.read_csv("target.csv")

    # Droping the index column
    X.drop(X.columns[[0]], axis=1, inplace=True)
    Y.drop(Y.columns[[0]], axis=1, inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size= test_size, random_state=42)   
    model = RandomForestClassifier(n_estimators = 5, criterion = 'entropy',random_state = 42)
    model.fit(X_train,y_train)
    return model

# dataset_saceled = '/Users/sg/Desktop/Betty/dataset/dataset_scaled.csv'
# dataset = "/Users/sg/Desktop/Betty/dataset/dataset.csv"
# class_label = '/Users/sg/Desktop/Betty/dataset/target.csv'
test_size = 0.2

# y_test,Y_predicted, weights_rbf, weights_linear = svm_model(dataset_saceled, class_label, test_size) 

weights = svm_model(test_size) 

print(weights)
print (weights.tolist())


# url_maliciou = 'http://boasecg7.beget.tech/cgi-bin/index/pcg/free/frebox158418/freemobs/'
# url_benign = 'https://www.wikipedia.org'


# rf = random_forest(dataset_saceled, class_label, test_size)

# data_dir = "/Users/sg/Desktop/Betty/dataset/dataset.csv"
# df = pd.read_csv(data_dir)
# df.drop(df.columns[[0]], axis=1, inplace=True)
# X = df.to_numpy()
# scaler =  StandardScaler()
# scaler.fit(X)
# while(True):
   
#     url = input('Enter : ')

#     features = [extract_features(url)]
#     features_scaled = scaler.transform(features)
#     features_scaled = features_scaled

#     print (features_scaled)
#     print (rf.predict(features_scaled))
    





