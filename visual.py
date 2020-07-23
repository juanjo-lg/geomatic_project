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
table["columns"] = ("1","2","3","4","5")
table.pack()
table.heading("#0", text="Archivo")
table.heading("1", text="Número")
table.heading("2", text="X")
table.heading("3", text="Y")
table.heading("4", text="Z")
table.heading("5", text="Código")

archivo = table.insert("",1,text="VIAL_CAJEO.PUN")

#Abrir archivo de puntos e insertarlos en la tabla.
with open("VIAL_CAJEO.PUN") as file:
    separator = "\t"
    #Contador de número de fila para insertarlo.
    count = 1
    for line in file:
        # Se podría instanciar un punto por cada línea que se lee del archivo.
        # Se crea una lista formada por las palabra de cada línea.
        line = line.split(separator)
        # Cambio de formato de los números.
        line[0] = int(line[0])
        line[1] = round(float(line[1]),3)
        line[2] = round(float(line[2]),3)
        line[3] = round(float(line[3]),3)
        # Supresión de salto de línea en el código.
        try:

            line[4] = line[4].rstrip()

        # En caso de que algún punto no tenga código,
        # se añade "Por Defecto"
        except:

            line.append("Por Defecto")

        if line[0] < 10:
            print(line)

            table.insert(archivo,count,values=(line[0],line[1],line[2],line[3],line[4]))
        count += 1

"""#Definición de columnas.
table["columns"]=("one","two","three")
table.column("#0", width=270, minwidth=270, stretch=tk.NO)
table.column("one", width=150, minwidth=150, stretch=tk.NO)
table.column("two", width=400, minwidth=200)
table.column("three", width=80, minwidth=50, stretch=tk.NO)
""""""id = table.insert('', 'end', 'widgets', text='Widget Tour')
table.insert(id, "end", text = "Table")"""
"""#Definición de los encabezados.
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
table.pack()"""

#Inicializando la raiz.
root.mainloop()
