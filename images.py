# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 12:59:00 2020

@author: Juanjo_LG
"""

"""Script para el manejo y tratamiento de imágenes."""

from PIL import Image
import sys

#Se crea una instancia de la imagen.
im = Image.open("Images/foto_caja.jpg")

#Información de la imagen.
print("Tamaño de la imagen: %dx%d Píxeles" % (im.size))
print("Formato de la imagen: %s" % (im.format))
print("Modo de la imagen: %s" % (im.mode))

#Separa la foto en las diferentes bandas.
#r, g, b = im.split()

#Muestra la foto en la banda del azul.
#b.show()

im_2 = im.convert("L")

#Se muestra la imagen.
im.show()
im_2.show()
