#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 18:32:21 2022

@author: Selçuk Sinan KIRAT (Ogr No: 211129110)
"""
import time
from random import random, randrange
from tkinter import *
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

window = Tk()
window.title("Gri Kurt Optimizasyon Algoritması")

# Mevcut ekran çözünürlüğü en ve boy oranları alınıyor
width = window.winfo_screenwidth() 
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))

window.resizable(1, 1)

aktifDeger1 = StringVar(value=0)
aktifDeger2 = StringVar(value=0)
aktifDeger3 = StringVar(value=0)
aktifDeger4 = StringVar(value=0)

xN = np.empty(shape=(0, 2)) # Gri kurt listesi
xA = xB = xD = 0            # Alfa, Beta ve Delta kurtları
rS = []                     # Rastgele sayı havuzu


def suruGuncelle():
    """
    Kullanıcıdan GUI ortamında alınan gri kurt sayısı 
    (populasyon sayısı) na göre gerekli güncellemeleri yapar.
    """
    global pN, xN
    
    pN = int(aktifDeger1.get())
    fig.clear()
    suruOlustur(pN)
    xN, xA, xB, xD = sirala(xN)
    goster(xN)
    
    
def itrGuncelle():
    """
    Kullanıcıdan GUI ortamında alınan maksimum iterasyon sayısı
    parametresine göre iN ve a değişkenini günceller.
    """
    global iN, a
    
    iN = int(aktifDeger2.get())
    a = np.arange(2, 0, -2*(1/iN)) 
    
    
def egimGuncelle():
    """
    Kullanıcıdan GUI ortamında alınan dağın eğimi parametresine
    göre grafik ortamındaki dağın görüntüsünü günceller
    """
    global dE
    
    dE = float(aktifDeger3.get())
    fig.clear()
    goster(xN)
    
    
def yukseklikGuncelle():
    """
    Kullanıcıdan GUI ortamında alınan dağın yüksekliği parametresine
    göre grafik ortamındaki dağın görüntüsünü günceller
    """
    global dY
    
    dY = int(aktifDeger4.get())
    fig.clear()
    goster(xN)
    

# [+] Tkinter Python GUI Widget'ler
L1 = Label(window, text="Gri Kurt Sayısı:")
L1.grid(row=0, column=0)

SB1 = Spinbox(window, from_=4, to=20, width=5, state="readonly",
              command=suruGuncelle, textvariable=aktifDeger1)
SB1.grid(row=0, column=1, sticky = W)
pN = int(SB1.get())

L2 = Label(window, text="İterasyon Sayısı:")
L2.grid(row=0, column=2)

SB2 = Spinbox(window, from_=15, to=2000, width=5, state="readonly",
              command=itrGuncelle, textvariable=aktifDeger2)
SB2.grid(row=0, column=3, sticky = W)
iN = int(SB2.get())
a = np.arange(2, 0, -2*(1/iN)) 

L3 = Label(window, text="Dağın Eğimi:")
L3.grid(row=0, column=4)

SB3 = Spinbox(window, from_=1.01, to=1.2, width=5, state="readonly",
              values=(1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07, 1.08, 1.09, 1.1, 1.15, 1.2),
              command=egimGuncelle, textvariable=aktifDeger3)
SB3.grid(row=0, column=5, sticky = W)
dE = float(SB3.get())


L4 = Label(window, text="Dağın Yüksekliği:")
L4.grid(row=0, column=6)

SB4 = Spinbox(window, from_=500, to=10000, width=5, state="readonly",
              values=(500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000),
              command=yukseklikGuncelle, textvariable=aktifDeger4)
SB4.grid(row=0, column=7, sticky = W)
dY = int(SB4.get())
# [-] Tkinter Python GUI Widget'ler

def katsayilar(i):
    """
    Parameters
    ----------
    i : her iterasyonda doğrusal olarak 2'den 0'a doğru azalan
    a değerleri için index bilgisi.

    Returns
    -------
    A katsayısı
    C katsayısı
    """
    r1 = random()
    r2 = random()
    
    A = 2*(a[i])*r1 - a[i]
    C = 2 * r2
    
    return A, C


def amacFonk(x):
    """
    Parameters
    ----------
    x : Her bir gri kurt için pozisyon bilgisi (x ekseni)

    Returns
    -------
    Her bir gri kurt için yamaç üzerindeki konum bilgisi (y ekseni)

    """
    return dY / (1+pow(dE, -x)) # return 3000 / (1+pow(1.1, -x))


def uygunlukFonk(x):
    """
    Parameters
    ----------
    x : Her bir gri kurt için pozisyon bilgisi (x ekseni)

    Returns
    -------
    Her bir gri kurt için uygunluk değeri (ava olan yakınlık)

    """
    f = amacFonk(x)
    return f * (dY - f) / dY


def suruOlustur(pN):
    """
    Parameters
    ----------
    pN : Kullanıcıdan alınan gri kurt sayısı (populasyon sayısı)
    bilgisine göre kurtların dağ yamacına rastgele dağıtılmasını
    sağlar.

    Returns
    -------
    None.

    """
    global xN
    
    rS.clear()
    xN = np.empty(shape=(0, 2))
    
    anahtar = 1
    while (len(rS) < pN):
    
        deger1 = randrange(-250, -100)
        deger2 = randrange(100, 250)
        
        if (anahtar == 1 and rS.count(deger1) == 0):
            xN = np.append(xN, [[deger1, uygunlukFonk(deger1)]], axis=0)
            rS.append(deger1)
            
        if (anahtar == -1 and rS.count(deger2) == 0):
            xN = np.append(xN, [[deger2, uygunlukFonk(deger2)]], axis=0)
            rS.append(deger2)
            
        anahtar *= -1


# [+] Tkinter GUI ortamında grafik çizdirmek için alan ayarlanıyor
fig = Figure(figsize = (9, 4), dpi = 150)
canvas = FigureCanvasTkAgg(fig, master = window)
# [-] Tkinter GUI ortamında grafik çizdirmek için alan ayarlanıyor

def goster(kurtlar):
    """
    Kurtların anlık olarak dağ yamacındaki hareketlerini gösterir.
    
    Parameters
    ----------
    kurtlar : kurtlar listesini alır. Listede tüm populasyonun
    konum ve uygunluk değerleri bulunmaktadır.

    Returns
    -------
    None.

    """
    
    plot1 = fig.add_subplot(111)
    plot1.set_title("AV SAHASI")
    plot1.set_ylabel("Yükseklik")
    plot1.set_xlabel("Mesafe")
    
    x = np.linspace(-300, 300, 601, dtype=np.int32) # x ekseni verileri
    y = amacFonk(x)     # y ekseni verileri
    yU = uygunlukFonk(x) # Uygunluk fonksiyonu çizimi için
    
    plot1.plot(x,y, label="Dağın Kesit Yüzey Kenarı")
    plot1.plot(x, yU, color="pink", label="Yüzey Kenar Eğimindeki Değişim")
    plot1.scatter(0, amacFonk(0), color="red", label="Av (Max Eğim)")
    
    xA = kurtlar[0,0] # Alfa Kurdu x konumu
    yA = amacFonk(xA) # Alfa Kurdu y konumu
    
    xB = kurtlar[1,0] # Beta Kurdu x konumu
    yB = amacFonk(xB) # Beta Kurdu y konumu
    
    xD = kurtlar[2,0] # Delta Kurdu x konumu
    yD = amacFonk(xD) # Delta Kurdu y konumu
    
    xT = kurtlar[3:,0] # Teta kurtlarının x konumları
    yT = amacFonk(xT)  # Teta kurtlarının y konumları
    
    
    plot1.scatter(xT, yT, color="gray", label="Teta Kurtları")
    plot1.scatter(xD, yD, color="orange", label="Delta Kurdu")
    plot1.scatter(xB, yB, color="green", label="Beta Kurdu")
    plot1.scatter(xA, yA, color="blue", label="Alfa Kurdu")
    
    plot1.legend()
    canvas.draw()
    canvas.flush_events()
    

def sirala(kurtlar):
    """
    Her iterasyonda kurtların güncellenen konum verilerine göre
    uygunluk değerleri referans alınarak Alfa, Beta ve Delta
    kurtları belirlenir.

    Parameters
    ----------
    kurtlar : kurtlar listesini alır. Listede tüm populasyonun
    konum ve uygunluk değerleri bulunmaktadır.

    Returns
    -------
    xN : Tüm gri kurt populasyonu
    xA : Alfa Kurdu
    xB : Beta Kurdu
    xD : Delta Kurdu

    """
    sirala1 = kurtlar[np.argsort(kurtlar[:,1])]
    xN = np.flip(sirala1, 0) # Listeyi ters çevir
    xA = xN[0]
    xB = xN[1]
    xD = xN[2]
    return xN, xA, xB, xD
    

def avlan():
    """
    max iterasyon sayısı tamamlanana kadar avlanma gerçekleştirir.

    Returns
    -------
    None
    """
    L11.config(text="")
    L10.config(text="Av Başladı")
    
    tempN = xN
    tempXa = xA
    tempXb = xB
    tempXd = xD
    
    t = 0
    while(t < iN):
        Aa, Ca = katsayilar(t) # Alfa kurdu için katsayılar
        Ab, Cb = katsayilar(t) # Beta kurdu için katsayılar
        Ad, Cd = katsayilar(t) # Delta kurdu için katsayılar
        
        for k in range(3, len(tempN)):
            Da = abs(Ca * tempXa[0] - tempN[k][0])
            Db = abs(Cb * tempXb[0] - tempN[k][0])
            Dd = abs(Cd * tempXd[0] - tempN[k][0])
            
            Ua = tempXa[0] - Aa * Da
            Ub = tempXb[0] - Ab * Db
            Ud = tempXd[0] - Ad * Dd
            
            tempN[k][0] = (Ua + Ub + Ud) / 3
            
            tempN[k][1] = uygunlukFonk(tempN[k][0])
            
        tempN, tempXa, tempXb, tempXd = sirala(tempN)
            
        t += 1
        
        fig.clear()
        #print(t, ". iterasyon")
        L11.config(text=str(t)+". iterasyon")
        goster(tempN)
        
    L10.config(text="Av tamamlandı! Alfa Kurdunun Konumu:")
    xKnm = str(round(tempXa[0],2))
    yKnm = str(round(amacFonk(tempXa[0]), 2))
    L11.config(text="x: " + xKnm + " y: " + yKnm + "m")


# [+] Tkinter Python GUI Widget'ler
B = Button(window, text="Ava Başla", command=avlan)
B.grid(row=1, column=0, columnspan=8)

canvas.get_tk_widget().grid(row=2, column=0, columnspan=8)

L10 = Label(window, text="", bg="yellow")
L10.grid(row=3, column=0, columnspan=4, sticky=E, pady=10)

L11 = Label(window, text="", bg="orange")
L11.grid(row=3, column=4, columnspan=4, sticky=W, pady=10)
# [-] Tkinter Python GUI Widget'ler


suruOlustur(pN)
xN, xA, xB, xD = sirala(xN)
goster(xN)


window.mainloop()
