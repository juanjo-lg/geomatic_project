# -*- coding: utf-8 -*-
"""
Created on Wen Aug 19 08:40:00 2020

@author: Juanjo_LG
"""

"""GUI para la aplicación de topografía para el TFG OOP (v.05)."""

import textwrap # Módulo para dar formato a texto y quitarle la sangría.
import os
import tkinter as tk
import numpy as np
import basic_elements as be
import matplotlib.patches as mpatches
from tkinter import filedialog, messagebox, ttk
from Pmw import Balloon as balloon # Crea ventanas emergentes con información.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import ticker

# Clase App que hereda de tk.Tk()
class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()
        # Listas provisionales de apoyo.
        self.splitters = ["espacio","tabulador","coma","punto y coma"]
        self.file_opened = []
        self.item_to_calc = []
        self.config_root()
        self.config_frames()
        self.draw_note(self.fr_note)
        self.draw_canvas(self.fr_canvas)
        self.draw_table(self.fr_table)
        self.draw_text(self.fr_text)
        # Crea tooltip para información.
        self.balloon = balloon(self,relmouse="both",xoffset=10,yoffset=-15)
        # El evento de cerrar desde el aspa se conecta con la función cerrar.
        self.protocol("WM_DELETE_WINDOW", self.close)
        # Enlace de los eventos con los atajos.
        self.bind('<Control-o>', self.open_file)
        self.bind('<Control-e>', self.select_all)
        self.bind('<Control-f>', self.filter)
        self.bind('<Control-d>', self.draw_points)
        self.bind('<Control-i>', self.add_manual_txt)
        self.table.bind('<Escape>', self.deselect_all)
        self.table.bind('<Button-3>',self.popup_table)
        # Enlace con los toolip.
        self.balloon.bind(self.btn_open,'Abrir archivo')
        self.balloon.bind(self.btn_save,'Guardar archivo')
        self.balloon.bind(self.btn_add,'Añadir punto de forma manual')
        self.balloon.bind(self.btn_clean,'Borrar cuadro de texto')
        self.balloon.bind(self.btn_clear_canvas,'Reiniciar dibujo')
        self.balloon.bind(self.btn_select_all,'Seleccionar todos los puntos')
        self.balloon.bind(self.btn_filter,'Filtrar puntos por códigos')
        self.balloon.bind(self.btn_draw,'Dibujar puntos seleccionados')
        self.balloon.bind(self.btn_dist_azim,'Cálculo de distancia y azimut')
        # Siempre funciona enlazado con la raiz.
        self.bind('<Control-q>', self.close)

    def config_root(self):
        # Configuración de ventana principal.
        self.title("TFG - Juan José Lorenzo Gutiérrez")
        self.screen_size = self.winfo_screenwidth(),self.winfo_screenheight()
        self.geometry("%dx%d+%d-%d" %
            (self.screen_size[0], self.screen_size[1]-70, -10, 30))
        self.configure(background='gray60')

    def config_frames(self):
        # Configuración de los Frames de la App.
        self.fr_note = tk.Frame(width=self.screen_size[0//2])
        self.fr_canvas = tk.Frame(width=self.screen_size[0]//2)
        self.fr_table = tk.Frame(bg='gray38',width=self.screen_size[0]//2)
        self.fr_text = tk.Frame(bg='gray60',width=self.screen_size[0]//2,
            height=self.screen_size[1]//2)
        # Colocación de Frames.
        self.fr_note.pack(side=tk.TOP,fill=tk.Y)
        self.fr_canvas.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
        self.fr_table.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.fr_text.pack(side=tk.BOTTOM,fill=tk.BOTH)

    def draw_note(self,master):
        # Configuracion del Notebook con estilos de diseño.
        self.style = ttk.Style()
        # De esta forma se quitan los bordes.
        self.style.theme_use('default')
        # 'TNotebook','TNotebook.Tab' y 'TFrame' son estilos de ttk.
        self.style.configure('TNotebook',borderwidth=0)
        # Quita las líneas punteadas de las tablas al seleccionarlas.
        self.style.configure('TNotebook.Tab',borderwidth=0,
            focuscolor=self.style.configure(".")["background"])
        self.style.configure('TFrame',borderwidth=0,background="gray60")
        # Con 'readonly' no salen las palabras enmarcadas.
        self.style.configure('TCombobox',
            selectbackground=[('readonly','white')],
            selectforeground=[('readonly','black')],
            fieldbackground=[('readonly','gray60')])
        # Constructor del Notebook.
        self.notebook = ttk.Notebook(master,style='TNotebook',
            width=int(self.screen_size[0]),
            height=int(self.screen_size[1]/12))
        # Funciones para crear distintas pestañas.
        def file():
            self.fr_file = ttk.Frame(master,style='TFrame')
            # Botón para abrir archivos.
            # Imagen para botón "abrir".
            self.img_open = tk.PhotoImage(file="images/carpeta_3.png")
            self.btn_open = tk.Button(
                self.fr_file,image=self.img_open,text='Abrir',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                width=80,bg="gray60",command=self.open_file,
                relief=tk.FLAT)
            self.btn_open.pack(side=tk.LEFT)
            # Frame para separadores.
            self.fr_separator = ttk.Frame(self.fr_file,style='TFrame',
                relief=tk.SUNKEN,borderwidth=1)
            self.fr_separator.pack(side=tk.LEFT,ipadx=5)
            # Etiqueta de separadores.
            self.lbl_separator = tk.Label(self.fr_separator,
                text='Separador de Datos',
                background="gray60", fg="black")
            self.lbl_separator.pack(side=tk.TOP,pady=5)
            # Combobox con los distintos separadores.
            self.cmb_separator = ttk.Combobox(self.fr_separator,
                values=self.splitters,justify=tk.CENTER,state="readonly")
            self.cmb_separator.set(self.splitters[1])
            #self.cmb_separator["values"] = self.splitters
            self.cmb_separator.pack(pady=5)
            """self.cmb_separator.bind("<<ComboboxSelected>>",
                print(self.cmb_separator.get()))"""
            # Botón para Guardar archivos.
            # Imagen para botón "guardar".
            self.img_save = tk.PhotoImage(file="images/salvar.png")
            self.btn_save = tk.Button(
                self.fr_file,image=self.img_save,text='Guardar',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                width=80,bg="gray60",
                command=lambda:print(self.notebook.tabs()),
                relief=tk.FLAT)
            self.btn_save.pack(side=tk.LEFT)
            # Botón para abrir base de datos.
            # Imagen para botón "base de datos".
            self.img_db = tk.PhotoImage(file="images/base-de-datos_2.png")
            self.btn_db = tk.Button(
                self.fr_file,image=self.img_db,text='DB',
                compound=tk.TOP,
                height=int(self.screen_size[1]/12),
                width=80,bg="gray60",
                relief=tk.FLAT)
            self.btn_db.pack(side=tk.LEFT)
            # Botón para seleccionar todos los puntos.
            # Imagen para botón "Seleccionar Todo".
            self.img_select_all = tk.PhotoImage(file="images/select_all.png")
            self.btn_select_all = tk.Button(
                self.fr_file,image=self.img_select_all,text='Seleccionar todo',
                compound=tk.TOP,command=self.select_all,
                height=int(self.screen_size[1]/12),
                width=80,bg="gray60",
                relief=tk.FLAT)
            self.btn_select_all.pack(side=tk.LEFT)
            # Botón para filtrar puntos.
            # Imagen para botón "Filtrar".
            self.img_filter = tk.PhotoImage(file="images/filtrar.png")
            self.btn_filter = tk.Button(
                self.fr_file,image=self.img_filter,text='Filtrar',
                compound=tk.TOP,command=self.filter,
                height=int(self.screen_size[1]/12),
                width=80,bg="gray60",
                relief=tk.FLAT)
            self.btn_filter.pack(side=tk.LEFT)
            # Botón para dibujar puntos.
            # Imagen para botón "Dibujar".
            self.img_draw = tk.PhotoImage(file="images/draw_one.png")
            self.btn_draw = tk.Button(
                self.fr_file,image=self.img_draw,text='Dibujar puntos',
                compound=tk.TOP,command=self.draw_points,
                height=int(self.screen_size[1]/12),
                width=80,bg="gray60",
                relief=tk.FLAT)
            self.btn_draw.pack(side=tk.LEFT)
            # Botón para Cálculo de estadísticas.
            # Imagen para botón "Estadísticas".
            self.img_stat = tk.PhotoImage(file="images/estadistica.png")
            self.btn_stat = tk.Button(
                self.fr_file,image=self.img_stat,text='Estadística',
                compound=tk.TOP,
                height=int(self.screen_size[1]/12),
                width=80,bg="gray60",command=self.add_points,
                relief=tk.FLAT)
            self.btn_stat.pack(side=tk.LEFT)
            # Botón para cerrar el programa.
            # Imagen para botón "cerrar".
            self.img_close = tk.PhotoImage(file="images/cerrar_ico_2.png")
            self.btn_close = tk.Button(
                self.fr_file,image=self.img_close,text='Cerrar',
                compound=tk.TOP,command=self.close,
                height=int(self.screen_size[1]/12),
                width=80,bg="gray60",
                relief=tk.FLAT)
            self.btn_close.pack(side=tk.RIGHT)
            self.notebook.add(self.fr_file,text="Archivo")
        def calculus():
            self.fr_calc = ttk.Frame(master,style='TFrame')
            # Botón de distancia y azimut.
            # Imagen para botón "Distancia y azimut".
            self.img_dist_azim = tk.PhotoImage(file="images/calculadora.png")
            self.btn_dist_azim = tk.Button(
                self.fr_calc,image=self.img_dist_azim,text='Dist & Azim',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                command=self.dist_azim,width=80,bg="gray60",
                relief=tk.FLAT)
            self.btn_dist_azim.pack(side=tk.LEFT)
            # Botón de transformación.
            # Imagen para botón "Transformación".
            self.img_trans = tk.PhotoImage(file="images/global.png")
            self.btn_trans = tk.Button(
                self.fr_calc,image=self.img_trans,text='Transformación',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                command=self.transformation,width=80,bg="gray60",
                relief=tk.FLAT)
            self.btn_trans.pack(side=tk.LEFT)
            self.notebook.add(self.fr_calc,text="Cálculos")
            # Botón de Intersección.
            # Imagen para botón "Intersección".
            self.img_inter = tk.PhotoImage(file="images/mercado.png")
            self.btn_inter = tk.Button(
                self.fr_calc,image=self.img_inter,text='Intersección',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                width=80,bg="gray60",
                relief=tk.FLAT)
            self.btn_inter.pack(side=tk.LEFT)
            self.notebook.add(self.fr_calc,text="Cálculos")
            # Botón de poligonal.
            # Imagen para botón "Itinerario".
            self.img_polig = tk.PhotoImage(file="images/mapa.png")
            self.btn_polig = tk.Button(
                self.fr_calc,image=self.img_polig,text='Itinerario',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                width=80,bg="gray60",
                relief=tk.FLAT)
            self.btn_polig.pack(side=tk.LEFT)
        def info():
            self.fr_info = ttk.Frame(master,style='TFrame')
            # Botón Información.
            # Imagen para botón "Información".
            self.img_info = tk.PhotoImage(file="images/ayuda.png")
            self.btn_info = tk.Button(
                self.fr_info,image=self.img_info,text='Información',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                width=80,bg="gray60",command=self.show_info,
                relief=tk.FLAT)
            self.btn_info.pack(side=tk.LEFT)
            self.notebook.add(self.fr_info,text="Información")
        # Inicialización de pestañas file y calculus
        file()
        calculus()
        info()
        self.notebook.pack(fill=tk.BOTH,expand=True)

    def draw_canvas(self,master):
        # Configuración de canvas.
        # Al cambiar el dpi se mueve al pasar el ratón por fuera del gráfico.
        self.fig = Figure(figsize=(3,3), dpi=80)
        self.ax = self.fig.add_subplot(1,1,1)
        # Iguala la escala de los ejes x e y y ajusta la caja a los límites.
        self.ax.set_aspect('equal',adjustable='datalim')
        self.ax.set_xlabel('Coordenadas X')
        self.ax.set_ylabel('Coordenadas Y')
        """HAY QUE DAR UNA VUELTA AL TICKLABEL_FORMAT PARA QUE NO HAYA EXPONENCIAL"""
        self.ax.ticklabel_format(style='plain', axis='both')
        """Quito las coordenadas para que no me reescalen la figura."""
        # Formato de coordenadas mostrado en los ejes 'X' e 'Y'.
        self.ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
        self.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
        #self.ax.format_coord = lambda x, y: ""
        self.canvas = FigureCanvasTkAgg(self.fig,master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas,master)
        self.img_clear = tk.PhotoImage(file="images/borrar24.png")
        self.btn_clear_canvas = tk.Button(self.toolbar,
            command=self.empty_canvas,image=self.img_clear)
        self.btn_clear_canvas.pack(side=tk.LEFT,fill=tk.Y)
        # Muestra todas las herramientas de la barra del canvas.
        # print(self.toolbar.toolitems)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
    def draw_table(self,master):
        # Label para la tabla de puntos.
        # Si esta etiqueta, el canvas se come a la tabla.
        self.lbl_table=tk.Label(self.fr_table,text="Puntos",width=90,
            bg='gray38',fg="gray75")
        self.lbl_table.pack()
        # Creación de tabla para cargar los puntos.
        self.table = ttk.Treeview(master,height=1000)
        self.table.pack(fill=tk.BOTH,expand=True)
        # Scrollbar para Treeview. Funciona solamente enlazándola al Frame.
        self.scroll_tree = ttk.Scrollbar(self.table, orient="vertical",
            command=self.table.yview)
        self.scroll_tree.pack(side="right", fill="y")
        # Configuración de la scroolbar.
        self.table.configure(yscrollcommand=self.scroll_tree.set)
        # Inserción de campos en la tabla.
        self.table["columns"] = ("1", "2", "3", "4", "5")
        self.table.column("#0",width=170,minwidth=100,stretch=tk.NO)
        self.table.column("1",width=60,minwidth=40,
            stretch=tk.NO,anchor=tk.CENTER)
        self.table.column("2",width=110,minwidth=50,
            stretch=tk.NO,anchor=tk.CENTER)
        self.table.column("3",width=110,minwidth=50,
            stretch=tk.NO,anchor=tk.CENTER)
        self.table.column("4",width=90,minwidth=50,
            stretch=tk.NO,anchor=tk.CENTER)
        self.table.column("5",width=110,minwidth=50,
            stretch=tk.NO,anchor=tk.CENTER)
        self.table.heading("#0", text="Archivo")
        self.table.heading("1", text="Número")
        self.table.heading("2", text="X")
        self.table.heading("3", text="Y")
        self.table.heading("4", text="Z")
        self.table.heading("5", text="Código")
        # Configuración de estilo del Treeview.
        self.style.configure('Treeview.Heading',
            relief=tk.FLAT,background="gray75")
        self.style.configure('Treeview',background="gray60",
            focuscolor=self.style.configure(".")["background"])
        """NO FUNCIONA FOCUSCOLOR EN ESTA OCASIÓN"""
    def draw_text(self, master):
        # Creación de caja de texto para mostrar información.
        self.text = tk.Text(master,bg='gray60')
        self.text.pack(padx=5,pady=5,fill = tk.BOTH,
            expand=True)
        # Botón para añadir puntos de forma manual al texto.
        self.btn_add = tk.Button(master,text='Añadir Punto',
            bg="gray60",relief=tk.FLAT,command=self.add_manual_txt)
        self.btn_clean = tk.Button(master,text='Borrar',
            command=self.remove_text,bg="gray60",relief=tk.FLAT)

        self.btn_add.pack(padx=5,pady=5,side=tk.LEFT)
        self.btn_clean.pack(padx=5,pady=5,side=tk.LEFT)
    def popup_table(self,event=None):
        # Menú para ejecutar en el Treeview al pulsar con el botón derecho.
        self.popup_menu_table = tk.Menu(self.table, tearoff=0)
        self.popup_menu_table.add_command(label='Abrir fichero',
            accelerator="Ctrl+O",command=self.open_file)
        self.popup_menu_table.add_command(label='Cerrar fichero',
            accelerator="",command=self.remove_file)
        self.popup_menu_table.add_command(label='Cerrar ficheros',
            accelerator="Ctrl+R",command=self.remove_table)
        self.popup_menu_table.add_separator()
        self.popup_menu_table.add_command(label='Filtrar',
            accelerator="Ctrl+F",command=self.filter)
        self.popup_menu_table.add_command(label='Seleccionar todos',
            accelerator="Ctrl+E",command=self.select_all)
        self.popup_menu_table.add_command(label='Deseleccionar todos',
            accelerator="Esc",command=self.deselect_all)
        self.popup_menu_table.add_separator()
        self.popup_menu_table.add_command(label='Insertar punto',
            accelerator="Ctrl+I",command=self.add_manual_txt)
        self.popup_menu_table.add_separator()
        self.popup_menu_table.add_command(label='Dibujar puntos',
            accelerator="Ctrl+D",command=self.draw_points)
        self.popup_menu_table.add_separator()
        self.popup_menu_table.add_command(label='Cerrar',
            accelerator="Ctrl+Q",command=self.close)
        # Se muestra en las coordenadas en las que se encuentra el ratón.
        self.popup_menu_table.tk_popup(event.x_root,event.y_root)
        self.popup_menu_table.grab_release()
    def open_file(self,event=None):
        # Función para abrir fichero de puntos.
        self.file_name = filedialog.askopenfilename(defaultextension="*.*",
            filetypes=[("All Files", "*.*"),
                ("Archivos de texto", ".txt"),
                ("Fichero GSI (Leica)", ".txt")],
                title="Cargar Puntos")
        if self.file_name:
            try:
                if self.file_name not in self.file_opened:
                    # Solo se inserta el nombre del archivo sin la ruta.
                    self.file_no_path = self.table.insert(
                        "", 1, text=os.path.basename(self.file_name))
                    with open(self.file_name) as self.file:
                        separators = [" ","\t",",",";"]
                        for i in enumerate(self.splitters):
                            if i[1] == self.cmb_separator.get():
                                # Usa el índice de la lista de separadores.
                                separator = separators[i[0]]
                        # Contador de número de fila para insertarlo.
                        count = 1
                        # Variables para el cálculo de la media de coordenadas.
                        x_sum = 0
                        y_sum = 0
                        self.file_opened.append(self.file_name)
                        for line in self.file:
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
                            self.table.insert(self.file_no_path,count,values=(
                                line[0],line[1],line[2],line[3],line[4]))

                            #Posible fallo en count, podría ser count-1
                            count += 1
                        print(self.file_opened)
                else:
                    messagebox.showerror(title="Error",
                        message="El archivo ya se encuentra abierto.")
            except:
                try:
                    # Elimina de la lista el archivo que no se abre.
                    self.file_opened.remove(self.file_name)
                    # Elimina de la tabla el nombre de archivo que no se abre.
                    # FUNCIONA!!!!!!!
                    item_to_delete = len(self.table.get_children())-1
                    self.table.delete(self.table.get_children()[item_to_delete])
                except:
                    pass # Habrá que implementar algo aquí.
                messagebox.showerror(title="Error",
                    message="Ha habido un error al abrir el archivo.")
    def select_all(self, event=None):
        # Forma de iterar entre todos los subelementos de un parent en Treeview.
        for children in self.table.get_children():
            child = self.table.get_children(children)
            self.table.selection_add(child)# Selecciona todos los items.
        # Elimina el nombre del archivo de la selección.
        self.table.selection_remove(children)
        table_items = self.table.selection()
    def deselect_all(self, event=None):
        # Deselecciona los items que estén seleccionados.
        self.table.selection_remove(self.table.selection())
    def filter(self, event=None):
        # Función para filtrar puntos según su código en el Treeview.
        def lbl_ntr_btn_top(master):
            # Función para colocar los elementos en la Toplevel de filtrado.
            lbl_filter = tk.Label(master,text='Código a filtrar:',bg="gray75")
            self.ntr_filter = tk.Entry(master)
            btn_filter = tk.Button(master,text='Filtrar',bg="gray60",
                command=command_btn_filter)
            lbl_filter.pack(pady=5)
            self.ntr_filter.pack(padx=10)
            btn_filter.pack(pady=5)

        def command_btn_filter(event = None):
            # Función de filtrado.
            filter = self.ntr_filter.get()
            self.deselect_all()
            for children in self.table.get_children():
                child = self.table.get_children(children)
                for item in child:
                    item_data = self.table.item(item,option="values")
                    # Se busca la coincidencia en minúsculas.
                    if filter.lower() in item_data[4].lower():
                        self.table.selection_add(item)
            self.table.selection_remove(children)
            self.top_filter.destroy()

        # En caso de tener abierto algún archivo, se abre una Toplevel.
        if self.table.get_children():
            # Toplevel para filtrado de puntos.
            self.top_filter = tk.Toplevel(self)
            self.top_filter.geometry("%dx%d" % (300,85))
            self.top_filter.configure(background="gray75")
            self.top_filter.title('Filtrado de puntos.')
            self.top_filter.resizable(False,False)
            lbl_ntr_btn_top(self.top_filter)
            self.ntr_filter.focus()
        # Enlace para comando de botón dando a enter en el Entry.
        self.ntr_filter.bind('<KeyPress-Return>', command_btn_filter)
    def draw_points(self, event= None):
        # Dibuja los puntos seleccionados en la tabla.
        if self.table.selection():
            table_items = self.table.selection()
            x_list = []
            y_list = []
            for item in table_items:
                item_data = self.table.item(item,option="values")
                x_list.append(float(item_data[1]))
                y_list.append(float(item_data[2]))
                #print(item_data)
                #array.append([float(item_data[1]),float(item_data[2])])
                """self.ax.plot(float(item_data[1]),float(item_data[2]),
                color="black",marker=".")
                self.canvas.draw()"""
            self.ax.scatter(x_list,y_list,marker=".")
            self.canvas.draw()
    def empty_canvas(self, event = None):
        # Destrucción y redibujaddo del canvas.
        self.canvas.get_tk_widget().destroy()
        self.toolbar.destroy()
        self.draw_canvas(self.fr_canvas)
    def add_points(self, event = None):
        # Añade puntos al cuadro de texto.
        if self.table.selection():
            table_items = self.table.selection()
            for item in table_items:
                item_data=str(self.table.item(item,option="values"))
                # Forma de borrar comillas y paréntesis.
                item_data=item_data.translate({ord(i):None for i in "'()"})
                self.item_to_calc.append(item_data)
                self.text.insert(tk.END,item_data+"\n")
    def add_manual_txt(self, event = None):
        # Ventana emergente para insertar puntos de forma manual.
        def ntr_clean(event = None):
            # Limpia los Entries.
            for i in self.top_manual.children.values():
                if type(i) == tk.Entry:
                    i.delete(0,tk.END)
        def ntr_insert(event = None):
            # Inserta el punto en el Treeview y en el cuadro de texto.
            line = []
            count = 0
            # En caso de que 'Manual' no exista, lo crea en la tabla.
            if 'Manual' not in self.file_opened:
                # Se añade 'Manual' a la lista de ficheros abiertos.
                self.file_opened.append('Manual')
                self.manual = self.table.insert("", 1, text='Manual')
            # Recorre los elementos hijos de Toplevel.
            for i in self.top_manual.children.values():
                # En caso de ser Entries, recupera los valores.
                if type(i) == tk.Entry:
                    line.append(i.get())
                    count += 1
            # Si no se introduce un código, se le asigna 'Por defecto'.
            if line[4] == "":
                line[4] = 'Por defecto'
            # Se insertan los valores en la tabla.
            self.table.insert(self.manual,count,values=(
                line[0],line[1],line[2],line[3],line[4]))
            ntr_clean()

        # Toplevel para inserción de puntos de forma manual.
        self.top_manual = tk.Toplevel(self)
        self.top_manual.title('Inserción manual de puntos.')
        self.top_manual.configure(background="gray75")
        # Etiquetas del Toplevel
        self.lbl_top_n = tk.Label(self.top_manual,text='Número',bg="gray75")
        self.lbl_top_x = tk.Label(self.top_manual,text='X',bg="gray75")
        self.lbl_top_y = tk.Label(self.top_manual,text='Y',bg="gray75")
        self.lbl_top_z = tk.Label(self.top_manual,text='Z',bg="gray75")
        self.lbl_top_cod = tk.Label(self.top_manual,text='Código',bg="gray75")
        # Entries del Toplevel.
        self.ntr_top_n = tk.Entry(self.top_manual)
        self.ntr_top_x = tk.Entry(self.top_manual)
        self.ntr_top_y = tk.Entry(self.top_manual)
        self.ntr_top_z = tk.Entry(self.top_manual)
        self.ntr_top_cod = tk.Entry(self.top_manual)
        # Botones del Toplevel.
        self.btn_top_ins = tk.Button(self.top_manual,text='Insertar',
            command=ntr_insert,relief=tk.FLAT,bg="gray60")
        self.btn_top_clear = tk.Button(self.top_manual,text='Borrar',
            command=ntr_clean,relief=tk.FLAT,bg="gray60")
        self.btn_top_close = tk.Button(self.top_manual,text='Cerrar',
            command=lambda:self.top_manual.destroy(),relief=tk.FLAT,bg="gray60")

        self.lbl_top_n.grid(column=0,row=0)
        self.lbl_top_x.grid(column=1,row=0)
        self.lbl_top_y.grid(column=2,row=0)
        self.lbl_top_z.grid(column=3,row=0)
        self.lbl_top_cod.grid(column=4,row=0)
        self.ntr_top_n.grid(column=0,row=1)
        self.ntr_top_x.grid(column=1,row=1)
        self.ntr_top_y.grid(column=2,row=1)
        self.ntr_top_z.grid(column=3,row=1)
        self.ntr_top_cod.grid(column=4,row=1)
        # Separador entre las Entries y los botones.
        ttk.Separator(self.top_manual,orient=tk.HORIZONTAL
            ).grid(column=0,row=2,columnspan=5,sticky="ew")

        self.btn_top_ins.grid(column=1,row=3,sticky=tk.N+tk.S+tk.E+tk.W)
        self.btn_top_clear.grid(column=2,row=3,sticky=tk.N+tk.S+tk.E+tk.W)
        self.btn_top_close.grid(column=3,row=3,sticky=tk.N+tk.S+tk.E+tk.W)

        self.top_manual.resizable(False,False)
    def remove_file(self, event = None):
        # Borrado de ficheros seleccionados.
        if self.table.selection() is not None:
            files_to_remove = self.table.selection()
            for i in files_to_remove:
                try:
                    # Se encuentra el padre del item seleccionado y su nombre.
                    parent = self.table.parent(i)
                    file_name = self.table.item(parent,'text')
                    for j in self.file_opened:
                        if file_name in j:
                            # Se borra el fichero de la lista de "Abiertos".
                            self.file_opened.remove(j)
                    # Borrado del fichero con los puntos del Treeview.
                    self.table.delete(self.table.parent(i))
                except: pass
    def remove_table(self, file = None, event = None):
        # Limpieza de la tabla.
        for item in self.table.get_children():
            self.table.delete(item)
        # Permite que se puedan volver a abrir los archivos borrados.
        if file == None:
            self.file_opened.clear()
        else:
            self.file_opened.remove(file)
    def remove_text(self, event = None):
        # Limpieza del cuadro de texto.
        self.text.delete('1.0',tk.END)
    def dist_azim(self, event = None):
        """HAY QUE SEGUIR CON ESTO, NO ESTÁ ACABADO."""
        """HAY QUE PONER EL NÚMERO DE PUNTO EN EL DIBUJO"""
        # Función para el cálculo de la distancia y azimut entre 2 puntos.
        global table_points, selected_points
        selected_pnts = []
        table_points = []
        table_strings = []
        table_items = self.table.selection()
        str_var = tk.StringVar()

        # En caso de tener abierto algún archivo, se abre una Toplevel.
        if self.table.selection():
            self.top_dist_azim = tk.Toplevel(self)
            self.top_dist_azim.geometry("%dx%d" % (300,85))
            self.top_dist_azim.configure(background="gray75")
            self.top_dist_azim.title('Azimut & Distancia')
            #self.top_dist_azim.resizable(False,False)
            # Se pone el foco en el Toplevel.
            self.top_dist_azim.focus()

        # Selección de puntos seleccionados en el Treeview.
        for item in table_items:
            item_data = self.table.item(item,option="values")
            point = be.Point(item_data[1],item_data[2],n=item_data[0])
            table_points.append(point)
        for i in table_points:
            table_strings.append(str(i))
        # Combobox para seleccionar puntos.
        self.cmb_dist_azim = ttk.Combobox(self.top_dist_azim,
            values=[i for i in table_strings],
            justify=tk.CENTER,state="readonly",width=40)

        str_var.set("Introduzca punto de estación.")
        self.lbl_d_a = tk.Label(self.top_dist_azim,textvariable=str_var
            ,bg="gray75")

        self.lbl_d_a.pack()
        self.cmb_dist_azim.pack()

        def handler_cmb_dist_azim(event=None):
            # Manejador para el evento de cambio de valor del Combobox
            pos = self.cmb_dist_azim.current() # Posición del punto.
            point = table_points[pos]
            selected_pnts.append(point)
            # Cambia el texto del Label dependiendo de la situación.
            if len(selected_pnts) == 1:
                str_var.set("Introduzca punto visado.")
            elif len(selected_pnts) == 2:
                azimut = be.Azimut(selected_pnts[0],selected_pnts[1]).azim
                azimut = round(azimut,4)
                dist = selected_pnts[0].distance(selected_pnts[1].coord)
                dist = round(dist,3)
                text_1 = "Azimut Calculado entre los puntos: %s y %s: %s g"\
                    "\n"%(selected_pnts[0].num,selected_pnts[1].num,azimut)
                text_2 = "Distancia entre los puntos: %s y %s: %s m"\
                    "\n\n"%(selected_pnts[0].num,selected_pnts[1].num,dist)
                self.empty_canvas()
                # Dibuja la línea de azimut (Norte) desde el punto de estación.
                self.ax.plot((selected_pnts[0].coord[0],
                    selected_pnts[0].coord[0]),
                    (selected_pnts[0].coord[1],
                    selected_pnts[0].coord[1]+dist/2))
                # Dibuja una línea entre los puntos.
                self.ax.plot((selected_pnts[0].coord[0],
                    selected_pnts[1].coord[0]),
                    (selected_pnts[0].coord[1],
                    selected_pnts[1].coord[1]))
                # Adición de texto.
                self.ax.text((selected_pnts[0].coord[0] +
                    selected_pnts[1].coord[0])/2,
                    (selected_pnts[0].coord[1] +
                    selected_pnts[1].coord[1])/2,
                    str(azimut)+' g\n' + str(dist)+' m')
                self.ax.text(selected_pnts[0].coord[0],
                    selected_pnts[0].coord[1]+dist/2,
                    'N',horizontalalignment = 'center')
                # Dibujo de arco.
                azim_deg = azimut * 360 / 400
                arc = mpatches.Arc((selected_pnts[0].coord[0],
                    selected_pnts[0].coord[1]),
                    dist/10,dist/10,theta1=90-azim_deg,theta2=90)
                self.ax.add_patch(arc)

                self.text.insert(tk.END,text_1+text_2)
                self.top_dist_azim.destroy()
                self.dist_azim()
            # Se deja vacía la caja del Combobox.
            self.cmb_dist_azim.set("")

        # Evento que devuelve los datos del Combobox cada vez que se cambia.
        self.cmb_dist_azim.bind("<<ComboboxSelected>>", handler_cmb_dist_azim)
    def transformation(self, event=None):
        """HAY QUE SEGUIR CON ESTO"""
        # Función de transformación de puntos.
        table_points = []
        table_strings = []
        table_items = self.table.selection()
        str_var = tk.StringVar()
        var_trans = tk.IntVar()
        var_trans.set(1)

        def handler_cmb_trans(event=None):
            # Manejador para el evento de cambio de valor del Combobox.
            pass
        def handler_radio(event=None):
            # Manejador para el evento de cambio de valor del Radiobutton.
            if var_trans.get() == 1:
                print("Parámetros")
            else:
                print("Cálculo Helmert")

        # En caso de tener abierto algún archivo, se abre una Toplevel.
        if self.table.selection():
            self.top_trans = tk.Toplevel(self)
            #self.top_trans.geometry("%dx%d" % (300,85))
            self.top_trans.configure(background="gray75")
            self.top_trans.title('Transformación Helmert')
            self.top_trans.focus()

        # Selección de puntos seleccionados en el Treeview.
        for item in table_items:
            item_data = self.table.item(item,option="values")
            point = be.Point(item_data[1],item_data[2],n=item_data[0])
            table_points.append(point)
        for i in table_points:
            table_strings.append(str(i))
        # Frames para la Toplevel de transformación.
        self.fr_trans_1 = tk.Frame(self.top_trans,bg="gray75")
        self.fr_trans_2 = tk.Frame(self.top_trans,bg="gray75")
        # Label para los Frames.
        self.lbl_trans_1 = tk.Label(self.fr_trans_1,textvariable=str_var,
            bg="gray75")
        self.lbl_trans_2 = tk.Label(self.fr_trans_2,
            text='Tipo de cálculo',bg="gray75")
        # Combobox para seleccionar puntos.
        self.cmb_trans = ttk.Combobox(self.fr_trans_1,
            values=[i for i in table_strings],
            justify=tk.CENTER,state="readonly",width=40)
        # Radiobuttons para opciones de cálculo.
        self.radio_trans_param = tk.Radiobutton(self.fr_trans_2,
            text="Cálculo de parámetros",bg="gray75",
            variable=var_trans,value=1,command=handler_radio)
        self.radio_trans_calc = tk.Radiobutton(self.fr_trans_2,
            text='Cálculo de transformación',bg="gray75",
            variable=var_trans,value=2,command=handler_radio)
        """LA VARIABLE SE TIENE QUE CONFIGURAR AL CAMBIAR EL Combobox
        Y EL RADIOBUTTON"""
        str_var.set("Pruebas")
        # Invoke hace que se active ese Radiobutton.
        self.radio_trans_param.invoke()

        self.fr_trans_1.pack(side=tk.LEFT)
        self.fr_trans_2.pack(side=tk.RIGHT)
        self.lbl_trans_1.pack()
        self.lbl_trans_2.pack()
        self.cmb_trans.pack()
        self.radio_trans_param.pack()
        self.radio_trans_calc.pack()

    def show_info(self, event=None):
        mess = 'Autor: Juan José Lorenzo Gutiérrez\n'\
        'Mail: juanjolorenzogutierrez@gmail.com\n\n'\
        'Proyecto desarrollado con Python 3x y Tkinter para el TFG del curso'\
        ' de adaptación al Grado de Geomática y Topografía.\n\n'\
        'Iconos obtenidos de:\n- Smashicons\n- Freepik\n- Google\n'\
        '- Kiranshastry\n- Gregor Cresnar'
        msgbox_info=messagebox.showinfo(title='Acerca de:',message=mess)
    def close(self, event=None):
        # Función para cerrar el programa.
        mess = "¿Está seguro de que quiere salir del programa?"
        request = messagebox.askyesno(title="¡Aviso!", message=mess)
        if request == True:
            self.destroy()  # Con sys.exit() no funciona.

# Inicializador de la App.
def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
