# -*- coding: utf-8 -*-
"""
p1_main.py : ** REQUIRED ** El vostre codi de la classe MusicData.
"""
# -*- coding: utf-8 -*-
"""
p1_main.py : ** REQUIRED ** El vostre codi de la classe MusicData.
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 10:52:04 2023

@author: juani
"""
from ElementData import ElementData
from os import walk
import os
import cfg
import copy
import sys
import uuid
import eyed3
import numpy
import vlc
import time
import math
from collections import defaultdict
from GrafHash import GrafHash
        
class MusicData():
    
    '--> Metadades de cada arxiu'
    __slots__ = ['_dicc_data','_graf']
    
    def __init__(self):
        self._dicc_data = {} #diccionari on guardarem  la informació
        self._graf = GrafHash([],[],[],True)
        
    @property
    def get_dades(self): #getter del diccionari
        return self._dicc_data
        
    def add_song(self, uuid: str, file: str):
        
        try:
            
            if uuid not in self._dicc_data and os.path.exists(os.path.join(cfg.get_root(), file)): # si el uuid no es trobava ja al diccionari i el fitxer existeix

                self._dicc_data[uuid] = ElementData(filename = os.path.join(cfg.get_root(), file))#[None,None,None,None,None, os.path.join(cfg.get_root(), file) ] #afegim al diccionari com a clau el uuid i com a valor una llista amb l'última posició el fitxer i les altres osicions pendents d'emplenar
                self._graf.insert_vertex(uuid, self._dicc_data[uuid])
        except:
            return None
        

    def remove_song(self, uuid: str): #eliminem la canço passada com a parametre donat el seu identificador
        
        if uuid in self._dicc_data.keys():
            
            del self._dicc_data[uuid]

        self._dicc_data = {clau: valor for clau, valor in self._dicc_data.items() if clau != ''} # eliminem també del diccionari aquells elmenets que tinguin com ac lau un string buit
        
        
    def load_metadata(self, uuid: str):  # ommplim la informació restant del diccionari 
        if uuid not in self._dicc_data: # si el uuid no es troba es produeix un error
            raise OSError("L'uuid no és al diccionari")
            
        else: 
            #carreguem les dades
            metadata = eyed3.load(self._dicc_data[uuid].get_filename()) #metadata de la cançó
            try:
                genre = metadata.tag.genre.name
            except:
                genre = "None" 
            file = self._dicc_data[uuid].get_filename()
            element = ElementData(metadata.tag.title, metadata.tag.artist, metadata.tag.album, genre, int(numpy.ceil(metadata.info.time_secs)), file)
            self._dicc_data[uuid] = element
            # self._dicc_data[uuid][0] = 
            # self._dicc_data[uuid][1] =  metadata.tag.title
            # self._dicc_data[uuid][2] =  
            # self._dicc_data[uuid][3] =  
            # # si el gènere no existeix el guardem com a "None"

                
            # self._dicc_data[uuid][4] = genre
            
    def get_title(self, uuid: str): # obtenim el titol d'una canço donat un uuid. Si no hi és, es produeix un error
        if uuid not in self._dicc_data.keys():
            return None
            #raise TypeError("Títol de què exactament? No conseguiras el títol de programació així")
        # if len(self._dicc_data[uuid]) == 6:
            # print("🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩",self._dicc_data[uuid])
            #print("titulasoo🤩🤩:", self._dicc_data[uuid][1])
        return self._dicc_data[uuid].get_title
        
        # else:
        #     return None
                
        
    def get_artist(self, uuid: str): # obtenim l'artista d'una canço donat un uuid. Si no hi és, es produeix un error
        if uuid not in self._dicc_data:
            return None
            #raise TypeError("Artista tu, que el teu codi no-funcional és art")
        
        #print("artistaso🤩:", self._dicc_data[uuid][2])
        # if len(self._dicc_data[uuid]) == 6:

        return self._dicc_data[uuid].get_artist
        
        # else:
        #     return None

    def get_album(self, uuid: str): # obtenim l'album d'una canço donat un uuid. Si no hi és, es produeix un error
        if uuid not in self._dicc_data:
            return None
            #raise TypeError("Printejo un àlbum de tots els teus èxits: []")
        
        #print("albumaso🤩:", self._dicc_data[uuid][3])
        # if len(self._dicc_data[uuid]) == 6:

        return self._dicc_data[uuid].get_album
        
        # else:
        #     return None
        
    #@property     
    def get_duration(self, uuid: str): # obtenim la duració d'una canço donat un uuid. Si no hi és, es produeix un error
        if uuid not in self._dicc_data:
            return -1
            #raise TypeError("Printejo la duració de tots els teus èxits: 0")
        
        #print("duració🤩:", self._dicc_data[uuid][0])
        # if len(self._dicc_data[uuid]) == 6:

        return self._dicc_data[uuid].get_duration
        
        # else:
        #     return None

    def get_genre(self, uuid: str): # obtenim el gènere d'una canço donat un uuid. Si no hi és, es produeix un error
        if uuid not in self._dicc_data:
            return None
            #raise TypeError("El gènere d'aquest temacle inexistent és: 🦕")
        
        #print("gèèèè``eenenrenree🤩:", self._dicc_data[uuid][4])
        # if len(self._dicc_data[uuid]) == 6:

        return self._dicc_data[uuid].get_genre
        
        # else:
        #     return None
    
    #@property
    def get_filename(self, uuid): # obtenim el nom del fitxer d'una canço donat un uuid. Si no hi és, es produeix un error
        if uuid not in self._dicc_data:
            return None
            #raise TypeError("El gènere d'aquest temacle inexistent és: 🦕")
        
        #print("filenameee🤩:", self._dicc_data[uuid][-1])
        # if len(self._dicc_data[uuid]) == 6:
        #print(self._dicc_data[uuid])
        return self._dicc_data[uuid].get_filename()
        
        # else:
        #     return None
    
    def read_playlist(self, obj_llista):
        
        obj_llista = list(obj_llista)
        
        for i in range(len(obj_llista)-1): #-1 per evitar que la consola faci muèèè muèèè per index OoR

            self._graf.insert_edge(obj_llista[i], obj_llista[i+1])
    

    def get_song_rank(self, uuid: str): #sumem graus d'entrada i sortida
        if uuid in self._graf:
            return self._graf.grauIn(uuid) + self._graf.grauOut(uuid)
        else:
            return 0

    def get_next_songs(self, uuid): #aqui hauriem de fer una certa cerca per trobar totes les cançons que les precedeixen

        for node in self._graf._out[uuid]:
            yield (node, self._graf._out[uuid][node])


    def get_previous_songs(self, uuid): #aqui també però del reves
        for node in self._graf._in[uuid]:
            yield (node, self._graf._in[uuid][node])


    def get_song_distance(self, node1, node2):
        
        value = 0
        
        if node1 == node2 or self._graf.camiMesCurt(node1,node2) == []:
            return (0,0)

        #nodes mirats
        nodes_visitats = self._graf.camiMesCurt(node1,node2)
        out = self._graf.getOut() #ens guardem el diccionari que conté els pesos de les arestes
        for node in range(len(nodes_visitats)-1): #fem la suma de tots els pesos
            
            nodeAct = nodes_visitats[node]
            node = nodes_visitats[node+1]
            value += out[nodeAct][node] #li sumem el valor del dict
        
        return (len(nodes_visitats) -1, value)
    
    def __iter__(self):
        return iter(self._dicc_data)
        
    def __len__(self):
        return len(self._dicc_data)
        
    def __str__(self):
        return self._dicc_data.__str__()
    
    def __repr__(self):
        return f'Informació(\'{self._dicc_data}\')'