# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 20:30:09 2025

@author: marcp

Aquest codi es necessari per generar els gràfics pels diferents espais de
la classificació de punts atípics pels possibles valors d'èpsilon i minSamples

"""
# Importem les llibreries necessaries
import pickle
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import plotly.io as pio

# Configuració per obrir el gràfic un cop creat directament
pio.renderers.default = "browser"  

# Triar el subespai per veure l'evolució dels clústers
option = int(input("""\nTria un espai de característiques per mostrar la seva evolució\n: 
                   
                   \t 0 - Espai total de característiques\n
                   \t 1 - Primer subespai de característiques\n
                   \t 2 - Segon subespai de característiques\n
                   \t 3 - Tercer subespai de característiques\n"""))

if option == 0:
    pkl = "Allfeatures.pkl" # Arxiu amb les característiques
    epsilons = [round(e, 2) for e in np.arange(1.4, 5.5, 0.1)] # Èpsilons on hi ha evolució
    html = "PercentatgeOutliersAF.html" # Fitxer on guardar el gràfic
    title = "Espai Total" # Títol per actualizar el gràfic
elif option == 1:
    pkl = "FeatureExtraction1.pkl"
    epsilons = [round(e, 2) for e in np.arange(0.1, 1.1, 0.1)]
    html = "PercentatgeOutliersF1.html"
    title = "Subespai 1"
elif option == 2:
    pkl = "FeatureExtraction2.pkl"
    epsilons = [round(e, 2) for e in np.arange(1.0, 4.5, 0.1)]
    html = "PercentatgeOutliersF2.html"
    title = "Subespai 2"
elif option == 3:
    pkl = "FeatureExtraction3.pkl"
    epsilons = [round(e, 2) for e in np.arange(0.4, 2.8, 0.1)]
    html = "PercentatgeOutliersF3.html"
    title = "Subespai 3"
    

# Recuperem de l'arxiu pkl els fragments i les seves característiques
with open(pkl, "rb") as f:
    data = pickle.load(f)

X = np.array(list(data.values())) # Característiques
Y = list(data.keys()) # Fragments

# Normalitzem les característiques
scaler = StandardScaler()
X_norm = scaler.fit_transform(X)

# Determinem el mínim de punts per agrupació
minSamples = [4, 6, 8, 10]

# Diccionari per guardar els percentatges d'outliers de cada mínim de punts
outliersResults = {sample: list() for sample in minSamples}

# Executem l'algoritme pels diferents mínims de punts
for sample in minSamples:
    # Executem l'algoritme pels diferents valors d'èpsilon
    for epsilon in epsilons:
        dbscan = DBSCAN(eps=epsilon, min_samples=sample, metric='euclidean')
        labels = dbscan.fit_predict(X_norm) # Recuperem els clústers

        # Calculem el percentatge de punts atípics
        nOutliers = np.sum(labels == -1) 
        pctOutliers = (nOutliers / len(labels)) * 100
       
        # Guardem els resultats
        outliersResults[sample].append(pctOutliers)

# Creació del gràfic amb PLOTLY
fig = go.Figure()

for sample in minSamples:
    fig.add_trace(go.Scatter(
        x=epsilons,
        y=outliersResults[sample],
        mode='lines+markers',
        name=f'{sample}'
    ))

fig.update_layout(
    title=f"Percentatge de punts atípics vs Èpsilon x minSamples ({title})",
    width=1100,  # Amplada 
    height=700,  # Alçada
    title_font=dict(size=30),
    xaxis=dict(
        title='Èpsilon',
        title_font=dict(size=32, family='Arial', color='black'),
        tickfont=dict(size=34, family='Arial', color='black')
    ),
    yaxis=dict(
        title="Percentatge de punts atípics (%)",
        title_font=dict(size=32, family='Arial', color='black'),
        tickfont=dict(size=34, family='Arial', color='black')
    ),
    legend=dict(
        title='MinPunts',
        font=dict(size=30, family='Arial', color='black')  
    ),
    template='plotly_white'
)

# Guardem el gràfic en html
fig.write_html(html)

