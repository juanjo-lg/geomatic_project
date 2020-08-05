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
        self.file_opened = []
        self.item_to_show = []
        self.config_root()
        self.config_menu()
        self.config_frames()
        self.btn = tk.Button(text = "Cerrar", command = self.close)
        self.btn.pack()
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
        self.fr_canvas = tk.Frame()
        self.fr_table = tk.Frame(bg='gray38')
        self.fr_note = tk.Frame()
        # Colocación de Frames.
        self.fr_canvas.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
        self.fr_table.pack(side=tk.TOP,fill=tk.Y)
        self.fr_note.pack(fill=tk.BOTH)
        def draw_canvas():
            # Configuración de canvas.
            self.fig = Figure(figsize=(5,5), dpi=100)
            self.ax = self.fig.add_subplot(1,1,1)
            self.ax.set_xlabel('Coordenadas X')
            self.ax.set_ylabel('Coordenadas Y')
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.fr_canvas)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(
                side=tk.LEFT, fill=tk.BOTH, expand = 1)
        # Inicialización de canvas.
        draw_canvas()
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
