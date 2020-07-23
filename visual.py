# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 17:13:00 2020

@author: Juanjo_LG
"""

"""GUI para la aplicación de topografía para el TFG."""

import sys
import tkinter as tk
from tkinter import ttk

#Creación de una instancia de la ventana padre.
root = tk.Tk()
root.title("TFG - Juan José Lorenzo Gutiérrez")
#Tamaño de la pantalla del dispositivo
screen_size = root.winfo_screenwidth(),root.winfo_screenheight()
#Ajuste de la geometría para que quede perfecta en el portatil.
#El formato es: 'Ancho'x'Alto'+'X'+'Y'
root.geometry("%dx%d+%d-%d" % (screen_size[0], screen_size[1]-80,-10,40))

#Pruebas con ttk.Treeview para tratarlo como una tabla. FUNCIONA.
table = ttk.Treeview(root)
#Definición de columnas.
table["columns"]=("one","two","three")
table.column("#0", width=270, minwidth=270, stretch=tk.NO)
table.column("one", width=150, minwidth=150, stretch=tk.NO)
table.column("two", width=400, minwidth=200)
table.column("three", width=80, minwidth=50, stretch=tk.NO)
"""id = table.insert('', 'end', 'widgets', text='Widget Tour')
table.insert(id, "end", text = "Table")"""
#Definición de los encabezados.
table.heading("#0",text="Name",anchor=tk.W)
table.heading("one", text="Date modified",anchor=tk.W)
table.heading("two", text="Type",anchor=tk.W)
table.heading("three", text="Size",anchor=tk.W)
#Insertar filas.
table.insert('',0,text='hola',values=("23-Jun-17 11:05","File folder",""))
# Level 1
folder1=table.insert("", 1, text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
table.insert("", 2, text="text_file.txt", values=("23-Jun-17 11:25","TXT file","1 KB"))
# Level 2
table.insert(folder1, "end", text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
table.insert(folder1, "end", text="photo2.png", values=("23-Jun-17 11:29","PNG file","3.2 KB"))
table.insert(folder1, "end", text="photo3.png", values=("23-Jun-17 11:30","PNG file","3.1 KB"))

table.pack()

#Inicializando la raiz.
root.mainloop()
