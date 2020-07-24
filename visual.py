# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 17:13:00 2020

@author: Juanjo_LG
"""

"""GUI para la aplicación de topografía para el TFG."""

import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox  # Si no se importa así, no funciona.

#Creación de una instancia de la ventana padre.
root = tk.Tk()
root.title("TFG - Juan José Lorenzo Gutiérrez")
#Tamaño de la pantalla del dispositivo
screen_size = root.winfo_screenwidth(),root.winfo_screenheight()
#Ajuste de la geometría para que quede perfecta en el portatil.
#El formato es: 'Ancho'x'Alto'+'X'+'Y'
root.geometry("%dx%d+%d-%d" % (screen_size[0], screen_size[1]-100,-10,40))

# Función para abrir un archivo desde el explorador.
def open_file(event = None):
    try:
        file_name = filedialog.askopenfilename()
        archivo = table.insert("",1,text="VIAL_CAJEO.PUN")
        print(file_name)
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

                if line[0] < 20:
                    print(line)

                    table.insert(archivo,count,values=(line[0],line[1],line[2],line[3],line[4]))
                count += 1
        """archivo = filedialog.askopenfile(mode = 'r')
        lines = archivo.read()
        print(lines)"""
    except:
        print("No se puede leer el archivo correctamente.")

#Función para definir el comportamiento del cierre.
def exit(event = None):
    request = messagebox.askyesno(title = "¡Aviso!",
        message = "¿Está seguro de que quiere salir del programa?")
    if request == True:
        sys.exit()

# Función para mostrar el mensaje sobre la información.
def about_click():
    about = ("Author: Juanjo Lorenzo\n"\
        "e-mail: juanjolorenzogutierrez@gmail.com\n"\
        "Date: 2020/24/07\n"\
        "Version: 0.00")
    messagebox.showinfo(title = "Acerca de:", message = about)

# Construcción de menu principal.
menubar = tk.Menu(root)
menu_file = tk.Menu(menubar, tearoff = 0)   # Se crea el menu de archivos.
menu_calc = tk.Menu(menubar, tearoff = 0)    # Menu calculo para transformaciones.
menu_about = tk.Menu(menubar, tearoff = 0)  # Menu about.

# Creación de casilla abrir.
menu_file.add_command(label = "Abrir"
    ,accelerator = "Ctrl+O"
    ,command = lambda: open_file())

# Creación de casilla cerrar.
menu_file.add_command(label = "Salir"
    ,accelerator = "Ctrl+Q"
    ,command = exit)

# Casilla Cálculos.
menu_calc.add_command(label = "Transformation")

# Creacion casilla about.
menu_about.add_command(label = "Acerca de", command = about_click)

# Cascadas de menus.
menubar.add_cascade(label = "Archivo", menu = menu_file)
menubar.add_cascade(label = "Cálculo", menu = menu_calc)
menubar.add_cascade(label = "Info", menu = menu_about)

#Pruebas con ttk.Treeview para tratarlo como una tabla. FUNCIONA.
table = ttk.Treeview(root)
table["columns"] = ("1","2","3","4","5")
table.pack()
table.column("#0", width=150, minwidth=100, stretch=tk.NO)
table.column("1", width=70, minwidth=40, stretch=tk.NO)
table.column("2", width=100, minwidth=50, stretch=tk.NO)
table.column("3", width=100, minwidth=50, stretch=tk.NO)
table.column("4", width=100, minwidth=50, stretch=tk.NO)
table.column("5", width=100, minwidth=50, stretch=tk.NO)
table.heading("#0", text="Archivo")
table.heading("1", text="Número")
table.heading("2", text="X")
table.heading("3", text="Y")
table.heading("4", text="Z")
table.heading("5", text="Código")



#Abrir archivo de puntos e insertarlos en la tabla.
"""with open("VIAL_CAJEO.PUN") as file:
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

        if line[0] < 20:
            print(line)

            table.insert(archivo,count,values=(line[0],line[1],line[2],line[3],line[4]))
        count += 1"""

#Scrollbar para Treeview.   NO FUNCIONA.
scroll_bar = ttk.Scrollbar(table)
table.configure(yscrollcommand = scroll_bar.set)
scroll_bar.config(command = table.yview)
"""scroll_bar.pack(side="right", fill="y")"""

# Se muestra el menu.
root.config(menu = menubar)

# Enlace de los eventos con los atajos.
root.bind('<Control-o>', open_file)
root.bind('<Control-q>', exit)  # Seempre funciona enlazado con la raiz.

#Inicializando la raiz.
root.mainloop()
