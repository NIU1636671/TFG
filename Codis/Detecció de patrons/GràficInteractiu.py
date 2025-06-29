# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 18:58:37 2025

@author: marcp
"""

# Importem les llibreries
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
import umap
import plotly.graph_objects as go
import os
import ast
from plotly.subplots import make_subplots

# Fem el mapping de gèneres derivats a gèneres generals
genreMapping = {
    'Pop': 'Pop', 'Dance Pop': 'Pop', 'Synth Pop': 'Pop', 'Alternative Pop': 'Pop',
    'Soft Rock': 'Rock', 'Pop Rock': 'Rock', 'Rock': 'Rock', 'Hard Rock': 'Rock', 'Reggae Rock': 'Rock',
    'Country Rock': 'Country', 'Indie Rock': 'Indie', 'Indie Pop': 'Indie', 'Indie': 'Indie',
    'Indie Folk': 'Indie', 'Folk': 'Indie', 'Folk Rock': 'Indie',
    'Country': 'Country', 'Country Pop': 'Country', 'Country Folk': 'Country', 'Southern Rock': 'Country',
    'Latin Urban': 'Latin', 'Reggaeton': 'Latin', 'Trap Latino': 'Latin',
    'Corridos tumbados': 'Latin', 'Bachata': 'Latin', 'Reggae': 'Latin',
    'Afrobeats': 'Urban', 'Dancehall': 'Urban',
    'Hip-Hop': 'Hip-Hop/Rap', 'Rap': 'Hip-Hop/Rap', 'Trap': 'Hip-Hop/Rap',
    'R&B': 'R&B/Soul', 'Soul': 'R&B/Soul',
    'Electropop': 'Electronic', 'EDM': 'Electronic', 'Disco': 'Electronic', 'House': 'Electronic',
    'Christmas': 'Other', 'Infantil': 'Other',
    'K-Pop': 'Pop', 'Heavy Metal': 'Rock', 'Alternative Rock': 'Rock'
}

# Obtenim el directori actual 
directory = os.getcwd()
# Formem la ruta completa del fitxer CSV
pathBD = os.path.join(directory, 'TFG_BD_1.csv')
# Llegeix el fitxer CSV amb separador ";" 
dfa = pd.read_csv(pathBD, sep=";", encoding="latin1")

# Creem una nova columna amb el gènere general aplicant la funció de mapeig
dfa['genre_general'] = dfa['genres'].apply(
    lambda g: genreMapping.get(g.split(",")[0].replace("['", "").replace("']", "").strip(), "Other")
)

# S'extreu el nom base de la cançó
dfa['fragment_base'] = dfa['filename'].apply(lambda x: os.path.splitext(x)[0])


# Carreguem les característiques
with open("AllFeatures.pkl", "rb") as f:
    data = pickle.load(f)

X = np.array(list(data.values()))
Y = list(data.keys())

# Normalitzem les característiques
scaler = StandardScaler()
Xnorm = scaler.fit_transform(X)

# Calculem la reducció de característiques amb PCA
pca = PCA(n_components=2)
PCA_2D = pca.fit_transform(Xnorm)

# Reducció de dimensionalitat amb t-SNE
tsne = TSNE(n_components=2, perplexity=30, learning_rate=200, random_state=42)
TSNE_2D = tsne.fit_transform(Xnorm)

# Reducció de dimensionalitat amb UMAP
umapModel = umap.UMAP(n_components=2, random_state=42)
UMAP_2D = umapModel.fit_transform(Xnorm)

# Definim els parametres del DBSCAN
epsilons = [round(e, 2) for e in np.arange(1.4, 5.8, 0.2)]
min_samples = 8

# Assignem símbols per gènere
unique_genres = sorted(dfa['genre_general'].dropna().unique())
symbol_map = {genre: i for i, genre in enumerate(unique_genres)}



# Funció per preparar el dataframe 
def prepararDataFrame(data_2D):
    # El dataframe té coordenades x,y (característiques)
    df = pd.DataFrame(data_2D, columns=['x', 'y'])
    # Afegim també una columna pel id del fragment
    df['fragment'] = Y
    # Afegim també una columna amb l'id de la  cançó
    df['song'] = ["_".join(name.split("_")[:2]) for name in Y]
    # Fem un merge amb el dataframe original (metadades) per obtenir el gènere general i el títol de la cançó
    df = df.merge(dfa[['fragment_base', 'genre_general', 'song']], left_on='song', right_on='fragment_base', how='left')
    # Canvia el nom de la columna creada automaticament pel merge.
    df.rename(columns={'song_y': 'title'}, inplace=True)
    # Elimina les columnes que ja no ens fan falta.
    df.drop(columns=['fragment_base'], inplace=True)
    # Afeim una columna de símbol per saber quin símbol tenen els fragment
    df['symbol'] = df['genre_general'].map(symbol_map)
    return df

# Crearem subgràfics de 1 fila 3 columnes
fig = make_subplots(
    rows=1, cols=3, 
    subplot_titles=("PCA", "t-SNE", "UMAP"), # Definim els títols
    shared_yaxes=True # Comparteixen eix Y
)

# Funció per afegir "frames" interactius per cada tècnica de reducció dimensional
def afegirFrames(fig, dfBase, col, tecnica):

    # Iterem per cada valor d'epsilon del DBSCAN
    for i, eps in enumerate(epsilons):
        df = dfBase.copy()  # Fem una còpia del DataFrame base per no modificar-lo

        # Executem DBSCAN per l'epsilon actual
        db = DBSCAN(eps=eps, min_samples=min_samples)
        df['cluster'] = db.fit_predict(Xnorm)  

        # Np considerem els punts atípics.
        df = df[df['cluster'] != -1]

        # Preparem una llista de visibilitats per controlar què es mostra a cada moment
        visible = [False] * len(fig.data)

        # Creem un objecte Scatter de Plotly per representar els punts
        scatter = go.Scatter(
            x=df['x'],
            y=df['y'],
            mode='markers',  
            marker=dict(
                color=df['cluster'], # Color segons el clúster
                symbol=df['symbol'], # Forma segons el gènere
                colorscale='Viridis',       
                size=7,                    
                line=dict(width=0),       
                showscale=(col == 1 and i == 0)  
            ),
            # Etiqueta de cada fragment
            text=df.apply(lambda row: f"Títol: {row['title']}<br>Fragment: {row['fragment']}<br>Gènere: {row['genre_general']}<br>Clúster: {row['cluster']}", axis=1),
            hoverinfo='text',
            name=f'{tecnica} èpsilon={eps}',  
            visible=(i == 0)  
        )

        # Afegim el "trace" al gràfic en la columna corresponent
        fig.add_trace(scatter, row=1, col=col)

    start_idx = len(fig.data) - len(epsilons)

    steps = []
    for i, eps in enumerate(epsilons):
        # Creem una llista que posa només un traç en visible a la vegada
        visibles = [True if j == (start_idx + i) else fig.data[j].visible for j in range(len(fig.data))]
        steps.append(dict(
            method='update',                  
            args=[{'visible': visibles}],     
            label=str(eps)                  
        ))
    slider = dict(
        active=0,     
        steps=steps,  
        x=0.33 * (col - 1),   
        xanchor="left",
        y=0,
        yanchor="top",
        pad=dict(t=10),  
        len=0.3          
    )


    return slider

# Generem els tres gràfics per separat
slider1 = afegirFrames(fig, prepararDataFrame(PCA_2D), 1, "PCA")
slider2 = afegirFrames(fig, prepararDataFrame(TSNE_2D), 2, "t-SNE")
slider3 = afegirFrames(fig, prepararDataFrame(UMAP_2D), 3, "UMAP")

# Diseny final del gràfic
fig.update_layout(
    title='Comparació de tècniques de reducció dimensional amb DBSCAN · Color: Clúster · Forma: Gènere',
    height=700,
    width=1400,
    sliders=[slider1, slider2, slider3],
    showlegend=False
)

fig.show()
fig.write_html("Clustering_Comparació_PCA_TSNE_UMAP.html", full_html=True)
