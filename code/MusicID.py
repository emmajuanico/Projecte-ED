# -*- coding: utf-8 -*-
"""
p1_main.py : ** REQUIRED ** El vostre codi de la classe MusicID.
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 10:51:22 2023

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

class MusicID():
    
    __slots__ = '_dicc_uuid'
    
    def __init__(self):
        
        self._dicc_uuid = {} #diccionari on guardarem la informació
        
    @property
    def get_dicc_uuid(self):
        return self._dicc_uuid    
    
    def generate_uuid(self, file): #generem un uuid per un fitxer determinat
        
        uri_file = cfg.get_one_file()
        if not os.path.isfile(uri_file):
            print("ERROR: Arxiu MP3 inexistent!") 
            sys.exit(1) 

        name_file = cfg.get_canonical_pathfile(file)
        mp3_uuid = uuid.uuid5(uuid.NAMESPACE_URL, name_file)
        mp3_uuid = str(mp3_uuid)
        
        if mp3_uuid not in self._dicc_uuid.values():
            self._dicc_uuid[file] = mp3_uuid # guardem el path a la key, i en el value el uuid generat

            return mp3_uuid
    

    def get_uuid(self, file): #getter del uuid
        
        if file in self._dicc_uuid:
            return self._dicc_uuid[file]
        
        else:
            return None
            #raise TypeError("Bro de quin maleït fitxer estas intentant conseguir el UUID?")
            #sys.exit(1) 
        
    def remove_uuid(self, uuid): #esborrem el  uuid del diccionari 
        borrar = None
        for file, ident in self._dicc_uuid.items():
            if str(ident) == str(uuid):
                borrar = file
        if borrar!=None:
            del self._dicc_uuid[borrar]
                
    def __iter__(self):
        return iter(self._dicc_uuid)
        
    def __len__(self):
        return len(self._dicc_uuid)
    
    def __str__(self):
        return self._dicc_uuid.__str__()
    
    def __repr__(self):
        return f'Directoris(\'{self._dicc_uuid}\')'