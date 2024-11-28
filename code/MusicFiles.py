# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 10:49:09 2023

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

class MusicFiles():
    
    __slots__ = ('_llista_paths', '_llista_added', '_llista_removed', '_antiga')
    
    def __init__(self):
        self._llista_paths = [] #llista de direccions dels fitxers actuals
        self._llista_added = [] #llista de direccions dels fitxers que s'han afegit
        self._llista_removed = [] #llista de direccions dels fitxers que s'han eliminat
        self._antiga = [] #llista de direccions dels fitxers antics
    
    
    def reload_fs(self, path):
        
        self._antiga = copy.deepcopy(self._llista_paths) #fem deepcopy per poder comparar si hem afegit o tret quelcom
        self._llista_paths = [] #la buidem per a tornarla a omplir
        
        
        caminadeta=walk(path)  #fem servir la funció walk per extreure tots els directoris i fitxers de ROOT_DIR

        for (dirpath, dirnames, nomsfitxer) in caminadeta:
            for fitxer in nomsfitxer:
                ruta=str(dirpath)+ str("/")  + str(fitxer) #creem la ruta amb tots els directoris per arribar a aquella cançó
                
                if fitxer.endswith(".mp3"): # si el fitxer és del tipus mp3, afegim la ruta a la llista
                    self._llista_paths.append(ruta)
        
    def files_added(self): 
        
        afegits = list(set(self._llista_paths) - set(self._antiga)) 
        
        # for canvi in afegits:
        #     print("\nS'ha afegit:",canvi)
        
        return afegits

    def files_removed(self):
        
        esborrats = list(set(self._antiga) - set(self._llista_paths))
        
        # for canvi in esborrats:
        #     print("\nS'ha esborrat:",canvi)
        
        return esborrats
            
    def __len__(self):
        return len(self._llista_paths)
        
    def __str__(self):
        return self._llista_paths.__str__()
    
    def __repr__(self):
        return f'Directoris(\'{self._llista_paths}\', \'{self._llista_added}\', \'{self._llista_removed}\')'
        