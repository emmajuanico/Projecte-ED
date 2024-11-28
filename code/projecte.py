# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 10:50:31 2023

@author: juani & jansu
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

        
class MusicData():
    
    '--> Metadades de cada arxiu'
    
    def __init__(self):
        self._dicc_data = {}
        
    @property
    def get_dades(self):
        return self._dicc_data
        
    def add_song(self, uuid: str, file: str):

        try:
            
            if uuid not in self._dicc_data and os.path.exists(os.path.join(cfg.get_root(), file)):
                self._dicc_data[str(uuid)] = [None,None,None,None,None, os.path.join(cfg.get_root(), file) ] #es quedarà al final de la llista
        except:
            return None
        

    def remove_song(self, uuid: str):
        
        if uuid in self._dicc_data.keys():
            
            del self._dicc_data[uuid]

        self._dicc_data = {clau: valor for clau, valor in self._dicc_data.items() if clau != ''}
        
        
    def load_metadata(self, uuid: str):
        if uuid not in self._dicc_data:
            raise OSError("L'uuid no és al diccionari")
            
        else: 
            
            metadata = eyed3.load(self._dicc_data[uuid][-1]) #metadata de la cançó
            self._dicc_data[uuid][0] = int(numpy.ceil(metadata.info.time_secs))
            self._dicc_data[uuid][1] =  metadata.tag.title
            self._dicc_data[uuid][2] =  metadata.tag.artist
            self._dicc_data[uuid][3] =  metadata.tag.album
            try:
                genre = metadata.tag.genre.name 
            except:
                genre = "None" 
                
            self._dicc_data[uuid][4] = genre
            
    def get_title(self, uuid: str):
        # print("broooooooo", self._dicc_data, uuid)
        if uuid not in self._dicc_data.keys():
            return None
            #raise TypeError("Títol de què exactament? No conseguiras el títol de programació així")
        if len(self._dicc_data[uuid]) == 6:
            # print("🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩",self._dicc_data[uuid])
            print("titulasoo🤩🤩:", self._dicc_data[uuid][1])
            return self._dicc_data[uuid][1]
        
        else:
            return None
                
        
    def get_artist(self, uuid: str):
        if uuid not in self._dicc_data:
            return None
            #raise TypeError("Artista tu, que el teu codi no-funcional és art")
        
        print("artistaso🤩:", self._dicc_data[uuid][2])
        if len(self._dicc_data[uuid]) == 6:

            return self._dicc_data[uuid][2]
        
        else:
            return None

    def get_album(self, uuid: str):
        if uuid not in self._dicc_data:
            return None
            #raise TypeError("Printejo un àlbum de tots els teus èxits: []")
        
        print("albumaso🤩:", self._dicc_data[uuid][3])
        if len(self._dicc_data[uuid]) == 6:

            return self._dicc_data[uuid][3]
        
        else:
            return None
            
    def get_duration(self, uuid: str):
        if uuid not in self._dicc_data:
            return None
            #raise TypeError("Printejo la duració de tots els teus èxits: 0")
        
        print("duració🤩:", self._dicc_data[uuid][0])
        if len(self._dicc_data[uuid]) == 6:

            return self._dicc_data[uuid][0]
        
        else:
            return None

    def get_genre(self, uuid: str):
        if uuid not in self._dicc_data:
            return None
            #raise TypeError("El gènere d'aquest temacle inexistent és: 🦕")
        
        print("gèèèè``eenenrenree🤩:", self._dicc_data[uuid][4])
        if len(self._dicc_data[uuid]) == 6:

            return self._dicc_data[uuid][4]
        
        else:
            return None
    
    def get_filename(self, uuid):
        if uuid not in self._dicc_data:
            return None
            #raise TypeError("El gènere d'aquest temacle inexistent és: 🦕")
        
        print("filenameee🤩:", self._dicc_data[uuid][-1])
        if len(self._dicc_data[uuid]) == 6:

            return self._dicc_data[uuid][-1]
        
        else:
            return None
        
    def __len__(self):
        return len(self._dicc_data)
        
    def __str__(self):
        return self._dicc_data.__str__()



class MusicFiles():
    def __init__(self):
        self._llista_paths = []
        self._llista_added = []
        self._llista_removed = []
        self._antiga = []
    
    
    def reload_fs(self, path):
        
        self._antiga = copy.deepcopy(self._llista_paths) #fem deepcopy per poder comparar si hem afegit o tret quelcom
        self._llista_paths = [] #la buidem per a tornarla a omplir
        
        
        caminadeta=walk(path)  #fem servir la funció walk per extreure tots els directoris i fitxers de ROOT_DIR

        for (dirpath, dirnames, nomsfitxer) in caminadeta:
            for fitxer in nomsfitxer:
                ruta=str(dirpath)+ str("/")  + str(fitxer)
                
                if fitxer.endswith(".mp3"):
                    self._llista_paths.append(ruta)
        
    def files_added(self):
        
        afegits = list(set(self._llista_paths) - set(self._antiga))
        
        for canvi in afegits:
            print("\nS'ha afegit:",canvi)
        
        return afegits

    def files_removed(self):
        
        esborrats = list(set(self._antiga) - set(self._llista_paths))
        
        for canvi in esborrats:
            print("\nS'ha esborrat:",canvi)
        
        return esborrats
            
    def __len__(self):
        return len(self._llista_paths)
        
    def __str__(self):
        return self._llista_paths.__str__()
    
    

class MusicID():
    
    def __init__(self):
        
        self._dicc_uuid = {}
        
    @property
    def get_dicc_uuid(self):
        return self._dicc_uuid    
    
    def generate_uuid(self, file):
        
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
    

    def get_uuid(self, file):
        
        if file in self._dicc_uuid:
            return self._dicc_uuid[file]
        
        else:
            return None
            #raise TypeError("Bro de quin maleït fitxer estas intentant conseguir el UUID?")
            #sys.exit(1) 
        
    def remove_uuid(self, uuid):
        borrar = None
        for file, ident in self._dicc_uuid.items():
            if str(ident) == str(uuid):
                borrar = file
        if borrar!=None:
            del self._dicc_uuid[borrar]
                
        
        #if file in self._dicc_uuid:
            
        
        #else:
           # return None
            #raise TypeError("Bro quin maleït fitxer estas intentant esborrar?")
            #sys.exit(1) 
            
    
    
    def __len__(self):
        return len(self._dicc_uuid)
    
    def __str__(self):
        return self._dicc_uuid.__str__()
                
    
    

class MusicPlayer():
    
    def __init__(self, musicdata):
        
        if musicdata == None:
            self._possibilitats = {}
        else:
            self._possibilitats = musicdata
        
    def print_song(self, uuid: str):
        
        
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
            
    def play_file(self, file):
        try: 
            for llista in self._possibilitats.get_dades.values():
                if llista[-1] == file:
                    player = vlc.MediaPlayer(llista[-1]) 
                    player.play()
                    timeout = time.time() + llista[0] 
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
    
    def play_song(self, uuid:str, mode: int): 
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
    
    
    
class PlayList():
    def __init__(self, musicid, musicplayer):
        
        self._files_uuid = musicid
        self._metadata = musicplayer
        self._size = 0
        self._playlist=[] #guardem els uuids de la cançó
        
    """
        En aquesta classe assumim que se'ns passa un fitxer M3U el qual té un format:
        #EXTM3U
        #EXTINF: duració, artista - canço
        fitxer.mp3
    """
        
    def load_file(self, file):
        self._playlist = []
        
        if file.endswith('.m3u'):
            with open(file, 'r', encoding='latin1') as m3u:
                for linia in m3u:
                    linia = linia.strip()
                    if not linia.startswith('#'):
                        
                        if linia in self._files_uuid.get_dicc_uuid.keys():
                    
                            uuid = self._files_uuid.get_uuid(linia)
                            if uuid not in self._playlist:
                                self._size +=1
                                self._playlist.append(uuid)

    def play(self, mode): #cridem el music player per a que executi la canço
        for uuid in self._playlist:
            self._metadata.play_song(uuid, mode)
            #m.play_song(uuid, mode)
            
    def add_song_at_end(self, uuid):
            
        self._playlist.append(uuid)

        
    def remove_first_song(self):
        if self._playlist != []:
            self._playlist.pop(0)

        
    def remove_last_song(self):
        
        if self._playlist != []:
            self._playlist.pop(-1)

            
    def __len__(self):
        return len(self._playlist)
        
    def __str__(self):
        return self._playlist.__str__()
    
    
    
      
class SearchMetadata():
    
    """sempre estamos retornando as listinhas com os UUIDs pertinêntes que complen as condições"""
    
    def __init__(self, musicdata):
        self._metadata = musicdata
        self._llista = []
    
    def title(self, sub):
        
        sub = str(sub).lower()
        self._llista = []
        
        for key, values in self._metadata.get_dades.items():
            
            #titol = str(values[1]).lower()
            titol = str(self._metadata.get_title(key)).lower()
            
            if sub in titol:
                self._llista.append(key)
                
        return self._llista
        
            
    def artist(self, sub):
        
        sub = str(sub).lower()
        self._llista = []
        
        for key, values in self._metadata.get_dades.items():
            artista = str(self._metadata.get_artist(key)).lower()
            #artista = str(values[2]).lower()

            if sub in artista:
                self._llista.append(key)
                
        return self._llista
        
            
    def album(self, sub):
        
        sub = str(sub).lower()
        self._llista = []
        
        for key, values in self._metadata.get_dades.items():
            album = str(self._metadata.get_album(key)).lower()
            #album = str(values[3]).lower()
            
            if sub in album:
                self._llista.append(key)
                
        return self._llista
            
    def genre(self, sub):
        
        sub = str(sub).lower()
        self._llista = []
            
        for key, values in self._metadata.get_dades.items():
            
            genre = str(self._metadata.get_genre(key)).lower()
            #genre = str(values[4]).lower()
            
            if sub in genre:
                self._llista.append(key)
                
        return self._llista
            
    def and_operator(self, l1, l2):
        
        self._llista = []
        
        try:
            
            self._llista = [item for item in l1 if item in l2]
            print("Elements en comú:", self._llista)
            return self._llista
            
        except: 
            return []
        
    def or_operator(self, l1, l2):
        
        self._llista = []
        
        try:
            l1l2 = l1 + l2
            self._llista = list(set(l1l2)) #agafem els que només estan en una llista
            print("Elements trobats només en una llista:", self._llista)
            return self._llista
        except:
            return []
        
    
# Music=MusicFiles()
# Music.reload_fs(r"C:\Users\juani\OneDrive\Escriptori\uni\UAB\2on\Q1\Estructures de dades\projecte\ROOT_DIR")           
    
try: 
    num=int(input("\nMenú \n 0 - Sortir del programa \n 1 - Mirar si s'han afegit cançons \n 2 - Mirar si s'han esborrat cançons \n 3 - Obtenir la informació de totes les cançons  \n 4 - Esborrar canço de la base de dades \n 5 - Reproduir i veure informació d'una canço \n 6 - Veure i reproduir una Playlist \n 7 - Buscar cançons a la PlayList per títol \n \n Opció a triar: "))
except:
    raise ValueError ('Introdueix un número permès')
    
while 0<=num<=10:
    Music=MusicFiles()
    Music.reload_fs(r"C:\Users\juani\OneDrive\Escriptori\uni\UAB\2on\Q1\Estructures de dades\projecte\ROOT_DIR")
    data = MusicData()
    identificador = MusicID()
    
    for canço in Music._llista_paths:
        ident = identificador.generate_uuid(canço)
    # print(identificador._dicc_uuid)
    for file, uuidd in identificador._dicc_uuid.items():
        data.add_song(uuidd, file)
    for uid in data._dicc_data.keys():
        data.load_metadata(uid)
        
    if num==0:
        print('\n Sortint del programa...... \n')
        break 
    
    if num==1:
        Music.files_added(r"C:\Users\juani\OneDrive\Escriptori\uni\UAB\2on\Q1\Estructures de dades\projecte\ROOT_DIR")
    
    if num==2:
        Music.files_removed(r"C:\Users\juani\OneDrive\Escriptori\uni\UAB\2on\Q1\Estructures de dades\projecte\ROOT_DIR")
    
    if num==3: #generar uuid
        # print(data._dicc_data)
        for uid in data._dicc_data.keys():
        #     data.load_metadata(uid)
            data.get_title(uid)
            data.get_artist(uid)
            data.get_album(uid)
            data.get_genre(uid)
            print('\n                           \n')
            
    if num == 4:

        print('\n Quina canço vols eliminar? Aquestes son les que hi ha ara:')
        cont=0
        for metadates in data.get_dades.values():
            x = str(cont)  + ' --- Títol: ' + str(metadates[1]) + ' - Artista: ' + str(metadates[2])
            print(x)
            cont+=1
        eliminar = int(input('\n Index de la canço a eliminar: '))
        if eliminar <= len(data.get_dades):
            identificador = list(data.get_dades)[eliminar]
            data.remove_song(identificador)
            # print(" UUID: {}".format(mp3_uuid)) 
            # print(" Arxiu: {}".format(name_file)) 
            
    if num == 5:
        player = MusicPlayer(data)
        player.print_song('48363a0d-4432-5826-9d76-3f02bd197518')
        player.play_file('cançons\\Manel - Criticarem les noves modes de pentinats.mp3')
        
        # musicdata = MusicData(identificador.get_dicc_uuid)
        # print(musicdata.get_title(ident))
    
    if num == 6:
        playlist = PlayList(identificador, data)
        playlist.load_file('estructures de dades.m3u')
        mode = int(input(" Què vols fer amb la PLaylis? \n 0 - Veure la PLayList \n 1- Veure la PlayList i reproduir-la  \n 2- Reproduir la PLayList"))
        playlist.play(mode)
    
    if num == 7:
        search = SearchMetadata(data)
        inputaçao = input("Terme que vols cercar:")
        x = search.title(inputaçao)
        print(x)
        
    try:
        num=int(input("\nMenú \n 0 - Sortir del programa \n 1- Mirar si s'han afegit cançons \n 2- Mirar si s'han esborrat cançons \n 3- Obtenir la informació de totes les cançons  \n 4 - Esborrar canço de la base de dades \n 5 - Reproduir i veure informació d'una canço \n 6 - Veure i reproduir una Playlist \n 7 - Buscar cançons a la PlayList per títol \n \n Opció a triar: "))
    except:
        raise ValueError ('Introdueix un número permès')




# #cada cop que fas una operacio sha de fer un reload

    
# class PlayList()
#     def load_file(file:str):
#         pass
#     def play():
#         pass
#     def add_song_at_end():
#         pass
#     def remove_first_song():
#         pass
#     def remove_last_song():
#         pass
        
# class SearchMetadata():

#     def title(sub: str):
#         pass

#     def artist(sub: str):
#         pass

#     def album(sub: str):
#         pass

#     def genre(sub: str):
#         pass

#     def and_operator(list1: list, list2: list):
#         pass

#     def or_operator(list1: list, list2: list):
#         pass
# def load_file(file):
#     with open(file, 'r', encoding='utf8') as m3u:
#         next(m3u)
#         for linia in m3u:
        
#             linia.strip()
#             if linia.startswith('#EXTINF'):
#                 linia = linia.strip().split(',')
#                 linia = linia[1].split(' - ')
#                 # linia = linia.split(' - ')
#                 print(linia)
                

# load_file('IndieCat.m3u')