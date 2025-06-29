# -*- coding: utf-8 -*-
"""
Created on Tue May 27 15:29:45 2025

@author: marcp

Aquest codi es el sistema de recomanació per contingut, et permet recomanar
utilitzant la mètrica de cosinus o euclidian.
"""

# Importem llibreries
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from collections import defaultdict
import pandas as pd
import numpy as np
import pickle
import os


# Carreguem el dataframe de metadades
directory = os.getcwd()
path_bd = os.path.join(directory,'TFG_BD_1.csv')
dfa = pd.read_csv(path_bd, sep=";", encoding="latin1")
dfa = dfa[['ranking','song','author','filename', 'genres']]

# Carreguem l'espai de característiques
with open("Allfeatures.pkl", "rb") as f:
    data = pickle.load(f)

# Seleccionem la cançó a recomanar
targetSong = input("\nSelecciona la teva cançó preferida: ") +"_"

# Seleccionem la mètrica per calcular la distància 
option = int(input("\nSelecciona una mètrica per calcular la distància entre cançons: \n\t 1 - cosine\n\t 2 - euclidean (default)\n"))

if option == 1:
    metric = "cosine"
else:
    metric = "euclidean"


# Extraiem el diccionari amb les cançons i features corresponents (sense la target)
X = np.array(list(data.values()))
Y = list(data.keys())

# Normalitzem les features
scaler = StandardScaler()
Xnorm = scaler.fit_transform(X)

    
# Configurem l'algoritme
knn = NearestNeighbors(metric=metric)
knn.fit(Xnorm)

    
# Busquem els fragments de la cançó seleccionada
matches = [i for i,item in enumerate(Y) if item.startswith(targetSong)]

# Obtenim el nom original de la cançó seleccionada per l'usuari
targetSongName = "_".join(targetSong.split("_")[:2])  

# Inicialitzem un diccionari per acumular les recomanacions 
recomanacions = defaultdict(set)

# Generem les recomanacions pels fragments de la cançó triada
for songIndex in matches:
    dist, indexs = knn.kneighbors(Xnorm[songIndex].reshape(1, -1), n_neighbors=10)
    
    # Acumulem les recomanacions dels fragments,traient la cançó seleccionada
    for index in indexs[0]:
        fragmentSong = Y[index]
        originalSong = "_".join(fragmentSong.split("_")[:2])
        
        # Afegim únicament el fragment si no pertany a la cançó seleccionada per l'usuari
        if originalSong != targetSongName:
            recomanacions[originalSong].add(fragmentSong)

# Ordenem les recomanacions per nombre de fragments únics i retornem les 10 primeres.
recomanacions_ordenades = sorted(recomanacions.items(), key=lambda item: len(item[1]), reverse=True)[:10]


# Inicialitzem les llistes per fer les estadístiques de les recomanacions
rankingList = list()
genresList = list()
recomanacionsInfo = list()

print("\n Et recomano que escolits aquestes cançons...\n")
for i, (k,v) in enumerate(recomanacions_ordenades):
    
    # Extraiem les metadades de la cançó
    metadades = dfa[dfa["filename"] == k]
    ranking = int(metadades["ranking"].values[0])
    name = metadades["song"].values[0]
    author = metadades["author"].values[0]
    genres = metadades["genres"].values[0]
    
    # Mostrem la informació de la recomanació
    print(f"{i} - {k} amb {len(v)} fragments")
    print(f"\t- Cançó: {name}")
    print(f"\t- Autor(s): {author}")
    print(f"\t- Gèneres: {genres}\n")
    
    recomanacionsInfo.append({
            "Posicio": i,
            "Cançó": name,
            "Autor": author,
            "Gèneres": genres,
            "Fragments recomanats": len(v),
            "Ranking":ranking
        })
    
    
    # Acumulem les metadades necessaries per les estadístiques de la recomanació
    rankingList.append(ranking)   
    for genre in genres.split(","):
        genresList.append(genre.strip())
  
# Calculem les estadístiques
print("Ranking promig de les recomanacions: ",np.mean(rankingList))
genreStats = pd.Series(genresList).value_counts(normalize=True) * 100
for g,pct in genreStats.items():
    print(f" - {g}: {pct:.2f}%")
    
df = pd.DataFrame(recomanacionsInfo)
df.to_csv(f"recomanacions_{targetSong}{metric}.csv", index=False, encoding="latin1")

 