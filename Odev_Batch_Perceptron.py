#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 12:05:31 2022

@author: sskirat
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

veriler = pd.read_excel('Iris.xls')
veriler2 = pd.read_excel('Iris.xls')
veriler = veriler.iloc[:100,:]

#print(veriler.tail())

X = veriler.iloc[:,[2,3]].values
y = veriler.iloc[:,4:].values
y = np.where(y=="Iris-setosa",1,-1)

#%%

class TekliAlgilayici(object): # Perceptron
    
    def __init__(self):
        print("Tekli Algılayıcı Oluşturuldu")
    
    def siniflandir(self, X, y):
        (n_ornek, n_ozellik) = X.shape
        self.w = np.zeros(n_ozellik)
        
        for i in range(0, n_ornek):
            pred = np.dot(self.w, X[i])
            if(y[i] * pred <= 0):
                self.w = self.w + y[i] * X[i]
                
        return self.w
    
    def tahmin(self, X):
        (n_samples, n_features) = X.shape
        self.predictions = np.zeros(n_samples)
        for i in range(0, n_samples):
            x = X[i]
            self.prediction = np.dot(self.w, x)
            if(self.prediction > 0):
                self.predictions[i] = 1
            else:
                self.predictions[i] = -1
        return self.predictions
    
    
class TopluAlgilayici(object): # Batch Perceptron
    
    def __init__(self):
        n_ornek = X.shape[0]
        print("Toplu Algılayıcı Oluşturuldu. (Toplam {} örnek)".format(n_ornek))
    
    def siniflandir(self, X, y):
        (n_ornek, n_ozellik) = X.shape
        self.w = np.zeros(n_ozellik)
        self.A = np.zeros(n_ozellik) # Delta
        
        for i in range(0, n_ornek):
            pred = np.dot(self.w, X[i])
            if(y[i] * pred <= 0):
                self.A = self.A + y[i] * X[i]
                
        self.A = self.A / n_ornek # Toplu (Batch) Güncelleme
        self.w = self.w + self.A
            
        return self.w
    
    def tahmin(self, X):
        (n_samples, n_features) = X.shape
        self.predictions = np.zeros(n_samples)
        for i in range(0, n_samples):
            x = X[i]
            self.prediction = np.dot(self.w, x)
            if(self.prediction > 0):
                self.predictions[i] = 1
            else:
                self.predictions[i] = -1
        return self.predictions
    
    
a = TekliAlgilayici()
a.siniflandir(X, y)

aT = TopluAlgilayici()
aT.siniflandir(X, y)

print("__________________________________________________")
print("Tekli algılayıcı (PERCEPTRON) ağırlıkları\n[w1, w2]:", a.w)
print("__________________________________________________")
print("Toplu algılayıcı (BATCH PERCEPTRON) ağırlıkları\n[w1, w2]:", aT.w)

sns.scatterplot(x="petal length", y="petal width", hue="iris", data=veriler)

plt.title("2 özelliğe göre Iris Veri Seti")
plt.show()