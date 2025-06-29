# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 16:21:58 2025

@author: marcp

Aquest codi serveix per convertir els fragments de les cançons de la BD en
arxius MIDI, els arxius MIDI no tenen so, són arxius que contenen instruments,
notes musicals, i els components estructurals de les cançons, és a dir,
les instruccions per generar una cançó.
"""

# Importem les llibreries
import os
from basic_pitch.inference import predict_and_save, Model
from basic_pitch import ICASSP_2022_MODEL_PATH

# Obtenim el directori actual
directory = os.getcwd()

# Inicialitzem el model que ens servirà per convertir els fitxers
basic_pitch_model = Model(ICASSP_2022_MODEL_PATH)

# Recorrem les carpetes on hi ha els audios de cada cançó
for folder in os.listdir(directory):
    folderPath = os.path.join(directory,folder)
    if os.path.isdir(folderPath):     
        
        # Obtenim la ruta de la carpeta on hi ha els fitxers d'audio
        audio = os.listdir(folderPath)
                
        # Verifiquem si hi ha arxius MIDI a la carpeta, és a dir, ja els hem convertit
        midi = any(f.endswith('.mid') for f in audio)
        if midi:
            print(f"Fitxers MIDI exsistens: {folder} (.mp3 convertit a .mid)")
            continue
        
        # Obtenim la llista de fitxers d'audio .mp3 de la carpeta
        audioList = [os.path.join(folder,x) for x in audio if x.lower().endswith(".mp3")]
        # Convertim la llista de fitxers d'audio de la carpeta a MIDI i els guardem
        predict_and_save(audioList,folderPath,True,False,False,False,basic_pitch_model)
    

