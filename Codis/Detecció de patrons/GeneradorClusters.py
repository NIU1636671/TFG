# -*- coding: utf-8 -*-
"""
Created on Wed May 28 15:54:00 2025

@author: marcp


Aquest codi es necessari per generar els clústers de l'algoritme DBSCAN amb
els diferents espais de característiques. Es poden generar directament en els
altres codis, però aquesta és la manera de fer-ho.

"""


# Importem les llibreries necessaries
import pickle
import pretty_midi
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import json

# Triar el subespai per generar clusters
option = int(input("""\nTria un espai de característiques per generar clústers\n: 
                   
                   \t 0 - Espai total de característiques\n
                   \t 1 - Primer subespai de característiques\n
                   \t 2 - Segon subespai de característiques\n
                   \t 3 - Tercer subespai de característiques\n"""))

minPts = int(input("Introdueix el mínim de punts que vols per agrupar: "))
maxPts = int(input("Introdueix el màxim de punts que vols per agrupar: "))

if option == 0:
    pkl = "Allfeatures.pkl" # Arxiu amb les característiques
    epsilons = [round(e, 2) for e in np.arange(1.4, 5.5, 0.1)] # Èpsilons on hi ha evolució
    title = "Espai Total" # Títol per actualizar el gràfic
   
elif option == 1:
    pkl = "FeatureExtraction1.pkl"
    epsilons = [round(e, 2) for e in np.arange(0.1, 1.1, 0.1)]
    title = "Subespai 1"
    
elif option == 2:
    pkl = "FeatureExtraction2.pkl"
    epsilons = [round(e, 2) for e in np.arange(1.0, 4.5, 0.1)]
    title = "Subespai 2"
    
elif option == 3:
    pkl = "FeatureExtraction3.pkl"
    epsilons = [round(e, 2) for e in np.arange(0.4, 2.8, 0.1)]
    title = "Subespai 3"
    

# Recuperem de l'arxiu pkl els fragments i les seves característiques
with open(pkl, "rb") as f:
    data = pickle.load(f)

X = np.array(list(data.values())) # Característiques
Y = list(data.keys()) # Fragments

# Normalitzem les característiques
scaler = StandardScaler()
X_norm = scaler.fit_transform(X)


for sample in np.arange(minPts, maxPts, 2):
    for epsilon in epsilons:
        # Apliquem DBSCAN 
        dbscan = DBSCAN(eps=epsilon, min_samples=sample,metric='euclidean')  
        clusters = dbscan.fit_predict(X_norm)
        
        # Guardar opcional
        diccionari = {}           
        for i,j in zip(Y,clusters):
            diccionari[i] = int(j)
        
        with open(f'Clusters_{epsilon}_{sample}_{title}.json', "w", encoding="utf-8") as f:
            json.dump(diccionari, f, ensure_ascii=False, indent=4)