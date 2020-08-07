# -*- coding: utf-8 -*-
"""
Created on Wen Aug 05 12:17:00 2020

@author: Juanjo_LG
"""

"""GUI para la aplicación de topografía para el TFG OOP (v.02)."""

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
        self.config_menu()
        self.config_frames()
        self.draw_canvas(self.fr_canvas)
        self.draw_note(self.fr_note)
        # El evento de cerrar desde el aspa se conecta con la función cerrar.
        self.protocol("WM_DELETE_WINDOW", self.close)
        # Enlace de los eventos con los atajos.
        self.bind('<Control-q>', self.close)  # Siempre funciona enlazado con la raiz.
    def config_root(self):
        # Configuración de ventana principal.
        self.title("TFG - Juan José Lorenzo Gutiérrez")
        self.screen_size = self.winfo_screenwidth(),self.winfo_screenheight()
        self.geometry("%dx%d+%d-%d" %
            (self.screen_size[0], self.screen_size[1]-100, -10, 40))
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
        self.fr_table = tk.Frame(bg='gray38',width=self.screen_size[0]/2)
        # Colocación de Frames.
        self.fr_canvas.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
        self.fr_note.pack(side=tk.TOP,fill=tk.Y)
        self.fr_table.pack(fill=tk.Y)
    def draw_note(self,master):
        # Configuracion del Notebook con estilos de diseño.
        note_style = ttk.Style()
        # De esta forma se quitan los bordes.
        note_style.theme_use('default')
        # 'TNotebook','TNotebook.Tab' y 'TFrame' son estilos de ttk.
        note_style.configure('TNotebook',borderwidth=0)
        # Quita las líneas punteadas de las tablas al seleccionarlas.
        note_style.configure('TNotebook.Tab',borderwidth=0,
            focuscolor=note_style.configure(".")["background"])
        note_style.configure('TFrame',borderwidth=0,background="gray60")
        # Con 'readonly' no salen las palabras enmarcadas.
        note_style.configure('TCombobox',
            selectbackground=[('readonly','white')],
            selectforeground=[('readonly','black')],
            fieldbackground=[('readonly','gray60')])
        # Constructor del Notebook.
        self.notebook = ttk.Notebook(master,style='TNotebook',
            width=int(self.screen_size[0]/2),
            height=int(self.screen_size[1]/12))
        """print(self.screen_size[1]/12)"""
        # Funciones para crear distintas pestañas.
        def file():
            self.fr_file = ttk.Frame(master,style='TFrame')
            # Botón para abrir archivos.
            # Imagen para botón "abrir".
            self.img_abrir = tk.PhotoImage(file="images/carpeta_abrir.png")
            self.btn_open = tk.Button(
                self.fr_file,image=self.img_abrir,text='Abrir',
                compound=tk.TOP,height=int(self.screen_size[1]/12),
                width=80,bg="grey60",
                relief=tk.FLAT)
            self.btn_open.pack(side=tk.LEFT)

            # Frame para separadores.
            self.fr_separator = ttk.Frame(self.fr_file,style='TFrame')
            self.fr_separator.pack(side=tk.LEFT)
            # Etiqueta de separadores.
            self.lbl_separator = tk.Label(self.fr_separator,
                text='Separador de Datos',
                background="gray60", fg="black")
            self.lbl_separator.pack(side=tk.TOP,pady=5)
            # Combobox con los distintos separadores.
            self.cmb_separator = ttk.Combobox(self.fr_separator,values=self.splitters)
            #self.cmb_separator["values"] = self.splitters
            self.cmb_separator.pack(pady=5)
            # Botón para cerrar el programa.
            # Imagen para botón "cerrar".
            self.img_close = tk.PhotoImage(file="images/cerrar_2.png")
            self.btn_close = tk.Button(
                self.fr_file,image=self.img_close,text='Cerrar',
                command=self.close,
                height=int(self.screen_size[1]/12),
                width=80,bg="grey60",
                relief=tk.FLAT)
            self.btn_close.pack(side=tk.LEFT)
            self.notebook.add(self.fr_file,text="Archivo")
        def calculus():
            self.fr_calc = ttk.Frame(master,style='TFrame')
            self.notebook.add(self.fr_calc,text="Cálculos")
        # Inicialización de pestañas file y calculus
        file()
        calculus()
        self.notebook.pack(fill=tk.BOTH,expand=True)
    def draw_canvas(self,master):
        # Configuración de canvas.
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.ax = self.fig.add_subplot(1,1,1)
        self.ax.set_xlabel('Coordenadas X')
        self.ax.set_ylabel('Coordenadas Y')
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
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
