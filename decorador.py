# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 12:39:00 2020

@author: Juanjo_LG
"""

"""PRUEBA DE DECORADOR PARA CLASE PUNTOS"""

import numpy as np

class Punto(object):
    _npunto = 0     # Número de instancias activas.
    _nplist = []    # Lista con los números de instancias activas.

    def __init__(self, x:float, y:float, z=0, **kwargs):
        self.coord = np.array([x, y, z])
        """if "n" in kwargs:
            self.n = kwargs["n"]
        else:
            self.n = Punto._npunto
        Punto.incremento_punto()
        print(locals())
        print(self.n)"""
        
    def __del__(self):
        del(self)
        Punto.decremento_punto()
        print(Punto._npunto)

    @classmethod
    # Método de clase para incrementar el número de instancias activas.
    def incremento_punto(cls):
        cls._npunto += 1    # Incremento de instancias activas.
        cls._nplist.append(cls._npunto)
        return cls._npunto

    @classmethod
    # Método de clase para decrementar el número de instancias activas.
    def decremento_punto(cls):
        cls._npunto -= 1    # Decremento de instancias activas.
        #cls._nplist.pop(-1)
        return cls._npunto


def main():
    p1 = Punto("10",12,z=100,n=10)
    for i in range(10):
        a=Punto(10,50)
    del(p1)

if __name__ == "__main__":
    main()