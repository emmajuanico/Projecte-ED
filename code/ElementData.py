# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 17:17:18 2023

@author: juani
"""

class ElementData:
    
    __slots__ = ['title', 'artist', 'album', 'genre', 'duration', 'filename']
    
    def __init__(self, title="", artist="", album="",genre="", duration=0, filename=""):
        self.title = title
        self.artist = artist
        self.album = album 
        self.genre = genre
        self.duration = duration
        self.filename = filename
        # if (title or artist or filename) == "":
        #     raise ValueError("No pot haver-hi elements clau buits")
        
    @property
    def get_title(self):
        return self.title
    
    @property
    def get_artist(self):
        return self.artist
    
    @property
    def get_album(self):
        return self.album
    
    @property
    def get_genre(self):
        return self.genre
    
    @property
    def get_duration(self):
        return self.duration
    
    #@property
    def get_filename(self):
        return self.filename
    
    def __hash__(self): # fem el has amb el filename per comparar
        return hash(self.filename)
     
    def __eq__(self, element):
        return hash(self) == hash(element)
        
    def __ne__(self, element):
        return hash(self) != hash(element)
            
    def __lt__(self, element):
        return hash(self) > hash(element)