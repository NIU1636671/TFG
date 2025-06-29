
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 17:31:56 2025

@author: marcp
Aquest codi es necessari per crear el tercer subespai de característiques,
s'extreuen característiques amb la llibreria librosa.

"""
import pickle
import pretty_midi
import librosa
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import json



    
def extract_midi_features(midi_path):
    # Extraiem característiques dels arxius midi
    directory = os.getcwd()
    midi_path = os.path.join(directory,midi_path)
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    note_pitches = [note.pitch for instrument in midi_data.instruments for note in instrument.notes]
    # Comprovem si es tracta d'un gragment buit o no.
    if len(note_pitches) <= 2:
        return None
    
    else:
        return True
    

# Funció per extreure característiques d'audio 
def extract_audio_features(audio_path):
    
    directory = os.getcwd()
    audio_path_ = os.path.join(directory,audio_path)
    y, sr = librosa.load(audio_path_, sr=None)
    
    # Extraiem el cromatograma d'audio.
    chroma = librosa.feature.chroma_stft(y=y, sr=sr) 
 
    # Retornem en forma de vector fent la mitjana pels temps
    return np.mean(chroma,axis=1)
       
        
  
# Funció per convertir el vector a array
def convert2Vec(chroma):
  
    audio_vector = np.array(list(chroma))
        
    return audio_vector

    

directory = os.getcwd()

songs = {}

# Recorrem les cançons
for i in range(1,201):
    folder_name = f'song_{i}'
    folder_path = os.path.join(directory, folder_name)
    # Recorrem les carpetes de les cançons
    for file in os.listdir(folder_path):
        if file.endswith(".mp3") and file[:-4] != folder_name:
            audio_path = os.path.join(folder_path,file)
            midi_path = os.path.join(folder_path, file.replace(".mp3","_basic_pitch.mid"))
            songs[file] = [audio_path, midi_path]
    


id_vector = list()
feature_vectors = list()
features = {}
for song, paths in songs.items():
    midi_features = extract_midi_features(paths[1])
    if midi_features == None:
        continue
    chroma = extract_audio_features(paths[0])
    featureVec = convert2Vec(chroma)
    feature_vectors.append(featureVec)
    id_vector.append(song)
    print(song,"\n")
    features[song] = featureVec

# Guardar en archivo
with open("featureExtraction3.pkl", "wb") as f:
    pickle.dump(features, f)



