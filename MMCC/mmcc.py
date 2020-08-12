# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 18:20:00 2020

@author: http://research.iac.es/sieinvens/python-course/source/scipy.html
"""

"""Ejemplo de Ajuste de funciones generales con MMCC con Python"""

"""import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import leastsq

# Datos de laboratorio
datos_y = np.array([ 2.9, 6.1, 10.9, 12.8, 19.2])
datos_x = np.array([ 1.0, 2.0, 3.0, 4.0, 5.0])

# Función para calcular los residuos, donde
# se calcula (datos - modelo)
def residuos(p, y, x):
    error  = y - (p[0]*x + p[1])
    return error

# Parámetros iniciales estimados
# y = p0[0]*x  + p0[0]

p0 = [2.0, 0.0]

# Hacemos  el ajuste por minimos cuadrados con leastsq(). El primer parámetro
# es la funcion de residuos, luego los parámetro iniciales y una tupla con los
# argumentos de la funcion de residuos, en este caso, datos_y y datos_x en
# ese orden, porque así se definió la función de error
ajuste = leastsq(residuos, p0, args=(datos_y, datos_x))

# El resultado es una lista, cuyo primer elemento es otra
# lista con los parámetros del ajuste
print(ajuste[0])
# array([ 3.93, -1.41])"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import leastsq
from scipy import random

# Generamos unos datos artificiales para hacer el ejemplo
# A datos_y se le añade "ruido" que simula error de
# medida, añadiendole un valor aleatorio
datos_x = np.arange(0, 0.1, 0.003)
A, k, theta = 10.0, 33.3, np.pi/5.0
y_real = A*np.sin(2*np.pi*k*datos_x + theta)
datos_y = y_real + 2*random.randn(len(datos_x))

# Ahora se trata de ajustar estos datos una función
# modelo tipo senoidal A*sin(2*pi*k*x + theta)

# Defino la funcion de residuos
def residuos(p, y, x):
    A, k, theta = p
    error = y - A*np.sin(2*np.pi*k*x + theta)
    return error

# Parámetros iniciales
# y = p[0]*np.sin(2*np.pi*p[1]*x + p[2])
# Si estos se alejan mucho del valor real
# la solución no convergerá
p0 = [8.0, 40.0, np.pi/3]

# hacemos  el ajuste por minimos cuadrados
ajuste = leastsq(residuos, p0, args=(datos_y, datos_x))

# El resultado es una lista, cuyo primer elemento es otra
# lista con los parámetros del ajuste.
print(ajuste[0])
# array([ -9.787095  ,  32.91201348,  -2.3390355 ]

# Ahora muestro los datos y el ajuste gráficamente

plt.plot(datos_x, datos_y, 'o')  # datos

# Defino la funcion modelo, para representarla gráficamente
def funcion(x, p):
    return p[0]*np.sin(2*np.pi*p[1]*x + p[2])

# genero datos a partir del modelo para representarlo
x1 = np.arange(0, datos_x.max(), 0.001)  # array con muchos puntos de x
y1 = funcion(x1, ajuste[0])           # valor de la funcion modelo en los x

plt.plot(x1, y1, 'r-')
plt.xlabel('Eje X')
plt.ylabel('Eje Y')
plt.title('Ajuste de funcion seno con leastsq')
plt.legend(('Datos', 'Ajuste lineal'))
plt.show()
