# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 17:31:56 2025

@author: marcp

Aquest codi es necessari per crear el segon subespai de característiques,
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



# Funció per validar si l'audio existeix o es un fragment buit
def extract_midi_features(midi_path):
    
    # Extraiem les carcterístiques MIDI
    directory = os.getcwd()
    midi_path_ = os.path.join(directory,midi_path)
    midi_data = pretty_midi.PrettyMIDI(midi_path_)
    
    # En el cas de que no hi hagi notes musicals, es retorna None, i passem de fragment
    note_pitches = [note.pitch for instrument in midi_data.instruments for note in instrument.notes]
    if len(note_pitches) <= 2:
        return None
    
    else:
        return True
    

# Funció per extreure característiques d'audio
def extract_audio_features(audio_path):
    
    # Carreguem el senyal d'audio
    directory = os.getcwd()
    audio_path = os.path.join(directory,audio_path)
    y, sr = librosa.load(audio_path, sr=None)
    
    # Exraiem els MFCCS
    mfccs = librosa.feature.mfcc(y=y, sr=sr)
    
    # Retornem el vector fent la mitjana pels temps.
    return np.mean(mfccs,axis=1)
       
        
  
# Funció per convertir el vector en array
def convert2Vec(mfccs):
  
    audio_vector = np.array(list(mfccs))
   
    return audio_vector

    

directory = os.getcwd()

songs = {}

# Recorrem les cançons de la BD
for i in range(1,201):
    folder_name = f'song_{i}'
    folder_path = os.path.join(directory, folder_name)
    # Recorrem els arxius de les carpetes
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
    mfccs = extract_audio_features(paths[0])
    featureVec = convert2Vec(mfccs)
    feature_vectors.append(featureVec)
    id_vector.append(song)
    features[song] = featureVec
    

# Guardem l'extracció de característiques
with open("featureExtraction2.pkl", "wb") as f:
    pickle.dump(features, f)

