# -*- coding: utf-8 -*-
"""
Created on Wen Jul 15 12:51:00 2020

@author: Juanjo_LG
"""

"""Elementos Básicos para aplicación de Topografía."""

import time
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
        self.coord = np.array([float(x), float(y), float(z)])
        if "n" in kwargs:
            self.num = kwargs["n"]
        #En caso de no tener código, se le asigna uno por defecto.
        if "cod" in kwargs:
            self.cod = kwargs["cod"]
        else:
            self.cod = "Por defecto"
        #Mensaje de creación de cada instancia.
        """print("Creación de punto con coordenadas: %s" % (self.coord))"""

    #Getter para obtener coordenadas.
    def get_coord(self, coord):
        coord = coord.lower()
        index = ""
        if coord == "x":
            index = 0
        elif coord == "y":
            index = 1
        elif coord == "z":
            index = 2
        print("La coordenada '%s' es: %s" % (coord,self.coord[index]))
        return self.coord[index]

    #Setter para cambiar valores de coordenadas.
    def set_coord(self, coord, value):
        coord = coord.lower()
        if coord == "x":
            self.coord[0] = value
        elif coord == "y":
            self.coord[1] = value
        elif coord == "z":
            self.coord[2] = value
        print("Las coordenadas del punto han cambiado: %s" % (self.coord))

    #Cálculo del módulo (distancia) entre dos vectores de dos puntos.
    #Las coordenadas deben ser de tipo np.array.
    def distance(self, coord):
        """Devuelve el módulo del vector o la distancia entre dos puntos en
        caso de que se añadan coordenadas a los parámetros del método"""
        if type(coord) != np.ndarray:
            coord = np.array(coord)
        return np.linalg.norm(self.coord-coord)

    def __str__(self):
        # Se pone en formato string para evitar problemas de compatibilidad.
        try:
            return str("Nº %s | X: %s | Y: %s | Z: %s"\
                % (self.num,self.coord[0],self.coord[1],self.coord[2]))
        except:
            return str("X: %s | Y: %s | Z: %s"\
                % (self.coord[0],self.coord[1],self.coord[2]))

#Clase Ángulo.
class Angle:
    def __init__(self, angle = '', ang_mes = "grad"):
        if ang_mes == "grad":
            pass
        elif ang_mes == "deg":
            angle = angle*(200/180)
        elif ang_mes == "rad":
            angle = angle*(200/math.pi)
        self.ang_mes = "grad"
        self.angle = angle % 400

#Clase Distancia.
class Distance:
    def __init__(self, coord_1, coord_2):
        if type(coord_1) != np.ndarray:
            coord_1 = np.array(coord_1)
        if type(coord_2) != np.ndarray:
            coord_2 = np.array(coord_2)
        self.dist = np.linalg.norm(coord_1-coord_2)

#Clase Azimut, hereda de clase Ángulo.
class Azimut(Angle):
    """Clase Azimut que toma como parámetros dos puntos:
    1 - Primer punto (o inicial)
    2 - Segundo punto (o final)"""
    def __init__(self, st_point, nd_point):
        #Puntos de clase Point.
        self.st_point = st_point
        self.nd_point = nd_point
        dif_coord = self.nd_point.coord - self.st_point.coord
        #El ángulo es el azimut.
        self.azim = (math.atan2(
            dif_coord[0],dif_coord[1]))*(200/math.pi) % 400
    def grad_2_deg(self):
        deg_azim = self.azim * 360/400
        return deg_azim

#Clase Ángulo Cenital.
class Zenith(Angle):
    """Clase Ángulo cenital"""
    def __init__(self, angle = ''):
        Angle.__init__(self, angle = '', ang_mes = "grad")
        self.zenith = angle

#Clase Base.
class Base(Point, Azimut, Zenith):
    def __init__(self, coord, azim):
        pass

#Clase Nivelación.
class Levelling:
    def __init__(self):
        pass

#Clase Poligonal.
class Polygonal:
    def __init__(self):
        pass

"""Pruebas"""
"""print("-------------------------")
print("PRUEBAS DE FUNCIONAMIENTO")
print("-------------------------")
inicio = time.time()"""
p1 = Point(-1, 1, 0, cod = "Arbol")
p2 = Point(1, 1, 0)
p3 = Point(2, 2, 2)
"""print("Dinstancia entre dos puntos con el método del punto: %s" %
    (p1.distance(p2.coord)))
print("Dinstancia entre dos puntos con np.linalg: %s" %
    (np.linalg.norm(p1.coord-p2.coord)))
print("azimut del punto 1: %s" % (p1.azimut([-2,2,0])))
print(p1.cod)
print(p2.coord[1])"""
"""azim_p1_p2 = Azimut(p1,p2)
print(azim_p1_p2.azim)"""
"""ang_1 = Angle(540, ang_mes="deg")
print(ang_1.angle)
print(ang_1.ang_mes)
p1.set_coord("x", 100)
p1.get_coord("y")
fin = time.time()
dif_time = fin - inicio
print(dif_time)"""

azimut = Azimut(p1,p2)
print(azimut.grad_2_deg())