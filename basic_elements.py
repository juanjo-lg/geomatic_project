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
        #Mensaje de creación de cada instancia.
        print("Creación de punto con coordenadas: %s" % (self.coord))

    #Cálculo del módulo (distancia) entre dos vectores de dos puntos.
    #Las coordenadas deben ser de tipo np.array.
    def distance(self, coord):
        """Devuelve el módulo del vector o la distancia entre dos puntos en
        caso de que se añadan coordenadas a los parámetros del método"""
        if type(coord) != np.ndarray:
            coord = np.array(coord)
        return np.linalg.norm(self.coord-coord)

    #Cálculo de azimut de un punto o entre dos puntos.
    #Las coordenadas deben ser de tipo np.array.
    def azimut(self, coord):
        #Convierte las coordenadas en una matriz.
        if type(coord) != np.ndarray:
            coord = np.array(coord)
        azim = (math.atan2(coord[0]-self.coord[0],
                coord[0]-self.coord[1]))*(200/math.pi)
        # Si self equivale al origen, el azimut es "0" o Nulo
        if tuple(self.coord) == (0,0,0):
            azim = 0
        # En caso de que no se pasen coordenadas, se calcula el azimut de self.
        elif tuple(coord) == (0,0,0):
            azim = azim + 200
        #Devuelve el resto del azimut entre 300.
        return azim % 400

"""Pruebas"""
print("-------------------------")
print("PRUEBAS DE FUNCIONAMIENTO")
print("-------------------------")
p1 = Point(-1, 1, 0, cod = "Arbol")
p2 = Point(1, 1, 0)
print("Dinstancia entre dos puntos con el método del punto: %s" %
    (p1.distance(p2.coord)))
print("Dinstancia entre dos puntos con np.linalg: %s" %
    (np.linalg.norm(p1.coord-p2.coord)))
print("azimut del punto 1: %s" % (p1.azimut([0,0,0])))
print(p1.cod)
print(p2.coord[1])
