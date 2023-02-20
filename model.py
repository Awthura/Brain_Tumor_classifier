import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.svm import SVC
import pandas as pd
import seaborn as sn


class Mdl:
    def __init__(self):
		# Out of these 3 models tested RandomForest was the most accurate one
		
        # self.lgr= LogisticRegression(dual=False, verbose=1, random_state=  4)
        # self.svm = SVC(kernel='poly', degree=2, gamma='auto', coef0=1, C=5)
        self.Rf = RandomForestClassifier(n_estimators = 2000, random_state= 4 ,verbose=1)
        self.df = pd.read_csv(r'data\Brain Tumor.csv')
        self.features = ['Mean','Variance','Standard Deviation','Entropy','Skewness','Kurtosis','Contrast','Energy','ASM',
                        'Homogeneity','Dissimilarity','Correlation','Coarseness']
        
    def preprocess(self):
		# Ignore preprocessing to import values from slider (very minimal accuracy drop)
        # self.df[features] = RobustScaler().fit_transform(self.df[features])
        X = self.df[self.features]
        y = self.df.Class 
        processed_data = train_test_split(X, y, test_size=0.25)
        return processed_data

    def train(self, processed_data):
        X_train, X_test,  y_train, y_test = processed_data
        mdl = self.Rf.fit(X_train, y_train)
        accuracy = self.Rf.score(X_test,y_test)
        return mdl, accuracy

    def predict_inst(self, X_inst, mdl):
        y_inst=mdl.predict([X_inst])
        return y_inst

    def predict_rdm(self, mdl):
        rdr = self.df.sample()
        row_num = rdr.index.to_list()
        rdr_X = rdr[self.features]
        rdr_y = rdr['Class'].to_string(index=False)
        mdl_y = mdl.predict(rdr_X)
        print(f'A random row from the dataset {row_num} is picked.{os.linesep}The actual result is {rdr_y} & the model predicts {mdl_y}.')
    
    def plotCm(self, processed_data, mdl):
        X_train, X_test,  y_train, y_test = processed_data
        y_pred = mdl.predict(X_test)
        cm = confusion_matrix(y_test,y_pred)
        # print(cm)
        df_cm = pd.DataFrame(cm,range(2),range(2))
        sn.set(font_scale=1.4) # for label size
        sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}, fmt='d') # font size
        # plt.show()
        return cm
    
# nmdl = Mdl()
# data = nmdl.preprocess()
# mdl, acc = nmdl.train(data)
# print(acc)
# nmdl.predict_rdm(mdl)
# nmdl.plotCm(data, mdl)


# df = pd.read_csv(r'data\Brain Tumor.csv')
# data = Mdl.preprocess(df)
# mdl, accuracy = Mdl.train(data)
# print(accuracy)

#instance = []
#y_pred = predict_inst(mdl,instance)
#print(y_pred)