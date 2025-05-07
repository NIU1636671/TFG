# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 17:31:56 2025

@author: marcp
"""



import openl3
import soundfile as sf
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os





directory = os.getcwd()
embList = list()
tsList = list()
idList = list()

for i in range(1,25):
    folder_name = f'song_{i}'
    folder_path = os.path.join(directory, folder_name)
    
    for file in os.listdir(folder_path):
        if file.endswith(".mp3") and file[:-4] != folder_name:
            audio_path = os.path.join(folder_path,file)
            audio_path_ = os.path.join(directory,audio_path)
            
            audio, sr = sf.read(audio_path_)
            if np.all(audio == 0):
                continue
            
            emb, ts = openl3.get_audio_embedding(audio, sr,embedding_size=512)
             
            embList.append(emb.mean(axis=0))
            tsList.append(ts)
            idList.append(file)
    
 
# Normalize feature vectors
feature_matrix = np.array(embList)
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
        for i,j in zip(idList,clusters):
            print("Song: ",i,"Cluster: ",j,"\n")
        
        np.save(f'test4Clusters_{epsilon}_{sample}', clusters)
        