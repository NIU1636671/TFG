# -*- coding: utf-8 -*-
"""
Created on Sun May 11 8:41:56 2025

@author: marcp

Aquest codi serveix per segmentar les cançons en fragments de 12 segons, i
guardar els fragments en nous arxius dins de la carpeta corresponent
"""

# Importar les llibreries necessaries
import os
from pydub import AudioSegment

def splitSongsMP3(base):
    
    # Recorrem els elements del directori actual
    for folderName in os.listdir(base):
        
        # Verificar si l'element comença amb l'estructura indicada
        if not folderName.startswith("song_"):
            continue
        
        # Recuperem el path de l'element
        folderPath = os.path.join(base, folderName)
        
        # Verifiquem si es un directori
        if not os.path.isdir(folderPath):
            continue
        
        # Obtenim tots els fitxers .mp3 dins del directori
        filesMP3 = [f for f in os.listdir(folderPath) if f.lower().endswith(".mp3")]
        # Enviem un comentari si la llista està buida
        if not filesMP3:
            print(f"No s'ha torbat cap fitxer .mp3 {folderName}")
            continue
        
        # Seleccionem el primer arxiu .mp3 (hauría d'haver només un)
        fileMP3 = os.path.join(folderPath, filesMP3[0])
                
 
        # Carreguem la cançó de la carpeta
        song = AudioSegment.from_file(fileMP3, format="mp3")
        duration = len(song)  # Obtenim la duració de la cançó en ms
    
        
        
        
        # Calculem quants fragments de 12 segons podem obtenir en milisegons
        duracioFragment = (12*1000) # 12 segons en milisegons
        nfragments = duration // duracioFragment
        
        # Generar los fragmentos
        for j in range(nfragments):
            tempsInicial = j * (12*1000)
            tempsFinal = tempsInicial + duracioFragment
            fragment = song[tempsInicial:tempsFinal]
            
            # Generem l'arxiu de nou fragment
            fragmentName = f"{os.path.splitext(filesMP3[0])[0]}_{j+1}.mp3"
            fragmentPath = os.path.join(folderPath, fragmentName)
            
            # Exportem el fragment generat
            fragment.export(fragmentPath, format="mp3")
            print(f"Fragment guardat: {fragmentPath}")
         

# Utilitzem el directori actual com a base
directory = os.getcwd()
splitSongsMP3(directory)
