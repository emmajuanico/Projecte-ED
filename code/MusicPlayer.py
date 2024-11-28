# -*- coding: utf-8 -*-
"""
p1_main.py : ** REQUIRED ** El vostre codi de la classe MusicPlayer.
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 10:52:55 2023

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

class MusicPlayer():
    
    __slots__ = '_possibilitats'
    
    def __init__(self, musicdata):
        
        #ens passen una classe musicdata com a paràmetre i la guardem. Si es buida la inicialitzem a None
        if musicdata == None:
            self._possibilitats = {}
        else:
            self._possibilitats = musicdata
        
    def print_song(self, uuid: str): #imprimim la informació bàsica de la cançó utilitzant els getters de la classe musicdata
        
        try:
            print("Reproduïnt {}".format(uri_file))
            print(" Duració: {} segons".format(self._possibilitats.get_duration(uuid)))
            print(" Títol: {}".format(self._possibilitats.get_title(uuid))) 
            print(" Artista: {}".format(self._possibilitats.get_artist(uuid))) 
            print(" Àlbum: {}".format(self._possibilitats.get_album(uuid))) 
            print(" Gènere: {}".format(self._possibilitats.get_genre(uuid))) 
            print(" UUID: {}".format(uuid))
            print(" Arxiu: {}".format(self._possibilitats.get_filename(uuid))) 
        
        except:
            return None
            
    def play_file(self, file): #es reprodueix la cançó i si no la troba es produeix un error
        try: 
            for element in self._possibilitats.get_dades.values():
                if element.get_filename() == file:
                    player = vlc.MediaPlayer(element.get_filename()[-1]) 
                    player.play()
                    timeout = time.time() + element.get_duration()[0] 
                    while True: 
                     if time.time() < timeout: 
                         try: 
                             time.sleep(1) 
                         except KeyboardInterrupt:
                             break 
                     else: 
                         break 
                     
                    player.stop() 

                    print("\nFinal!")
        except:
            raise KeyError("No s'ha trobat el fitxer desitjat")
    
    def play_song(self, uuid:str, mode: int): #funció per triar si volem reproduir la cançó, veure la informació bàsica o ambdues coses 
        try: 
            if mode == 0:
                self.print_song(uuid)
            elif mode == 1:
                self.print_song(uuid)
                self.play_file(self._possibilitats.get_filename(uuid))
            elif mode == 2:
                self.play_file(self._possibilitats.get_filename(uuid))
        except:
            raise ValueError ('Introdueix un mode permès')
            
    def __str__(self):
        return self._possibilitats.__str__()
    
    def __repr__(self):
        return f'Directoris(\'{self._possibilitats}\')'