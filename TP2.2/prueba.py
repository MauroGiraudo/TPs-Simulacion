import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gamma, nbinom, binom, hypergeom, poisson, norm, expon

# --- GAMMA (continua) ---
def funcion_densidad_gamma(x, k=2, theta=2):
    return gamma.pdf(x, a=k, scale=theta)

def metodo_rechazo_continuo(f, a, b, M, n):
    muestras = []
    while len(muestras) < n:
        x = random.uniform(a, b)
        y = random.uniform(0, M)
        if y < f(x):
            muestras.append(x)
    return muestras

# Ejemplo Gamma
a, b = 0, 20
k, theta = 2, 2
M = funcion_densidad_gamma((k-1)*theta, k, theta) 
n = 100000
muestras_gamma = metodo_rechazo_continuo(lambda x: funcion_densidad_gamma(x, k, theta), a, b, M, n)

plt.hist(muestras_gamma, bins=30, density=True, alpha=0.6, label='Gamma')
x = np.linspace(a, b, 200)
plt.plot(x, funcion_densidad_gamma(x, k, theta), 'r-', label='Gamma PDF')
plt.legend()
plt.title("Gamma")
plt.show()

# --- PASCAL (Negative Binomial, discreta) ---
def funcion_pmf_pascal(k, r=5, p=0.4):
    return nbinom.pmf(k, r, p)

def metodo_rechazo_discreto(pmf, kmin, kmax, M, n):
    muestras = []
    while len(muestras) < n:
        x = random.randint(kmin, kmax)
        y = random.uniform(0, M)
        if y < pmf(x):
            muestras.append(x)
    return muestras

# Ejemplo Pascal
r, p = 5, 0.4
kmin, kmax = 0, 30
M = max([funcion_pmf_pascal(k, r, p) for k in range(kmin, kmax+1)])
n = 100000
muestras_pascal = metodo_rechazo_discreto(lambda k: funcion_pmf_pascal(k, r, p), kmin, kmax, M, n)

plt.hist(muestras_pascal, bins=range(kmin, kmax+2), density=True, alpha=0.6, label='Pascal')
x = np.arange(kmin, kmax+1)
plt.plot(x, [funcion_pmf_pascal(k, r, p) for k in x], 'ro', label='Pascal PMF')
plt.legend()
plt.title("Pascal (Neg. Binomial)")
plt.show()

# --- BINOMIAL (discreta) ---
def funcion_pmf_binomial(k, n=10, p=0.5):
    return binom.pmf(k, n, p)

n_bin, p_bin = 10, 0.5
kmin, kmax = 0, n_bin
M = max([funcion_pmf_binomial(k, n_bin, p_bin) for k in range(kmin, kmax+1)])
muestras_binomial = metodo_rechazo_discreto(lambda k: funcion_pmf_binomial(k, n_bin, p_bin), kmin, kmax, M, 100000)

plt.hist(muestras_binomial, bins=range(kmin, kmax+2), density=True, alpha=0.6, label='Binomial')
x = np.arange(kmin, kmax+1)
plt.plot(x, [funcion_pmf_binomial(k, n_bin, p_bin) for k in x], 'ro', label='Binomial PMF')
plt.legend()
plt.title("Binomial")
plt.show()

# --- HIPERGEOMÉTRICA (discreta) ---
def funcion_hipergeometrica_pmf(k, N=50, K=10, n=5):
    return hypergeom.pmf(k, N, K, n)

N, K, n_hip = 50, 10, 5
kmin, kmax = max(0, n_hip+K-N), min(n_hip, K)
M = max([funcion_hipergeometrica_pmf(k, N, K, n_hip) for k in range(kmin, kmax+1)])
muestras_hipergeom = metodo_rechazo_discreto(lambda k: funcion_hipergeometrica_pmf(k, N, K, n_hip), kmin, kmax, M, 100000)

plt.hist(muestras_hipergeom, bins=range(kmin, kmax+2), density=True, alpha=0.6, label='Hipergeométrica')
x = np.arange(kmin, kmax+1)
plt.plot(x, [funcion_hipergeometrica_pmf(k, N, K, n_hip) for k in x], 'ro', label='Hipergeométrica PMF')
plt.legend()
plt.title("Hipergeométrica")
plt.show()

# --- POISSON (discreta) ---
def funcion_poisson_pmf(k, mu=3):
    return poisson.pmf(k, mu)

mu = 3
kmin, kmax = 0, 15
M = max([funcion_poisson_pmf(k, mu) for k in range(kmin, kmax+1)])
muestras_poisson = metodo_rechazo_discreto(lambda k: funcion_poisson_pmf(k, mu), kmin, kmax, M, 100000)

plt.hist(muestras_poisson, bins=range(kmin, kmax+2), density=True, alpha=0.6, label='Poisson')
x = np.arange(kmin, kmax+1)
plt.plot(x, [funcion_poisson_pmf(k, mu) for k in x], 'ro', label='Poisson PMF')
plt.legend()
plt.title("Poisson")
plt.show()

# --- EMPÍRICA DISCRETA ---
# Por ejemplo: valores posibles [1,2,3,4] con probabilidades [0.1, 0.2, 0.3, 0.4]
valores_empirica = [1, 2, 3, 4]
probs_empirica = [0.1, 0.2, 0.3, 0.4]
def funcion_empirica_discreta_pmf(k):
    return probs_empirica[valores_empirica.index(k)] if k in valores_empirica else 0

kmin, kmax = min(valores_empirica), max(valores_empirica)
M = max(probs_empirica)
muestras_empirica = metodo_rechazo_discreto(funcion_empirica_discreta_pmf, kmin, kmax, M, 100000)

plt.hist(muestras_empirica, bins=np.arange(kmin, kmax+2)-0.5, density=True, alpha=0.6, label='Empírica')
x = np.array(valores_empirica)
plt.plot(x, [funcion_empirica_discreta_pmf(k) for k in x], 'ro', label='Empírica PMF')
plt.legend()
plt.title("Empírica Discreta")
plt.show()

# Distribución Normal




