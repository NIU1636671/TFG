# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 9:30:09 2025

@author: marcp

Aquest codi es necessari per generar els gràfics que representen el espai
bidimensional (nombre de clústers generats, % d'outliers generats), el gràfic
preten analitzar la tendència de classificació de les cançons en les primeres 
i darreres posicions del rànquing Billboard.

"""


# Importem les llibreries necessaries
import pickle
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from collections import defaultdict, Counter
import pandas as pd
import plotly.io as pio

# Configuració per obrir el gràfic un cop creat directament
pio.renderers.default = "browser"  

# Triar quina part del rànquing vols analitzar
option1 = int(input("""\nTria una opció: \n: 
                   
                   \t 1 - TOP 10 cançons\n
                   \t 2 - BOTTOM 10 cançons\n"""))

# Triar el subespai per veure la tendència de classificació
option2 = int(input("""\nTria un espai de característiques per mostrar la seva classificació\n: 
                   
                   \t 0 - Espai total de característiques\n
                   \t 1 - Primer subespai de característiques\n
                   \t 2 - Segon subespai de característiques\n
                   \t 3 - Tercer subespai de característiques\n"""))


if option1 == 1:
    # Es defineix el top 10 com song_1 a song_10
    rankSongs = [f"song_{i}" for i in range(1, 11)]
    html = "Top10"
    title = "Clústers, % punts atípics per les primeres 10 cançons a "
    
elif option1 == 2:
    # Es defineix el bottom 10 com song_191 a song_200
    rankSongs = [f"song_{i}" for i in range(191, 200)]
    html = "Bottom10"
    title = "Clústers, % punts atípics per les darreres 10 cançons a "
    
if option2 == 0:
    pkl = "Allfeatures.pkl" # Arxiu amb les característiques
    epsilons = [round(e, 2) for e in np.arange(1.4, 5.5, 0.1)] # Èpsilons on hi ha evolució
    html += "AF.html"
    title+= "(Espai total)"
    
elif option2 == 1:
    pkl = "FeatureExtraction1.pkl"
    epsilons = [round(e, 2) for e in np.arange(0.1, 1.1, 0.1)]
    html += "F1.html"
    title += "(Subespai 1)"
    
elif option2 == 2:
    pkl = "FeatureExtraction2.pkl"
    epsilons = [round(e, 2) for e in np.arange(1.0, 4.5, 0.1)]
    html += "F2.html"
    title += "(Subespai 2)"
elif option2 == 3:
    pkl = "FeatureExtraction3.pkl"
    epsilons = [round(e, 2) for e in np.arange(0.4, 2.8, 0.1)]
    html += "F3.html"
    title += "(Subespai 3)"
    

# Recuperem les característiques
with open(pkl, "rb") as f:
    data = pickle.load(f)

X = np.array(list(data.values())) # Guardem les característiques
Y = list(data.keys()) # Guardem els fragments

# Extraiem el nom original de les cançons (separant-les del fragment)
songNames = ["_".join(name.split("_")[:2]) for name in Y]

# Normalitzem les característiques
scaler = StandardScaler()
Xnorm = scaler.fit_transform(X)

# Configurem el mínim de punts
minSamples = 8

rows = []

# Executem per cada èpsilon l'algoritme DBSCAN
for eps in epsilons:
    dbscan = DBSCAN(eps=eps, min_samples=minSamples)
    labels = dbscan.fit_predict(Xnorm)

    # Assignem etiquetes a cada fragment
    df_labels = pd.DataFrame({
        "fragment": Y,
        "song": songNames,
        "label": labels
    })
    
    # Obtenim la informació de cada cançó a partir de les cançons del top/bottom 10
    for song in rankSongs:
        song_df = df_labels[df_labels["song"] == song]
        labelsSong = song_df["label"]

        uniqueClusters = set(labelsSong) - {-1}  # Excluim els no classificats
        nClusters = len(uniqueClusters) # Recompte dels clústers únics
        pctOutliers = 100 * np.sum(labelsSong == -1) / len(labelsSong) # Calculem el percentatge d'outliers

        rows.append({
            "song": song,
            "epsilon": eps,
            "numClusters": nClusters,
            "pctOutliers": pctOutliers
        })

df = pd.DataFrame(rows)

# Fem el gràfic amb PLOTLY

fig = px.scatter(
    df,
    x="numClusters",
    y="pctOutliers",
    color="song",              # Color únic per cada cançó
    symbol="song",             # Símbols únics per cada cançó
    hover_data=["epsilon"],    # Mostrar epsilon en hover
    title=title,
    labels={
        "numClusters": "Nombre de clústers únics",
        "pctOutliers": "% de fragments no classificats",
        "epsilon": "ε"
    },size_max=8  
)

# Personalització del gràfic per tenir els símbols més grans o més petits
fig.update_traces(
    marker=dict(
        size=18,  # Mida dels símbols
        line=dict(width=2, color='DarkSlateGrey')  # Silueta
    ),
    selector=dict(mode='markers')
)

# Personalització del disseny del gràfic (eixos, títol, llegenda)
fig.update_layout(
    title_font=dict(size=30),
    width=1100,  # Amplada
    height=900,  # Alçada
    xaxis=dict(
        title_font=dict(size=34, family='Arial', color='black'),
        tickfont=dict(size=34, family='Arial', color='black'),
        tickmode='linear',
        dtick=1
    ),
    yaxis=dict(
        title_font=dict(size=34, family='Arial', color='black'),
        tickfont=dict(size=34, family='Arial', color='black')
    ),
    legend=dict(
        title='Cançons',
        font=dict(size=30, family='Arial', color='black')),  
    template='plotly_white'
)

fig.write_html(html)
fig.show()
