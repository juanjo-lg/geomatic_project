# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 17:13:00 2020

@author: Juanjo_LG
"""

"""GUI para la aplicación de topografía para el TFG."""


# Creación de una instancia de la ventana padre.
import os
import sys
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox  # Si no se importa así, no funciona.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


# Ventana principal
root = tk.Tk()
root.title("TFG - Juan José Lorenzo Gutiérrez")
# Tamaño de la pantalla del dispositivo
screen_size = root.winfo_screenwidth(), root.winfo_screenheight()
# Ajuste de la geometría para que quede perfecta en el portatil.
# El formato es: 'Ancho'x'Alto'+'X'+'Y'
root.geometry("%dx%d+%d-%d" % (screen_size[0], screen_size[1]-100, -10, 40))

root.configure(background="gray60")

# Lista de archivos abiertos.
file_opened = []

# Función para abrir un archivo desde el explorador.
def open_file(event=None):
    try:
        file_name = filedialog.askopenfilename(defaultextension="*.*",
            filetypes=[("All Files", "*.*"),
                ("Archivos de texto", ".txt"),
                ("Fichero GSI (Leica)", ".txt")],
                title="Cargar Puntos")
        print(file_name)
        if file_name not in file_opened:
            # Solo se inserta el nombre del archivo sin la ruta.
            file_no_path = table.insert(
                "", 1, text=os.path.basename(file_name))

            with open(file_name) as file:
                separator = "\t"
                # Contador de número de fila para insertarlo.
                count = 1
                # Variables para el cálculo de la media de coordenadas.
                x_sum = 0
                y_sum = 0
                file_opened.append(file_name)
                for line in file:
                    # Se podría instanciar un punto por cada línea que se lee del archivo.
                    # Se crea una lista formada por las palabra de cada línea.
                    # Así lee los puntos separados tanto por espacios como por tabulaciones.
                    line = "\t".join(line.split())
                    line = line.split(separator)
                    # Cambio de formato de los números.
                    line[0] = int(line[0])
                    line[1] = round(float(line[1]), 3)
                    line[2] = round(float(line[2]), 3)
                    line[3] = round(float(line[3]), 3)
                    # Supresión de salto de línea en el código.
                    try:
                        line[4] = line[4].rstrip()

                    # En caso de que algún punto no tenga código,
                    # se añade "Por Defecto"
                    except:
                        line.append("Por Defecto")

                    # print(line)
                    table.insert(file_no_path, count, values=(
                        line[0], line[1], line[2], line[3], line[4]))
                    count += 1
                    x_sum += float(line[1])
                    y_sum += float(line[2])
                #Posible fallo en count, podría ser count-1
                #No funciona bien, hay que arreglarlo para añadir la media al final de la lista
                file_opened.append((x_sum/count, y_sum/count))
                print(file_opened[0])

        else:
            messagebox.showerror(title="Error",
                                 message="El archivo que intenta abrir ya se encuentra abierto.")
    except:
        messagebox.showerror(title="Error",
                             message="Ha habido un error al abrir el archivo.")

# Función para definir el comportamiento del cierre.
def exit(event=None):
    mess = "¿Está seguro de que quiere salir del programa?"
    request = messagebox.askyesno(title="¡Aviso!", message=mess)
    if request == True:
        sys.exit()

# Función para mostrar el mensaje sobre la información.
def about_click():
    about = ("Author: Juanjo Lorenzo\n"
             "e-mail: juanjolorenzogutierrez@gmail.com\n"
             "Date: 2020/24/07\n"
             "Version: 0.00")
    messagebox.showinfo(title="Acerca de:", message=about)

# Función para seleccionar un item del Treeview.
def select_item(event=None):
    table_item = table.focus()
    item_data = table.item(table_item, option="values")
    return item_data

def draw_canvas(event=None):
    coord = select_item()[1:3]
    ax.plot(coord[0],coord[1],'bo')
    #ax.scatter(coord[0],coord[1],s=10)
    canvas.draw()


# Construcción de menu principal.
menubar = tk.Menu(root)
menu_file = tk.Menu(menubar, tearoff=0)   # Se crea el menu de archivos.
# Menu calculo para transformaciones.
menu_calc = tk.Menu(menubar, tearoff=0)
menu_about = tk.Menu(menubar, tearoff=0)  # Menu about.

# Creación de casilla abrir.
menu_file.add_command(label="Abrir", accelerator="Ctrl+O",
                      command=lambda: open_file())

# Creación de casilla cerrar.
menu_file.add_command(label="Salir", accelerator="Ctrl+Q", command=exit)

# Casilla Cálculos.
menu_calc.add_command(label="Transformation")

# Creacion casilla about.
menu_about.add_command(label="Acerca de", command=about_click)

# Cascadas de menus.
menubar.add_cascade(label="Archivo", menu=menu_file)
menubar.add_cascade(label="Cálculo", menu=menu_calc)
menubar.add_cascade(label="Info", menu=menu_about)

# Frame para herramientas.
fr_tool = tk.Frame(root)
#fr_tool.grid(row=0, column=0, padx=2, pady=0, sticky=tk.W)
fr_tool.pack(side=tk.TOP)

# Frame prueba para canvas matplotlib.
fr_canvas = tk.Frame(root)
fr_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

# Frame para el Treeview.
fr_table = tk.Frame(root)
fr_table.configure(background='gray38')
#fr_table.grid(row=1, column=0, padx=0, pady=0, sticky=tk.W)
fr_table.pack(side=tk.TOP, fill=tk.Y)

# Frame para notebook.
fr_note = tk.Frame(root)
fr_note.pack()

# Botones para herramientas.
btn_open = tk.Button(fr_tool, text="Abrir", command=open_file,
    height=2, width=5, relief=tk.SOLID, borderwidth=1,
    bg='gray38', fg="gray75")
btn_open.pack(side="left", ipadx=5, ipady=5)

btn_save = tk.Button(fr_tool, text="Guardar", command=draw_canvas,
    height=2, width=5, relief=tk.SOLID, borderwidth=1,
    bg='gray38', fg="gray75")
btn_save.pack(side="left", ipadx=5, ipady=5)

btn_format = tk.Button(fr_tool, text="Formato", command='',
    height=2, width=5, relief=tk.SOLID, borderwidth=1,
    bg='gray38', fg="gray75")
btn_format.pack(side="left", ipadx=5, ipady=5)

btn_dist = tk.Button(fr_tool, text="Distancia", command='',
    height=2, width=5, relief=tk.SOLID, borderwidth=1,
    bg='gray38', fg="gray75")
btn_dist.pack(side="left", ipadx=5, ipady=5)

btn_azim = tk.Button(fr_tool, text="Azim", command='',
    height=2, width=5, relief=tk.SOLID, borderwidth=1,
    bg='gray38', fg="gray75")
btn_azim.pack(side="left", ipadx=5, ipady=5)

# Notebook con distintas pestañas.
note = ttk.Notebook(fr_note)
"""note = ttk.Notebook(
        fr_note, width=int(screen_size[0]/2), height=int(screen_size[1]/2))"""
fr_puntos = tk.Frame(note)

note.add(fr_puntos, text="Hola")
note.pack(fill=tk.BOTH, expand=1)

# Encabezado para fr_table.
lbl_table = tk.Label(fr_table, text="Puntos", bg='gray38', fg="gray75")
lbl_table.pack()

# Pruebas con ttk.Treeview para tratarlo como una tabla. FUNCIONA.
table = ttk.Treeview(fr_table)
table.pack(side="left", fill=tk.Y)

# Scrollbar para Treeview. Funciona solamente enlazándola al Frame.
scroll_tree = ttk.Scrollbar(fr_table, orient="vertical", command=table.yview)
scroll_tree.pack(side="right", fill="y")

# Configurar las scroolbar en cada widget.
table.configure(yscrollcommand=scroll_tree.set)

table["columns"] = ("1", "2", "3", "4", "5")
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

"""PRUEBA MATPLOTLIB"""
fig = Figure(figsize=(5,5), dpi=100)
#t = np.arange(0, 3, .01)
#fig.add_subplot(111).plot(t, 2*np.sin(2*np.pi*t))
ax = fig.add_subplot(1,1,1)
ax.set_autoscale_on(True)
#fig.add_subplot(111).plot(20,33,'bo')

canvas = FigureCanvasTkAgg(fig, master=fr_canvas)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand = 1)

# Se muestra el menu.
root.config(menu=menubar)

# Enlace de los eventos con los atajos.
root.bind('<Control-o>', open_file)
root.bind('<Control-q>', exit)  # Seempre funciona enlazado con la raiz.

# Inicializando la raiz.
root.mainloop()
