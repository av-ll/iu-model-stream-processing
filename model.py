# import libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_score
import warnings
import pickle

#filter some sklearn warnings
warnings.filterwarnings("ignore")

#read the training data,
#separate the labels and into train/test data
data = pd.read_csv('data_frame.csv')
labels = data['labels']
data = data.drop(['labels'],axis=1)

data,labels

xtrain,xtest,ytrain,ytest = train_test_split(data,labels,random_state=1)

#parameters for the gridsearch algorithmn
log_reg_params = {"penalty": ['l1', 'l2','elasticnet'], 'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],'solver' : ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}

grid_log_reg = GridSearchCV(LogisticRegression(), log_reg_params)

grid_log_reg.fit(xtrain,ytrain)

# Getting the best parameters fit for the model
lr = grid_log_reg.best_estimator_


# just checking precision score which is around 96% and accuracy 99%
# which should be enough for this project
prediction = lr.predict(xtest)

precision = precision_score(ytest,prediction)

accuracy = accuracy_score(ytest,prediction)

precision

accuracy

model_name = 'model.pkl'

pickle.dump(lr, open(model_name, 'wb'))
