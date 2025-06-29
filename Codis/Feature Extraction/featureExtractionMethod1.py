# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 17:31:56 2025

@author: marcp

Aquest codi es necessari per crear el primer subespai de característiques,
s'extreuen característiques amb la llibreria librosa.

"""

# Importem les llibreries necessaries
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

# Funció per extreure característiques dels arxius MIDI
def extract_midi_features(midi_path):
    
    # Carguem l'arxiu MIDI
    directory = os.getcwd()
    midi_path_ = os.path.join(directory,midi_path)
    midi_data = pretty_midi.PrettyMIDI(midi_path_)
    
    # Extraiem les notes de l'arxiu
    note_pitches = [note.pitch for instrument in midi_data.instruments for note in instrument.notes]
    
    # Si no hi ha notes detectades retornem None    
    if len(note_pitches) <= 2:
        return None
    
    # Extraiem les característiques 
    tempo = midi_data.estimate_tempo()
    pitch_class_histogram = midi_data.get_pitch_class_histogram()
    chroma = midi_data.get_chroma().mean(axis=1)  
    beats = midi_data.get_beats()
    
    # Retornem en forma de vector
    return {
        'tempo': tempo,
        'note_pitches_mean': np.mean(note_pitches),
        'pitch_class_histogram': pitch_class_histogram.mean(),
        'chroma': chroma.mean(),
        'num_beats': len(beats)
    }

# Mètode 1 d'extracció de característiques
def extract_audio_features(audio_path):
    
    # Carreguem l'arxiu d'audio
    directory = os.getcwd()
    audio_path_ = os.path.join(directory,audio_path)
    y, sr = librosa.load(audio_path_, sr=None) # Extraiem els valors del senyal (y) i la frequencia de mostreig (sr)
    
    # Extraiem les caracterísitiques 
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
    rms = librosa.feature.rms(y=y)  
    zcr = librosa.feature.zero_crossing_rate(y)
    tempo = librosa.feature.tempo(y=y)[0]
    
    return {
       
        'spectral_centroid': spectral_centroid,
        'spectral_bandwidth': spectral_bandwidth,
        'rms': rms.mean(),
        'zcr': zcr.mean(),
        'tempo': tempo
        
    }

# Funció per passar a arrays les característiques 
def combine_features(audio_features):

    #midi_vector = np.array(list(midi_features.values()))
    audio_list = list(audio_features.values())
    audio_vector = np.array(audio_list)

    return audio_vector

    

directory = os.getcwd()

songs = {}


# Recorrem les carpetes de les cançons que volem
for i in range(1,201):
    folder_name = f'song_{i}'
    folder_path = os.path.join(directory, folder_name)
    # Evitem agafar la cançó completa 
    for file in os.listdir(folder_path):
        if file.endswith(".mp3") and file[:-4] != folder_name:
            audio_path = os.path.join(folder_path,file)
            midi_path = os.path.join(folder_path, file.replace(".mp3","_basic_pitch.mid"))
            # Guardem el path de l'audio i el arxiu midi corresponent
            songs[file] = [audio_path, midi_path]
    
# Cridem les funcions necessaries
feature_vectors = []
midi_features = []
id_vector = []
chroma = []
audio_features = []
features = {}
# Recorrem totes les cançons de la llista 
for song, paths in songs.items():
    midi_features = extract_midi_features(paths[1])
    if midi_features == None:
        continue
    audio_features = extract_audio_features(paths[0])
    combined_vector = combine_features(audio_features)
    feature_vectors.append(combined_vector)
    id_vector.append(song)
    print(song,"\n")
    features[song] = combined_vector

# Guardem l'extracció de característiques en un fitxer pkl
with open("featureExtraction1.pkl", "wb") as f:
    pickle.dump(features, f)

