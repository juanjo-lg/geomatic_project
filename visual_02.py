# -*- coding: utf-8 -*-
"""
Created on Wen Aug 05 12:17:00 2020

@author: Juanjo_LG
"""

"""GUI para la aplicación de topografía para el TFG OOP (v.02)."""

import textwrap # Módulo para dar formato a texto y quitarle la sangría.
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# Clase App que hereda de tk.Tk()
class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()
        # Listas provisionales de apoyo.
        self.splitters = ["espacio","tabulador","coma","punto y coma"]
        self.file_opened = []
        self.item_to_show = []
        self.config_root()
        #self.config_menu()
        self.config_frames()
        self.draw_canvas(self.fr_canvas)
        self.draw_note(self.fr_note)
        self.draw_table(self.fr_table)
        # El evento de cerrar desde el aspa se conecta con la función cerrar.
        self.protocol("WM_DELETE_WINDOW", self.close)
        # Enlace de los eventos con los atajos.
        self.bind('<Control-q>', self.close)  # Siempre funciona enlazado con la raiz.
    def config_root(self):
        # Configuración de ventana principal.
        self.title("TFG - Juan José Lorenzo Gutiérrez")
        self.screen_size = self.winfo_screenwidth(),self.winfo_screenheight()
        self.geometry("%dx%d+%d-%d" %
            (self.screen_size[0], self.screen_size[1]-70, -10, 30))
        self.configure(background="gray60")
    def config_menu(self):
        # Configuración de barra de menu.
        # Creación de menu.
        self.menubar = tk.Menu()
        self.menu_file = tk.Menu(tearoff=0)
        self.menu_calc = tk.Menu(tearoff=0)
        self.menu_about = tk.Menu(tearoff=0)
        # Casillas de menu.
        self.menu_file.add_command(label="Abrir", accelerator="Ctrl+O",
            command='')
        self.menu_file.add_command(label="Salir", accelerator="Ctrl+Q",
            command=self.close)
        self.menu_calc.add_command(label="Transformation")
        self.menu_about.add_command(label="Acerca de", command='')
        # Cascadas de menu.
        self.menubar.add_cascade(label="Archivo", menu=self.menu_file)
        self.menubar.add_cascade(label="Cálculo", menu=self.menu_calc)
        self.menubar.add_cascade(label="Info", menu=self.menu_about)
        # Enlace del menu con root.
        self.config(menu=self.menubar)
    def config_frames(self):
        # Configuración de los Frames de la App.
        self.fr_canvas = tk.Frame(width=self.screen_size[0]/2)
        self.fr_note = tk.Frame()
        self.fr_table = tk.Frame(bg='gray38',width=self.screen_size[0]/2,
            height=self.screen_size[1]/4)
        # Colocación de Frames.
        self.fr_canvas.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
        self.fr_note.pack(side=tk.TOP,fill=tk.Y)
        self.fr_table.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
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
            width=int(self.screen_size[0]/2),
            height=int(self.screen_size[1]/12))
        # Funciones para crear distintas pestañas.
        def file(event=None):
            self.fr_file = ttk.Frame(master,style='TFrame')
            # Botón para abrir archivos.
            # Imagen para botón "abrir".
            self.img_open = tk.PhotoImage(file="images/carpeta_3.png")
            self.btn_open = tk.Button(
                self.fr_file,image=self.img_open,text='Abrir',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                width=80,bg="grey60",command=self.open_file,
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
                width=80,bg="grey60",
                command=lambda:print(type(self.notebook.tabs())),
                relief=tk.FLAT)
            self.btn_save.pack(side=tk.LEFT)
            # Botón para abrir base de datos.
            # Imagen para botón "base de datos".
            self.img_db = tk.PhotoImage(file="images/base-de-datos_2.png")
            self.btn_db = tk.Button(
                self.fr_file,image=self.img_db,text='DB',
                compound=tk.TOP,
                height=int(self.screen_size[1]/12),
                width=80,bg="grey60",command=self.draw_points,
                relief=tk.FLAT)
            self.btn_db.pack(side=tk.LEFT)
            # Botón para filtrar puntos.
            # Imagen para botón "Filtrar".
            self.img_filter = tk.PhotoImage(file="images/filtrar.png")
            self.btn_filter = tk.Button(
                self.fr_file,image=self.img_filter,text='Filtrar',
                compound=tk.TOP,command=self.draw_all,
                height=int(self.screen_size[1]/12),
                width=80,bg="grey60",
                relief=tk.FLAT)
            self.btn_filter.pack(side=tk.LEFT)
            # Botón para Cálculo de estadísticas.
            # Imagen para botón "Estadísticas".
            self.img_stat = tk.PhotoImage(file="images/estadistica.png")
            self.btn_stat = tk.Button(
                self.fr_file,image=self.img_stat,text='Estadística',
                compound=tk.TOP,
                height=int(self.screen_size[1]/12),
                width=80,bg="grey60",
                relief=tk.FLAT)
            self.btn_stat.pack(side=tk.LEFT)
            # Botón para cerrar el programa.
            # Imagen para botón "cerrar".
            self.img_close = tk.PhotoImage(file="images/cerrar_ico_2.png")
            self.btn_close = tk.Button(
                self.fr_file,image=self.img_close,text='Cerrar',
                compound=tk.TOP,command=self.close,
                height=int(self.screen_size[1]/12),
                width=80,bg="grey60",
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
                width=80,bg="grey60",
                relief=tk.FLAT)
            self.btn_dist_azim.pack(side=tk.LEFT)
            # Botón de transformación.
            # Imagen para botón "Transformación".
            self.img_trans = tk.PhotoImage(file="images/global.png")
            self.btn_trans = tk.Button(
                self.fr_calc,image=self.img_trans,text='Transformación',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                width=80,bg="grey60",
                relief=tk.FLAT)
            self.btn_trans.pack(side=tk.LEFT)
            self.notebook.add(self.fr_calc,text="Cálculos")
            # Botón de Intersección.
            # Imagen para botón "Intersección".
            self.img_inter = tk.PhotoImage(file="images/mercado.png")
            self.btn_inter = tk.Button(
                self.fr_calc,image=self.img_inter,text='Intersección',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                width=80,bg="grey60",
                relief=tk.FLAT)
            self.btn_inter.pack(side=tk.LEFT)
            self.notebook.add(self.fr_calc,text="Cálculos")
            # Botón de poligonal.
            # Imagen para botón "Itinerario".
            self.img_polig = tk.PhotoImage(file="images/mapa.png")
            self.btn_polig = tk.Button(
                self.fr_calc,image=self.img_polig,text='Itinerario',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                width=80,bg="grey60",
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
                width=80,bg="grey60",command=self.show_info,
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
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.ax = self.fig.add_subplot(1,1,1)
        self.ax.set_xlabel('Coordenadas X')
        self.ax.set_ylabel('Coordenadas Y')
        # Prueba con dos puntos
        #self.ax.scatter([353342.2613,200],[4610774.0014,200])
        #self.ax.set_xticks(range(75,125))
        # Prueba para mostrar los dos puntos.
        #self.ax.set_yticks(range(198,202,1))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas,master)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
    def draw_table(self,master):
        # Configuracioón de la tabla de puntos.
        # Label para la tabla.
        self.lbl_table = tk.Label(master,text="Puntos",bg='gray38',fg="gray75")
        self.lbl_table.pack()
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
        self.table.column("#0", width=150, minwidth=100, stretch=tk.NO)
        self.table.column("1", width=100, minwidth=40, stretch=tk.NO)
        self.table.column("2", width=130, minwidth=50, stretch=tk.NO)
        self.table.column("3", width=130, minwidth=50, stretch=tk.NO)
        self.table.column("4", width=130, minwidth=50, stretch=tk.NO)
        self.table.column("5", width=130, minwidth=50, stretch=tk.NO)
        self.table.heading("#0", text="Archivo")
        self.table.heading("1", text="Número")
        self.table.heading("2", text="X")
        self.table.heading("3", text="Y")
        self.table.heading("4", text="Z")
        self.table.heading("5", text="Código")
        # Configuración de estilo del Treeview.
        self.style.configure('Treeview.Heading',
            relief=tk.FLAT,background="gray75")
        self.style.configure('Treeview',background="grey60",
            focuscolor=self.style.configure(".")["background"])
        """NO FUNCIONA FOCUSCOLOR EN ESTA OCASIÓN"""
    def show_info(self, event=None):
        mess = 'Autor: Juan José Lorenzo Gutiérrez\n'\
        'Mail: juanjolorenzogutierrez@gmail.com\n\n'\
        'Proyecto desarrollado con Python 3x y Tkinter para el TFG del curso'\
        ' de adaptación al Grado de Geomática y Topografía.\n\n'\
        'Iconos obtenidos de:\n- Smashicons\n- Freepik\n- Google'
        msgbox_info=messagebox.showinfo(title='Acerca de:',message=mess)
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

                            x_sum += float(line[1])
                            y_sum += float(line[2])
                            #Posible fallo en count, podría ser count-1
                            #No funciona bien, hay que arreglarlo para añadir la media al final de la lista
                            count += 1
                        self.file_opened.append((x_sum/count, y_sum/count))
                        print(self.file_opened[0])
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
    def draw_points(self, event=None):
        # Función que dibuja los puntos con sus coordenadas en el canvas.
        self.table_item = self.table.focus()
        self.item_data = self.table.item(self.table_item,option="values")
        self.ax.scatter(float(self.item_data[1]),float(self.item_data[2]))
        self.canvas.draw()
    def draw_all(self, event=None):
        # Forma de iterar entre todos los subelementos de un parent en Treeview.
        for children in self.table.get_children():
            child = self.table.get_children(children)
            self.table.selection_add(child)# Selecciona todos los items.
        table_items = self.table.selection()
        """EUREKA!!!! AUNQUE HAY QUE DARLE UNA VUELTA DE TUERCA PORQUE TARDA
        MUCHO EN DIBUJAR LOS PUNTOS."""
        for item in table_items:
            item_data=self.table.item(item,option="values")
            # print(item_data)
            self.ax.plot(float(item_data[1]),float(item_data[2]),
            color="black",marker=".")
            self.canvas.draw()
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
