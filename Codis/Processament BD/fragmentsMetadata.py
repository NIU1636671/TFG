# -*- coding: utf-8 -*-
"""
Created on Sun May 11 18:41:56 2025

@author: marcp

Aquest codi serveix per actualitzar el fitxer de metadades amb les columnes
del nombre de fragments que es pot partir una cançó i la duració de l'audio
"""

# Importar llibreries
import os
import pandas as pd
from pydub import AudioSegment

# Carregar les metadades de la base de dades
df = pd.read_csv("TFG_BD_1.csv", sep=";",encoding="latin1")

# Inicialitzem dues llistes, per guardar les duracions i fragments
duracions = list()
fragments = list()

# Recorrem totes les cançons
for song in range(1,201):
    folder = f"song_{song}"
    filename = folder + ".mp3"
    filePath = os.path.join(folder, filename)
 
    # Comprovem si existeix l'arxiu
    if os.path.exists(filePath):
        
        # Carreguem el audio amb el filePath
        audio = AudioSegment.from_mp3(filePath)
        # Obtenim la duració en milisegons
        duracioMs = len(audio)
        # Convertim en minuts la duració
        minuts = duracioMs // 60000
        # Obtenim els segons de la duració
        segons = (duracioMs % 60000) // 1000
        duracioStr = f"{minuts:02}:{segons:02}"
        # Calculem quants fragments de 12 segons es poden fer en ms
        duracioFragment = 12 * 1000  
        nfragments = duracioMs // duracioFragment
        
    else:
        print(f"No s'ha trobat': {filePath}")
        duracioStr = ""

    # Guardem tant la duració com el nombre de fragments de la cançó
    duracions.append(duracioStr)
    fragments.append(nfragments)

# Afegim a l'arxiu de metadades dues noves columnes
df['duration'] = duracions
df['num_fragments'] = fragments
df.to_csv("TFG_BD_1.csv", index=False, sep=";",encoding="latin1")
