# -*- coding: utf-8 -*-
"""
Created on Sun Jun  1 20:19:54 2025

@author: marcp

Aquest codi serveix per graficar la generació de clústers dels diferents
espais de característiques variant l'èpsilon i el mínim de punts.
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
    html = "EvolucioClustersAF.html" # Fitxer on guardar el gràfic
    title = "Espai Total" # Títol per actualizar el gràfic
elif option == 1:
    pkl = "FeatureExtraction1.pkl"
    epsilons = [round(e, 2) for e in np.arange(0.1, 1.1, 0.1)]
    html = "EvolucioClustersF1.html"
    title = "Subespai 1"
elif option == 2:
    pkl = "FeatureExtraction2.pkl"
    epsilons = [round(e, 2) for e in np.arange(1.0, 4.5, 0.1)]
    html = "EvolucioClustersF2.html"
    title = "Subespai 2"
elif option == 3:
    pkl = "FeatureExtraction3.pkl"
    epsilons = [round(e, 2) for e in np.arange(0.4, 2.8, 0.1)]
    html = "EvolucioClustersF3.html"
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

# Diccionari per guardar els clústers generats de cada mínim de punts
results = {sample: list() for sample in minSamples}

# Executem l'algoritme per cada mínim de punts
for sample in minSamples:
    # Executem per cada èpsilon l'algoritme
    for epsilon in epsilons:
        dbscan = DBSCAN(eps=epsilon, min_samples=sample, metric='euclidean') # Especifiquem la distància euclidiana
        labels = dbscan.fit_predict(X_norm) # Recuperem els clústers

        # recompte dels clústers generats, evitant els no classificats.
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        # Guardem el resultat
        results[sample].append(n_clusters) 


# Creació del gràfic amb PLOTLY
fig = go.Figure()

# Per cada mínim de punts es crea un scatter plot
for sample in minSamples:
    fig.add_trace(go.Scatter(
        x=epsilons,
        y=results[sample],
        mode='lines+markers',
        name=f'{sample}'
    ))
    
# Comanda per actualitzar el disseny del gràfic
fig.update_layout(
    title=f"Nombre de clústers generats vs Èpsilon x minSamples ({title})",
    title_font=dict(size=30),
    width=1100,  # Amplada del gràfic
    height=700,  # Alçada del gràfic
    margin=dict(l=80, r=40, t=100, b=80),  # Marges
    xaxis=dict( 
        title='Èpsilon',
        title_font=dict(size=34, family='Arial', color='black'),
        tickfont=dict(size=35, family='Arial', color='black')
    ),
    yaxis=dict(
        title="Nombre de clústers",
        title_font=dict(size=34, family='Arial', color='black'),
        tickfont=dict(size=35, family='Arial', color='black')
    ),
    legend=dict(
        title='MinPunts',
        font=dict(size=30, family='Arial', color='black')
    ),
    template='plotly_white'
)

fig.write_html(html)
fig.show()
