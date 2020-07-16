# -*- coding: utf-8 -*-
"""
Created on Wen Jul 15 12:51:00 2020

@author: Juanjo_LG
"""

"""Elementos Básicos para aplicación de Topografía."""

import math
import numpy as np

#Clase punto.
class Point:
    """
    Se inicializa pasando las coordenadas X, Y, Z del punto para crear alguna
    matriz con el vector de dicho punto.
    También puede pasarse un código de punto o cualquier otro atributo.
    """
    #Constructor del punto.
    def __init__(self, x, y, z=0, **kwargs):
        self.coord = np.array([x, y, z])
        if "n" in kwargs:
            self.num = kwargs["n"]
        #En caso de no tener código, se le asigna uno por defecto.
        if "cod" in kwargs:
            self.cod = kwargs["cod"]
        else:
            self.cod = "Por defecto"
    #Cálculo del módulo (distancia) entre dos vectores de dos puntos.
    def distance(self, x=0, y=0, z=0):
        """Devuelve el módulo del vector o la distancia entre dos puntos en
        caso de que se añadan coordenadas a los parámetros del método"""
        return np.linalg.norm(self.coord-np.array([x,y,z]))
    #Cálculo de azimut de un punto o entre dos puntos.
    def azimut(self, x=0, y=0, z=0):
        azim = (math.atan2(x-self.coord[0],y-self.coord[1]))*(200/math.pi)
        return azim
        #Hay que revisarlo!!!!!

"""Pruebas"""
print("PRUEBAS DE FUNCIONAMIENTO")
p1 = Point(2, 2, 0)
p2 = Point(1, 1, 0)
print("Coordenadas de Punto 1: %s" % (p1.coord))
print(p1.distance(x=1,y=1,z=0))
print(np.linalg.norm(p1.coord-p2.coord))
print("azimut del punto 1: %s" % (p1.azimut(0,0,0)))
