import random
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare, norm, chi2
from math import sqrt, isnan, gcd

# Validamos que la ejecución del programa sea correcta
if(len(sys.argv) != 3 or sys.argv[1] != '-s' or sys.argv[3] != 'd'):
  print("Uso: python tp1.py -s <semilla> -d <distribucion>")
  sys.exit(1)

#Distribución Uniforme

def uniforme(a, b):
    u = random.random()  # U ~ Uniforme(0,1)
    x = a + u * (b - a)  # Inversa de la CDF
    return x

# Parámetros
a, b = 0, 1
n = 100000

muestras2  = [uniforme(a, b) for _ in range(n)]

# Visualización

plt.hist(muestras2, bins=100, density=True, alpha=0.6, label='Muestras (inversa)')

plt.plot([a, b], [1/(b-a), 1/(b-a)], 'r-', label='Densidad uniforme teórica')
plt.legend()
plt.title('Distribución uniforme (inversa)')
plt.xlabel('x')
plt.ylabel('Densidad')
plt.show()

# Distribución Exponencial


# Distribución Normal


# Distribución Gamma


# Distribución Pascal


# Distribución Binomial


# Distribución Hipergeométrica


# Distribución Poisson


# Distribución Empírica Discreta

