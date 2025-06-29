# -*- coding: utf-8 -*-
"""
Created on Sat May 10 17:33:31 2025

@author: marcp

Aquest codi serveix per representar la distribució de les posicions 
de les cançons en el ràquing de Billboard, de cada gènere musical. Es fa servir
un daigrama de caixa per poder fer un anàlisi complet i una bona comparació.
Addicionalment, també es guarda en dos arxius csv, la quantitat de fragments de 
cada gènere i les posicions de les cançons per cada gènere.
"""

# Importem les llibreries necessaries per implementar el codi
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import pandas as pd
from plotly.subplots import make_subplots

# Carregem les metadades de la BD en un dataframe
df = pd.read_csv("TFG_BD_1.csv",encoding='latin1',sep=';')

# Ordenem el dataframe per ranking
dfOrdenat = df.sort_values(by="ranking")

# Inicialitzem diccionaris per guardar els gèneres, el fragments i el rànquing per pròxims anàlisis
generesFragments = defaultdict(list)
generesRankings = defaultdict(list)

# Extraiem les metadades cançó a cançó
for i, (generes, fragments) in enumerate(zip(dfOrdenat['genres'],dfOrdenat['num_fragments'])):
    # per cada gènere de la cançó (pot ser una llista), es guarda el nombre de gragments i la posició en la que es troba.
    for genere in [g.strip() for g in generes.split(',')]:
        generesFragments[genere].append(int(fragments))
        generesRankings[genere].append(i+1)

# Guardem el total de fragments de les cançons (per recuperar el nombre de cançons, dividim cada num_fragments pel total de fragments de la BD)
generesVolum = {k: sum(v) for k, v in generesFragments.items() if len(v) >= 5}
# Guardem en un diccionari la llista de posicions per gènere, únicament si tenen més de cinc cançons a la base de dades
generesRanking = {k: v for k, v in generesRankings.items() if len(v) >= 5}

# Ordenem el diccionari per nombre de cançons per millorar la visualització
boxplotRanking = dict(sorted(generesRanking.items(), key=lambda item: len(item[1]),reverse=True))

# Guardem el diccionari de ranking en un dataframe
dfRankings = pd.DataFrame([(genere, posicio) for genere, ranking in boxplotRanking.items() for posicio in ranking],
                  columns=["GÈNERE", "POSICIÓ"])
# Amb la llibreria plotly, creem el boxplot que haurem de dividir en dues parts per millorar la visualització

# Convertim el diccionari de ranking en dos dataframe
dfRankings_1 = pd.DataFrame([(genere, posicio) for genere, ranking in list(boxplotRanking.items())[:9] for posicio in ranking],
                  columns=["GÈNERE", "POSICIÓ"])

dfRankings_2 = pd.DataFrame([(genere, posicio) for genere, ranking in list(boxplotRanking.items())[9:] for posicio in ranking],
                  columns=["GÈNERE", "POSICIÓ"])


# Generem dues figures per repartir els diagrames en dos files
fig1 = px.box(dfRankings_1, x="GÈNERE", y="POSICIÓ", points='all', color_discrete_sequence=["purple"])
fig2 = px.box(dfRankings_2, x="GÈNERE", y="POSICIÓ", points='all', color_discrete_sequence=["purple"])

# Inicialitzem la figura final on unim les dues figures anteriors
fig = make_subplots(rows=2, cols=1, vertical_spacing=0.3)

# Afegim els subplots a cada fila
for trace in fig1.data:
    fig.add_trace(trace, row=1, col=1)

for trace in fig2.data:
    fig.add_trace(trace, row=2, col=1)

# Configuració estètica
fig.update_layout(
    height=1000,
    font=dict(size=32),
    showlegend=False,
    xaxis_tickangle=45,
    xaxis=dict(
        title= 'GÈNERE',
        title_font=dict(size=30, family='Arial', color='black'),
        tickfont=dict(size=26, family='Arial', color='black')
    ),
    xaxis2=dict(
        title= 'GÈNERE',
        title_font=dict(size=30, family='Arial', color='black'),
        tickfont=dict(size=26, family='Arial', color='black')
    ),
    yaxis=dict(
        title='POSICIÓ',
        title_font=dict(size=28, family='Arial', color='black'),
        tickfont=dict(size=26, family='Arial', color='black')
    ),
    yaxis2=dict(
        title='POSICIÓ',
        title_font=dict(size=28, family='Arial', color='black'),
        tickfont=dict(size=26, family='Arial', color='black')
    )
)

# Mostrem per navegador el resultat i guardem en un arxiu html el gràfic.
pio.renderers.default = "browser"
fig.show()
fig.write_html("BoxplotGèneresxRankinh.html")

# Guardem el volum de fragments per rànquing per futurs anàlisi en un csv
dfVolum = pd.DataFrame(list(generesVolum.items()), columns=["Genere", "TotalFragments"])
dfVolum.to_csv("fragmentsXGenere.csv", index=False)
dfRankings.to_csv("rankingxGenere.csv",index = False)



        
