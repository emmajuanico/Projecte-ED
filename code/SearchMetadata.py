# -*- coding: utf-8 -*-
"""
p1_main.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 10:55:05 2023

@author: juani
"""

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
import MusicData
import MusicPlayer

        
class SearchMetadata():
    
    """sempre estamos retornando as listinhas com os UUIDs pertinêntes que complen as condições"""
    
    __slots__ = ('_metadata', '_llista', '_graf')
    
    def __init__(self, musicdata):
        if musicdata == None:
            self._metadata = {}
        else: 
            self._metadata = musicdata #classe musicdata
        self._graf = musicdata._graf
        self._llista = [] #llista on afegirem els uuid de les caçons amb la condició demanada
    
    def title(self, sub):
        
        sub = str(sub).lower() # convertim a minuscules el parametre passat per poder comparar totes les possibilitats
        self._llista = [] #biudem la llista de possibles iteracions anteriors
        
        for key, values in self._metadata.get_dades.items():
            
            titol = str(self._metadata.get_title(key)).lower() #titol de cada canço en minuscules
            
            if sub in titol:
                self._llista.append(key) # si el string passat coma parametre es troba dins el titol l'afegim dins la llista
                
        return self._llista
        
    #mateixa metodologia que title() pero amb els artistes
    def artist(self, sub):
        
        sub = str(sub).lower()
        self._llista = []
        
        for key, values in self._metadata.get_dades.items():
            artista = str(self._metadata.get_artist(key)).lower()
            if sub in artista:
                self._llista.append(key)
                
        return self._llista
        
     #mateixa metodologia que title() pero amb es albums       
    def album(self, sub):
        
        sub = str(sub).lower()
        self._llista = []
        
        for key, values in self._metadata.get_dades.items():
            album = str(self._metadata.get_album(key)).lower()
            
            if sub in album:
                self._llista.append(key)
                
        return self._llista
         
    #mateixa metodologia que title() pero amb els gèneres
    def genre(self, sub):
        
        sub = str(sub).lower()
        self._llista = []
            
        for key, values in self._metadata.get_dades.items():
            
            genre = str(self._metadata.get_genre(key)).lower()
            
            if sub in genre:
                self._llista.append(key)
                
        return self._llista
    
    #cançons que es  troben a les dues llistes
    def and_operator(self, l1, l2):
        #raise ValueError("No pot haver-hi elements clau buits")
        self._llista = []
        
        try:
            
            self._llista = [item for item in l1 if item in l2]
            #print("Elements en comú:", andd)
            return self._llista
            
        except: 
            return []
    
    #totes les cançons de les dues llistes sense epeticions
    def or_operator(self, l1, l2):
        
        self._llista = []
        
        try:
            l1l2 = l1 + l2
            self._llista = list(set(l1l2)) #agafem els que només estan en una llista
            #print("Elements trobats només en una llista:", orr)
            return self._llista
        except:
            return []
    
    def semblanca(self, uuid, node):
        AB_nodes, AB_value = self._metadata.get_song_distance(uuid,node)
        BA_nodes, BA_value  = self._metadata.get_song_distance(node, uuid)
        #print(AB_value, AB_nodes, BA_value, BA_nodes)
        AB = 0; BA = 0
        if (AB_nodes != 0):
            AB = (AB_value / AB_nodes) * (self._metadata.get_song_rank(uuid) / 2)
        if (BA_nodes != 0):
            BA = (BA_value / BA_nodes) * (self._metadata.get_song_rank(node) / 2)
        semblanca = AB + BA 
        return semblanca
    
    
    def get_similar(self, uuid, max_list):
        similar = {}
        for node in self._graf:
            if node != uuid:
                x = self.semblanca(uuid, node)

                similar[node] = x

        return list(dict(sorted(similar.items(), key=lambda item: item[1], reverse=True)))[:max_list]
    
    def get_topfive(self):
        dicc = {}
        for node in self._metadata._graf.nodes():
            rank = self._metadata.get_song_rank(node)
            dicc[node] = rank
            
        top_5_list = list(dict(sorted(dicc.items(), key=lambda item: item[1], reverse=True)))[:5]
        llista = []
        for i in top_5_list:
            llista.append(self.get_similar(i,5))
            
        llista_unica = list(set(element for sublist in llista for element in sublist)) #hauria de tenir tambe la incial?
        
        sol = []
        dist = {}
        for i in llista_unica:
            for j in llista_unica:
                if i != j:
                    dist[i] += self.semblanca(i,j)
        
        top_five = list(dict(sorted(dist.items(), key=lambda item: item[1], reverse=True)))[:5]
        return top_five
        
    def __str__(self):
        return self._llista.__str__()
    
    
    def __len__(self):
        return len(self._llista)
    
    def __repr__(self):
        return f'Cançons que compleixen la condició(\'{self._llista}\')'