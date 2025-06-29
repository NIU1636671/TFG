"""
Created on Sat Mar 22 11:40:53 2025

@author: marcp

Aquest codi serveix per obtenir una taula descriptiva de les cançons de la BD, 
obtenim informació sobre el rang i la mitjana d'atributs com la duració o el 
nombre de fragments, també sabem el nombre d'artistes i gèneres que hi ha. Per
altra banda, es guarden dos dataframes on obtenim informació de el nombre de 
cançons de la BD que hi ha per gènere i per artista.
"""

# Importem la llibreria necessaria
import pandas as pd

# Carreguem l'arxiu de metadades de la BD
df = pd.read_csv("TFG_BD_1.csv", sep=";", encoding="latin1")

# Obtenim tots els gèneres de la BD
allGenres = df['genres'].str.split(',').explode().str.strip() # amb .explode() separem cada element de la llista en una fila
# Eliminem duplicats
uniqueGenres = allGenres.unique() 
# Recompte de generes
numGenres = len(uniqueGenres) 

# Obtenim tots els autors de la BD 
allAuthors = df['author'].str.split(',').explode().str.strip() # fem el mateix que amb els gèneres
# Eliminem els duplicats
uniqueAuthors = allAuthors.unique()
# Fem recompte d'autors
numAuthors = len(uniqueAuthors)

# Funcions per a la duració de les cançons
def mmss2seg(mmss):
    '''
    Parameters
    ----------
    mmss : string
        Duració de la cançó en forma mm:ss.

    Returns
    -------
    int
        Duració de la cançó en segons.

    '''
    
    minuts, segons = map(int, mmss.split(':'))
    return minuts * 60 + segons

def seg2mmss(seg):
    '''
    Parameters
    ----------
    seg : int
        Duració de la cançó en segons.

    Returns
    -------
    str
        Duració de la cançó en format mm:ss
    '''
    return f"{int(seg // 60)}:{str(int(seg % 60)).zfill(2)}"

# Obtenim les duracions de les cançons en segons
duracioSegons = df['duration'].dropna().apply(mmss2seg)
# Obtenim la duració mínima de tota la BD en format mm:ss
duracioMin = seg2mmss(duracioSegons.min())
# Obtenim la duració màxima de tota la BD en format mm:ss
duracioMax = seg2mmss(duracioSegons.max())
# Obtenim la duració mitjana de tota la BD en format mm:ss
duracioMean = seg2mmss(round(duracioSegons.mean(),2))

# Obtenim el nombre mínim de fragments de la BD
minFragments = df['num_fragments'].min()
# Obtenim el nombre màxim de fragments de la BD
maxFragments = df['num_fragments'].max()
# Obtenim el nombre mitjà de fragments de la BD
meanFragments = df['num_fragments'].mean()

# Reemplaçem la llista de gèneres del dataframe per cada gènere separat en una fila
genresDF = (df.assign(genres=df['genres'].str.split(',')).explode('genres').dropna(subset=['genres']))

# Eliminem espais innecessaris dels strings amb .strip()
genresDF['genres'] = genresDF['genres'].str.strip()
 
# Comptem quants cops surten els gèneres al dataframe
songsXgenre = genresDF['genres'].value_counts()

# Separem la llista d'artistes replicant les files per cada element de la llista
artistsDF = (
    df.assign(author=df['author'].str.split(','))
      .explode('author')
      .dropna(subset=['author'])
)

# Eliminem espais innecessaris dels strings amb .strip()
artistsDF['author'] = artistsDF['author'].str.strip()

# Comptem quants cops surt l'artista en el dataframe
songsXartist = artistsDF['author'].value_counts()

# Guardem tota la informació en un dataframe
statsDF = pd.DataFrame({
    "Stat": ["Gèneres únics", "Autors únics", "Duració mínima", "Duració màxima", "Duració mitjana",
                "Nombre de fragments mínim", "Nombre de fragments màxim", "Nombre mitjà de fragments"],
    "Valor": [numGenres, numAuthors, duracioMin, duracioMax, duracioMean,
              minFragments, maxFragments, round(meanFragments, 2)]
})

# Formem un dataframe amb el gènere i el nombre de cançons corresponent
songsXgenreDF = songsXgenre.reset_index() # necessari despres d'explode()
songsXgenreDF.columns = ['Gènere', 'Nombre de cançons']

# Formem un dataframe amb els artistes i el nombre de cançons corresponent
songsXartistDF = songsXartist.reset_index() # necessari despres d'explode()
songsXartistDF.columns = ['Artista', 'Nombre de cançons']

# Guardem els dataframes resultants
pd.DataFrame.to_csv(songsXgenreDF, "songsXgenre.csv")
pd.DataFrame.to_csv(songsXartistDF, "songsXautor.csv")
pd.DataFrame.to_csv(statsDF, "taulaDescriptiva.csv")

# Mostrem els resultats 
print(statsDF)
print(songsXgenreDF)
print(songsXartistDF)