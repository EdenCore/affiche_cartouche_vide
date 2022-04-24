# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 16:05:34 2022

@author: Kévin Moutoussamy

@Description:
    
 Le programme va ouvrir la page de gestion des mopieurs inscrits dans un fichier
 Puis récupérer le niveau d'encre et de tambour et afficher dans un tableau
 
"""

import os
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
from tabulate import tabulate
options=webdriver.FirefoxOptions()
options.set_capability('acceptSslCerts', False)
# Il faut pointer l'executable de geckodriver pour firefox. Si c'est sur chrome, utiliser un autre driver
service = Service('geckodriver.exe',log_path=os.path.dirname(os.path.abspath(__file__))+'/geckodriver.log')
driver = Firefox(service=service, options=options)
resultat = []
elements_mopieur = ["Cartouche Noir","Tambour Noir","Cartouche cyan","Tambour cyan","Cartouche magenta","Tambour magenta","Cartouche jaune","Tambour jaune","Kit de transfert","Kit de fusion"]
fichier_mopieur = open(os.path.dirname(os.path.abspath(__file__))+'/liste_mopieurs.csv', "r")
# La variable prends les valeurs ligne par ligne
data_mopieur = str(fichier_mopieur.readline())
# C'est pour éviter de recopier plusieurs fois le dsp
while data_mopieur != '':
    ip_mopieur = 'http://' + str(data_mopieur[data_mopieur.index(',')+1:len(data_mopieur)])
    dsp_mopieur = str(data_mopieur[:data_mopieur.index(',')])
    page = driver.get(ip_mopieur)
    soup = BeautifulSoup(driver.page_source,features='html.parser')
    ligne_resultat = []
    for i in range (11):
        quantite = soup.find("span", {"id":"SupplyGauge"+str(i)}).text
        if quantite == "2%":
            if ligne_resultat == []:
                ligne_resultat.append(dsp_mopieur)
            ligne_resultat.append(elements_mopieur[i])
    resultat.append(ligne_resultat)
    data_mopieur = str(fichier_mopieur.readline())
print(tabulate(resultat,showindex="always"))
driver.close()