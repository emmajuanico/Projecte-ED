# -*- coding: utf-8 -*-
"""
p1_main.py : ** REQUIRED ** El vostre codi de la classe PlayList.
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 10:53:59 2023

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

class PlayList():
    
    __slots__ = ('_metadata', '_playlist', '_files_uuid')
    
    def __init__(self, musicid, musicplayer):
        
        self._files_uuid = musicid #classe musicd
        self._metadata = musicplayer #classe musicplayer
        self._playlist=[] #guardem els uuids de la cançons
        
    """
        En aquesta classe assumim que se'ns passa un fitxer M3U el qual té un format:
        #EXTM3U
        #EXTINF: duració, artista - canço
        fitxer.mp3
    """
        
    def load_file(self, file):
        self._playlist = [] #buidem la playlis en cas de que hi hagues alguna cosa previament
        cont = 0
        if file.endswith('.m3u'): #si el fitxer es del tipus M3U l'obrim
            with open(file, 'r', encoding='latin1') as m3u:
                for linia in m3u: #per cada linia del fitxer
                    linia = linia.strip() 
                    cont+=1
                    if not linia.startswith('#'): #si la linia no comença per #
                        
                        if linia in self._files_uuid.get_dicc_uuid.keys(): # linia = nom del fitxer, si el nom del fitxer es troba al diccionari de music id 
                    
                            uuid = self._files_uuid.get_uuid(linia) # obtrnim l'uuid d'aquella cançó
                            
                            if uuid not in self._playlist:
                            #if len(self._playlist) > 0:
                               # if uuid != self._playlist[-1]: #si ha sigut lultima, no la posarem dos cops
                                   # self._playlist.append(uuid)
                           # else:
                                self._playlist.append(uuid)

        print(cont)                        
    def read_list(self, p_llista):
        self._playlist = p_llista

    def play(self, mode): #cridem el music player per a que executi la canço
        for uuid in self._playlist:
            self._metadata.play_song(uuid, mode)
            #m.play_song(uuid, mode)
            
    def add_song_at_end(self, uuid): #afegeix canço al final de la playlist

        self._playlist.append(uuid)

        
    def remove_first_song(self): #elimina la primera canço de la playlist
        if self._playlist != []:
            self._playlist.pop(0)

        
    def remove_last_song(self): #elimina l'última cançó de la playlist
        
        if self._playlist != []:
            self._playlist.pop(-1)

    def get_playlist(self):
        return self._playlist
    
    def __len__(self):
        return len(self._playlist)
        
    def __str__(self):
        return self._playlist.__str__()
        
    def __iter__(self):
        return iter(self._playlist)
        
    def __repr__(self):
        
        return f'uuids de la playlist(\'{self._playlist}\')'