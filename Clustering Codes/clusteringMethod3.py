
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 17:31:56 2025

@author: marcp
"""

import pretty_midi
import librosa
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os


# Function to validate if audio exists

    
def extract_midi_features(midi_path):
    
    directory = os.getcwd()
    midi_path_ = os.path.join(directory,midi_path)
    midi_data = pretty_midi.PrettyMIDI(midi_path_)
    # Extract features
    note_pitches = [note.pitch for instrument in midi_data.instruments for note in instrument.notes]
    if len(note_pitches) <= 2:
        return None
    
    else:
        return True
    

# Function to extract audio features
def extract_audio_features(audio_path):
    
    directory = os.getcwd()
    audio_path_ = os.path.join(directory,audio_path)
    y, sr = librosa.load(audio_path_, sr=None)
    
    # Extract features
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)  # Mean MFCCs
    
    # Return as a feature vector
    return np.mean(chroma,axis=1)
       
        
  
# Function to combine MIDI and audio features
def convert2Vec(chroma):
  
    audio_vector = np.array(list(chroma))
    
    # Combine into a single feature vector
    #combined_vector = np.concatenate((midi_vector, audio_vector))
    
    #return combined_vector
    return audio_vector

    

directory = os.getcwd()

songs = {}


for i in range(1,201):
    folder_name = f'song_{i}'
    folder_path = os.path.join(directory, folder_name)
    
    for file in os.listdir(folder_path):
        if file.endswith(".mp3") and file[:-4] != folder_name:
            audio_path = os.path.join(folder_path,file)
            midi_path = os.path.join(folder_path, file.replace(".mp3","_basic_pitch.mid"))
            songs[file] = [audio_path, midi_path]
    
# Extract and combine features for all songs

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
    

# Normalize feature vectors
feature_matrix = np.array(feature_vectors)
scaler = StandardScaler()
feature_matrix_normalized = scaler.fit_transform(feature_matrix)

minSamples = [2,4,6,8]
epsilons = [1.0,1.1,1.2,1.3,1.4,1.5,2.0,2.5,3.0]
for sample in minSamples:
    for epsilon in epsilons:
        # Apply DBSCAN clustering
        dbscan = DBSCAN(eps=epsilon, min_samples=sample)  # Adjust eps and min_samples as needed
        clusters = dbscan.fit_predict(feature_matrix_normalized)
    
        # Visualize clusters using PCA
        pca = PCA(n_components=2)
        reduced_features = pca.fit_transform(feature_matrix)
        
        # Plot the clusters
        plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=clusters, cmap='viridis', marker='o')
        plt.title('Clustering of Songs using DBSCAN')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.colorbar(label='Cluster')
        plt.show()
        
        # Print cluster assignments
        for i,j in zip(id_vector,clusters):
            print("Song: ",i,"Cluster: ",j,"\n")
        
        np.save(f'test3Clusters_{epsilon}_{sample}', clusters)
        