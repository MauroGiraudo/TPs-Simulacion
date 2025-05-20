import random
import matplotlib.pyplot as plt
import numpy as np

def f(x):
    # Ejemplo: densidad triangular en [0, 1], f(x) = 2x
    return 2 * x if 0 <= x <= 1 else 0

def rejection_sampling(f, a, b, M, n):
    muestras = []
    while len(muestras) < n:
        x = random.uniform(a, b)
        y = random.uniform(0, M)
        if y < f(x):
            muestras.append(x)
    return muestras

def uniforme(a, b):
    u = random.random()  # U ~ Uniforme(0,1)
    x = a + u * (b - a)  # Inversa de la CDF
    return x

# Parámetros
a, b = 0, 1
M = 2 * b  # Máximo de f(x) en [0,1] para f(x)=2x
n = 100000

muestras1 = rejection_sampling(f, a, b, M, n)

muestras2  = [uniforme(a, b) for _ in range(n)]

# Visualización

plt.hist(muestras1, bins=100, density=True, alpha=0.6, label='Muestras')
x = np.linspace(a, b, 100)
plt.plot(x, [f(xi) for xi in x], 'r-', label='f(x)')
plt.legend()
plt.show()

plt.hist(muestras2, bins=100, density=True, alpha=0.6, label='Muestras (inversa)')

plt.plot([a, b], [1/(b-a), 1/(b-a)], 'r-', label='Densidad uniforme teórica')
plt.legend()
plt.title('Distribución uniforme (inversa)')
plt.xlabel('x')
plt.ylabel('Densidad')
plt.show()