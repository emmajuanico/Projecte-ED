# -*- coding: utf-8 -*-
"""
GrafHash.py : ** REQUIRED ** El vostre codi de la classe GrafHash.
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:14:59 2023

@author: juani
"""

import copy
from ElementData import ElementData
import math 

class GrafHash:
    """Graf amb Adjacency Map structure"""
    
    __slots__= ['_nodes', '_out', '_in']

    class Vertex:
        __slots__ = '_elementdata'

        def __init__(self, elementdata):
            self._elementdata=elementdata
        
        @property
        def get(self):
            return self._elementdata
        
        def __str__(self):
            return str(self._elementdata)
    
################################Definicio Class _Vertex     
    
    
    def __init__(self, ln=[],lv=[],lp=[], digraf = None):
        """Crea graf (no dirigit per defecte, digraf si dirigit es True.
        """
        self._nodes = { }
        self._out = { }
        self._in = { } if digraf else self._out
        
        for n in ln:
            v=self.insert_vertex(n)            
        if lp==[]:
            for v in lv:
                self.insert_edge(v[0],v[1])
        else:
            for vA,pA in zip(lv,lp):
                self.insert_edge(vA[0],vA[1],pA)
    
    def es_digraf(self):
       return self._out != self._in
    
    def getOut(self):
        return self._out
    
    def get(self, key):
        if key in self._nodes:
            return self._nodes[key].get
        else:
            return None
        
    def __contains__(self, key):
        return key in self._nodes
        
    def __getitem__(self, key):
        if key not in self._nodes:
            return None
        else:
            return self._nodes[key].get
        
    def __delitem__(self, key):
        if key in self._nodes:
            self._nodes.pop(key)

    def insert_vertex(self, key, e):
        if isinstance(e, ElementData):

            v= self.Vertex(e)
            self._nodes[key] = v
            self._out[key] = { }
            if self.es_digraf():
                self._in[key] = { }
            
            return v
        else:
            return None
    
    def edges_out(self, node):
        if node in self._nodes:
            return self._out[node]
        else:
            return None
            
    def insert_edge(self, n1, n2, p1=1):
        if n2 in self._out[n1]:
            self._out[n1][n2] += p1
            self._in[n2][n1] += p1
        else:
            self._out[n1][n2] = p1
            self._in[n2][n1] = p1

    def grauOut(self, x):
        d = 0
        for clau, valor  in self._out[x].items():
            d+=valor
        return d # len(self._out[x])

    def grauIn(self, x):
        d = 0
        for clau, valor  in self._in[x].items():
            d+=valor
        return d #len(self._in[x])
    
    def vertices(self):
        """Return una iteracio de tots els vertexs del graf."""
        return self._nodes.__iter__( )

    def edges(self,x):
        """Return una iteracio de tots els edges de x al graf."""
        #return self._out[x].items()
        return iter(self._out[x].items())

        
    def minDistance(self, dist, visitat):
        minim = math.inf
        res = ""
        for node, distancia, in dist.items():
            if node not in visitat and distancia < minim:
                minim = distancia
                res = node
        return res


    def dijkstra(self, node):
        dist = {nAux: math.inf for nAux in self._out}
        visitat = {}
        dist[node] = 0
        predecessor = {}
        for count in range(len(self._nodes) - 1):
            nveiAct = self.minDistance(dist, visitat)
            visitat[nveiAct] = True
            if nveiAct in self._out:
                for n2, p2 in self._out[nveiAct].items():
                    if (n2 not in visitat):
                        if (dist[nveiAct] + p2 < dist[n2]):
                            dist[n2] = dist[nveiAct] + p2
                            predecessor[n2] = nveiAct

        return dist, predecessor

    def camiMesCurt(self, n1, n2):
        
        cami = []
        if n1 in self._nodes and n2 in self._nodes:
            dist, predecessor = self.dijkstra(n1) #dijkstra modificat
            if n2 in predecessor:
                cami.append(n2)
                nodeAct = n2
                while not nodeAct == n1:
                    vei = predecessor[nodeAct]
                    cami.append(vei)
                    nodeAct = vei

            cami.reverse()
        return cami
        
    
    def __len__(self):
        return len(self._nodes)
        
    def __iter__(self):
        return iter(self._nodes)
    
    def __str__(self):
        cad="===============GRAF===================\n"
     
        for it in self._out.items():
            cad1="____________________________\n"
            cad1=cad1+str(it[0])+" : "
            for valor in it[1].items():
                cad1=cad1+str(str(valor[0])+"("+ str(valor[1])+")"+" , " )
                            
            cad = cad + cad1 + "\n"
        
        return cad