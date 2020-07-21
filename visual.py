# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 17:13:00 2020

@author: Juanjo_LG
"""

"""GUI para la aplicación de topografía para el TFG."""

import sys
import tkinter as tk

#Creación de una instancia de la ventana padre.
root = tk.Tk()
root.title("TFG - Juan José Lorenzo Gutiérrez")
#Tamaño de la pantalla del dispositivo
screen_size = root.winfo_screenwidth(),root.winfo_screenheight()
#Ajuste de la geometría para que quede perfecta en el portatil.
#El formato es: 'Ancho'x'Alto'+'X'+'Y'
root.geometry("%dx%d+%d-%d" % (screen_size[0], screen_size[1]-80,-10,40))

#Inicializando la raiz.
root.mainloop()
