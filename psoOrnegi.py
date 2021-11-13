#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 07:08:52 2021

@author: Selçuk Sinan KIRAT
"""
from random import random, randrange
from math import sqrt
import sys
import numpy as np
from matplotlib import pyplot as plt

#hedef = 0 # Amaç fonksiyonda y'nin 0'a yaklaşması [-1.5,1.5] aralığı hedeflendi

c1 = 1.5
c2 = 2.5

r1 = round(random(),1)
r2 = round(random(),1)

parcaciklar = {}

def amacFonk(x):
    return pow(x,2)-5*x-6 # y = x2-5x-6

def psoBaslat(pSayisi:int):
    enYakin = sys.maxsize
    gBest = 0
    
    rSayilar = []
    pNo = 1
    
    x = []
    
    while(len(rSayilar)<pSayisi):
        sayi = randrange(9,16)
        
        if(rSayilar.count(sayi)==0):
            rSayilar.append(sayi)
            parcaciklar["p-"+str(pNo)]=[sayi, sayi, 0] # [deger, pBest, hiz]
            x.append(parcaciklar["p-"+str(pNo)][0])
            print("|p-"+str(pNo)+" parçacığı|","\tDeğer:",sayi,"\tpBest:",sayi,"\tİlk Hız:",0,sep="")
            pNo += 1
        
            if(sayi < enYakin): enYakin = sayi
            
    gBest = enYakin
    
    print("Global En İyi (gBest):", gBest)
    print("HEDEFE UZAKLIK:", amacFonk(gBest))
    
    xx = np.array(x)
    yy = amacFonk(xx)
    grafikCiz(xx,yy)
    
    hareketEt(gBest)
    
def hareketEt(gB):
    gBest = gB
    pBest = 0
    x = []
    sayac = 1
    
    while(True):
        print(40 * "_")
        print(sayac, ". İTERASYON", sep="")
        
        for i in parcaciklar:
            ekle = parcaciklar[i][2] + c1*r1*(parcaciklar[i][1]-parcaciklar[i][0]) + c2*r2*(gBest-parcaciklar[i][0])
            
            parcaciklar[i][2] = ekle
            parcaciklar[i][0] += ekle
            
            # Grafik çizimi için x verileri toplanıyor
            x.append(parcaciklar[i][0])
            
            # y = 0 noktasına göre mutlak uzaklıklar
            u1 = amacFonk(parcaciklar[i][0])
            degerUzakligi = round(sqrt((0 - u1) ** 2)) # Mutlak uzaklık
            
            u2 = amacFonk(parcaciklar[i][1])
            pBestUzakligi = round(sqrt((0 - u2) ** 2))
            
            if (degerUzakligi < pBestUzakligi): pBest = parcaciklar[i][0]
            else: pBest = parcaciklar[i][1]
            
            parcaciklar[i][1] = round(pBest,1)
            
            # Güncellenen uzaklık
            u2 = amacFonk(parcaciklar[i][1])
            pBestUzakligi = round(sqrt((0 - u2) ** 2))
            
            gBestUzakligi = round(sqrt((0 - amacFonk(gBest)) ** 2))
            
            # Hedefe daha yakın pBest varsa, gBest'i güncelle
            if (pBestUzakligi < gBestUzakligi): gBest = pBest
            
            print("|"+i+" parçacığı|","\tDeğer:",round(parcaciklar[i][0],1),"\tpBest:",round(parcaciklar[i][1],1),"\tYeni Hız:",round(parcaciklar[i][2],1),sep="")
            
        print(40 * "-")
        print("Global En İyi (gBest):", round(gBest,1))
        print("HEDEFE UZAKLIK:", amacFonk(gBest))
        
        xx = np.array(x)
        yy = amacFonk(xx)
        grafikCiz(xx,yy)
        
        x.clear()
              
        if (amacFonk(gBest)<=1.5 and amacFonk(gBest)>=-1.5):
            break   # [-1.5,1.5] aralığına girinceye kadar hareket et
            
        sayac += 1
    
       
def grafikCiz(xx, yy):
    plt.figure(figsize=(1,3))
    plt.ylim(-30, 150)
    plt.xlim(-10, 20)
    plt.xlabel("x değerleri")
    plt.ylabel("y = x2-5x-6")
    plt.title("PSO DÜZLEMİ")
    plt.scatter(xx, yy)
    plt.grid()
    plt.show()
    
psoBaslat(5)
