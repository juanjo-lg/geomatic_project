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

#Función para buscar coordenadas de píxeles que tengan un valor r,g,b.
def find_coord(image_name, r_q, g_q, b_q):
    coord_list = []
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            r,g,b = im.getpixel((x,y))
            if r == r_q and g == g_q and b == b_q:
                coord_list.append((x,y))
    return coord_list

print(im.getpixel((0,5)))
print("RGB = 59,59,51",find_coord(im, 59, 59, 51))

#Información de la imagen.
print("Tamaño de la imagen: %dx%d Píxeles" % (im.size))
print("Formato de la imagen: %s" % (im.format))
print("Modo de la imagen: %s" % (im.mode))

#Separa la foto en las diferentes bandas.
#r, g, b = im.split()

#Muestra la foto en la banda del azul.
#b.show()

im_2 = im.convert("L")


#Muestra los píxeles de la imagen.
data = list(im.getdata())

#Cuidado con mostrar todos los datos porque son MUCHISIMOS.
print(data[:5])

#Se muestra la imagen.
"""im.show()
im_2.show()"""
