# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 17:31:56 2025

@author: marcp

Aquest codi es necessari per poder extreure les característiques del senyal
d'audio, utilitzarem totes les característiques contemplades en el treball, es
fara servir la llibreria librosa per computar les extraccions.
"""

# Llibreries necessaries
import pretty_midi
import librosa
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import json
import pickle


# Funció per extreure les característiques MIDI per veure si es tracta d'un fragment buit
def extract_midi_features(midiPath):
    
    # Carregem l'arxiu MIDI 
    directory = os.getcwd()
    midiPath = os.path.join(directory,midiPath)
    midiData= pretty_midi.PrettyMIDI(midiPath)
    
    # Extraiem les notes de l'arxiu
    notePitches = [note.pitch for instrument in midiData.instruments for note in instrument.notes]
    
    # Si no hi ha notes detectades retornem None    
    if len(notePitches) <= 2:
        return None
    
    # Extraiem les característiques 
    tempo = midiData.estimate_tempo()
    pitch_class_histogram = midiData.get_pitch_class_histogram()
    chroma = midiData.get_chroma().mean(axis=1)  
    beats = midiData.get_beats()
    
    # Retornem en forma de vector
    return {
        'tempo': tempo,
        'note_pitches_mean': np.mean(notePitches),
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
    # Extraiem les característiques del subespai 2
    mfccs = librosa.feature.mfcc(y=y, sr=sr)  
    # Extraiem les característiques del subespai 3
    chroma = librosa.feature.chroma_stft(y=y, sr=sr) 
    
    return {
       
        'spectral_centroid': spectral_centroid,
        'spectral_bandwidth': spectral_bandwidth,
        'rms': rms.mean(),
        'zcr': zcr.mean(),
        'tempo': tempo
        
    },np.mean(mfccs,axis=1),np.mean(chroma, axis=1)

# Funció per combinar els dos vectors de característiques 
def combine_features(audio_features, mfccs, chroma):

    # Convertim cada vector de característiques en un array
    featuresVector1 = np.array(list(audio_features.values()))
    featuresVector2 = np.array(list(mfccs))
    featuresVector3 = np.array(list(chroma))
       
    
    # Convinem els tres vectors en un sol
    combinedVec = np.concatenate((featuresVector1, featuresVector2, featuresVector3))
    

    return combinedVec

    

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
    featureVec1, featureVec2, featureVec3 = extract_audio_features(paths[0])
    combined_vector = combine_features(featureVec1, featureVec2, featureVec3)
    feature_vectors.append(combined_vector)
    id_vector.append(song)
    print(song,"\n")
    features[song] = combined_vector
    
# Guardar en archivo
with open("Allfeatures.pkl", "wb") as f:
    pickle.dump(features, f)


