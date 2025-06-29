# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 21:16:49 2025

@author: marcp

Aquest codi es necessari per generar els gràfics de K-distàncies pels espais
de la BD, i marcar l'èpsilon òptima per poder estudiar el comportament de 
l'algoritme en un futur.
"""

# Importem les llibreries necessaries
import pickle
import numpy as np
import plotly.graph_objects as go
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from kneed import KneeLocator
import plotly.io as pio

# Configuració per obrir el gràfic un cop creat directament
pio.renderers.default = "browser"  

# Triar el subespai per veure l'evolució dels clústers
option = int(input("""\nTria un espai de característiques per generar el gràfic de les K-distàncies\n: 
                   
                   \t 0 - Espai total de característiques\n
                   \t 1 - Primer subespai de característiques\n
                   \t 2 - Segon subespai de característiques\n
                   \t 3 - Tercer subespai de característiques\n"""))


if option == 0:
    pkl = "Allfeatures.pkl" # Arxiu amb les característiques
    html = "KdistAF.html" # Fitxer on guardar el gràfic
    title = "Espai Total" # Títol per actualizar el gràfic
    
elif option == 1:
    pkl = "FeatureExtraction1.pkl"
    html = "KdistF1.html"
    title = "Subespai 1"
    
elif option == 2:
    pkl = "FeatureExtraction2.pkl"
    html = "KdistF2.html"
    title = "Subespai 2"
    
elif option == 3:
    pkl = "FeatureExtraction3.pkl"
    html = "KdistF3.html"
    title = "Subespai 3"
    

# Recuperem de l'arxiu pkl els fragments i les seves característiques
with open(pkl, "rb") as f:
    data = pickle.load(f)

X = np.array(list(data.values())) # Característiques
Y = list(data.keys()) # Fragments

# Normalitzem les característiques
scaler = StandardScaler()
Xnorm = scaler.fit_transform(X)

# Calculem el gràfic de les K-distàncies
k = 8 # Definim la distància al vuité veí
neigh = NearestNeighbors(n_neighbors=k) # Inicialitzem l'algoritme
neigh.fit(Xnorm) # Entrenem l'algoritme amb les característiques normalitzades
distances, indexs = neigh.kneighbors(Xnorm) # Obtenim les distàncies i els indexs
kDistances = np.sort(distances[:, k-1]) # Ordenem les distàncies de forma ascendent

# Detectem el "colze" automaticament amb la llibreria importada
kneedle = KneeLocator(
    x=np.arange(len(kDistances)),
    y=kDistances,
    curve='convex',
    direction='increasing'
)

# Obtenim l'èpsilon (distància) òptima
epsilon = kDistances[kneedle.knee] if kneedle.knee is not None else None
# Obtenim l'index per situar-lo al gràfic
epsilonIndex = kneedle.knee

# Creació del graf amb PLOTLY
fig = go.Figure()

# Mostrem les distàncies en un scatter plot 
fig.add_trace(go.Scatter(
    x=np.arange(len(kDistances)),
    y=kDistances,
    mode='lines',
    name=f'{k}-distancies',
    line=dict(color='blue')
    ))

# Afegim el punt vermell (èpsilon) si s'ha detectat
if epsilonIndex is not None:
    fig.add_trace(go.Scatter(
    x=[epsilonIndex],
    y=[epsilon],
    mode='markers',
    name='Èpsilon detectat',
    marker=dict(size=30, color='red')
    ))

    # Afegim una etiqueta sobre el punt per visualitzar millor el valor òptim
    fig.add_annotation(
    x=epsilonIndex - 500,  # Posició X de la etiqueta
    y=epsilon + 0.30, # Posició Y de la etiqueta
    text=f"ε = {epsilon:.2f}", # Text de la etiqueta
    showarrow=False,
    font=dict(size=40, color="black"), # Font de la etiqueta
    align="left", # Alineació del text
    bgcolor="white", # Fons blanc a l'etiqueta
    bordercolor="black", # Fons negre de l'etiqueta
    borderwidth=1,
    borderpad=4)   


# Configuració estètica del grafic
fig.update_layout(
    title=f"Gràfic de K-distàncies i estimació d'èpsilon òptim ({title})",
    width=1200,   # Amplada
    height=700,   # Alçada
    font=dict(size=24), # Text base
    showlegend=False,
    xaxis=dict( # Configuració de l'eix X
        title= 'Fragments ordenats',
        title_font=dict(size=32, family='Arial', color='black'),
        tickfont=dict(size=34, family='Arial', color='black')
    ),

    yaxis=dict( # Configuració de l'eix Y
        title='Distància al 8-èsim veí',
        title_font=dict(size=32, family='Arial', color='black'),
        tickfont=dict(size=34, family='Arial', color='black')
    ))


fig.write_html(html)
fig.show()
