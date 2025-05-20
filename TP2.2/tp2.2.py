import random
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gamma, nbinom, binom, hypergeom, poisson, norm, expon, chisquare

def metodo_rechazo_continuo(f, a, b, M, n):
    muestras = []
    while len(muestras) < n:
        x = random.uniform(a, b)
        y = random.uniform(0, M)
        if y < f(x):
            muestras.append(x)
    return muestras

def metodo_rechazo_discreto(pmf, kmin, kmax, M, n):
    muestras = []
    while len(muestras) < n:
        x = random.randint(kmin, kmax)
        y = random.uniform(0, M)
        if y < pmf(x):
            muestras.append(x)
    return muestras

# Validamos que la ejecución del programa sea correcta
if(len(sys.argv) != 3 or sys.argv[1] != '-d'):
  print("Uso: python tp2.2.py -d <distribucion>")
  sys.exit(1)

distribucion = sys.argv[2]

def generar_nombre_distribucion(distribucion):
    if(distribucion == 'u'):
        return 'Distribución Uniforme'
    elif(distribucion == 'e'):
        return 'Distribución Exponencial'
    elif(distribucion == 'n'):
        return 'Distribución Normal'
    elif(distribucion == 'g'):
        return 'Distribución Gamma'
    elif(distribucion == 'p'):
        return 'Distribución Pascal'
    elif(distribucion == 'b'):
        return 'Distribución Binomial'
    elif(distribucion == 'h'):
        return 'Distribución Hipergeométrica'
    elif(distribucion == 'po'):
        return 'Distribución Poisson'
    elif(distribucion == 'ed'):
        return 'Distribución Empírica Discreta'

nombre_distribucion = generar_nombre_distribucion(distribucion)

print(distribucion)

if(distribucion != 'u' and distribucion != 'e' and distribucion != 'n' and distribucion != 'g' and distribucion != 'p' and distribucion != 'b' and distribucion != 'h' and distribucion != 'po' and distribucion != 'ed'):
    print('Las distribuciones posibles son: u (uniforme), e (exponencial), n (normal), g (gamma), p (pascal), b (binomial), h (hipergeometrica), po (poisson) y ed (empírica discreta)')
    sys.exit(1)

def generar_valores(distribucion):
  valores = []
  if(distribucion == 'u'):
    #Distribución Uniforme
    
    def uniforme(a, b):
      u = random.random()  # U ~ Uniforme(0,1)
      x = a + u * (b - a)  # Inversa
      return x
    
    # Parámetros
    a, b = 0, 1
    n = 2**16

    resultados_uniforme  = [uniforme(a, b) for _ in range(n)]
    valores.extend(resultados_uniforme)

    # Visualización

    plt.hist(resultados_uniforme, bins=100, density=True, alpha=0.6, label='Muestras (inversa)')

    plt.plot([a, b], [1/(b-a), 1/(b-a)], 'r-', label='Densidad uniforme teórica')
    plt.legend()
    plt.title('Distribución uniforme (inversa)')
    plt.xlabel('x')
    plt.ylabel('Densidad')
    plt.show()

  elif(distribucion == 'e'):
    # Distribución Exponencial

    lambd = 1  # Tasa
    n = 2**16    # Cantidad de muestras

    u = np.random.rand(n)

    resultados_exponencial = -np.log(u) / lambd

    x = np.linspace(0, np.max(resultados_exponencial), 2**16)
    pdf = lambd * np.exp(-lambd * x)

    plt.figure(figsize=(10, 6))
    plt.hist(resultados_exponencial, bins=50, density=True, alpha=0.6, color='orange', label='Muestras generadas')
    plt.plot(x, pdf, 'r-', label='Distribución exponencial teórica')
    plt.title('Generador de números pseudoaleatorios - Distribución Exponencial\n(método de la función inversa)')
    plt.xlabel('Valor')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(True)
    plt.show()
    valores.extend(resultados_exponencial)

  elif(distribucion == 'n'):
    
    # Distribución Normal
    mu = 0       # media
    sigma = 1    # desviación estándar
    n = 2**16    # cantidad de números aleatorios

    u = np.random.rand(n)

    normal_samples = norm.ppf(u, loc=mu, scale=sigma)

    x = np.linspace(-4, 4, 2**16)
    pdf = norm.pdf(x, mu, sigma)

    plt.figure(figsize=(10, 6))
    plt.hist(normal_samples, bins=50, density=True, alpha=0.6, color='skyblue', label='Muestras generadas')
    plt.plot(x, pdf, 'r-', label='Distribución normal teórica')
    plt.title('Generador de números pseudoaleatorios con distribución normal\n(método de la función inversa)')
    plt.xlabel('Valor')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(True)
    plt.show()
    valores.extend(normal_samples)

  elif(distribucion == 'g'):
    # Distribución Gamma
    def funcion_densidad_gamma(x, k=2, theta=2):
      return gamma.pdf(x, a=k, scale=theta)

    a, b = 0, 15 #REVISAR
    k, theta = 2, 3
    M = funcion_densidad_gamma((k-1)*theta, k, theta) 
    n = 2**16
    muestras_gamma = metodo_rechazo_continuo(lambda x: funcion_densidad_gamma(x, k, theta), a, b, M, n)

    plt.hist(muestras_gamma, bins=30, density=True, alpha=0.6, label='Gamma')
    x = np.linspace(a, b, 200)
    plt.plot(x, funcion_densidad_gamma(x, k, theta), 'r-', label='Gamma PDF')
    plt.legend()
    plt.title("Gamma")
    plt.show()
    valores.extend(muestras_gamma)

  elif(distribucion == 'p'):
    # Distribución Pascal
    def funcion_pmf_pascal(k, r=5, p=0.4):
      return nbinom.pmf(k, r, p)

    r, p = 5, 0.4
    kmin, kmax = 0, 30
    M = max([funcion_pmf_pascal(k, r, p) for k in range(kmin, kmax+1)])
    n = 2**16
    muestras_pascal = metodo_rechazo_discreto(lambda k: funcion_pmf_pascal(k, r, p), kmin, kmax, M, n)

    plt.hist(muestras_pascal, bins=range(kmin, kmax+2), density=True, alpha=0.6, label='Pascal')
    x = np.arange(kmin, kmax+1)
    plt.plot(x, [funcion_pmf_pascal(k, r, p) for k in x], 'ro', label='Pascal PMF')
    plt.legend()
    plt.title("Pascal (Neg. Binomial)")
    plt.show()
    valores.extend(muestras_pascal)

  elif(distribucion == 'b'):
    # Distribución Binomial

    def funcion_pmf_binomial(k, n=10, p=0.5):
      return binom.pmf(k, n, p)

    n_bin, p_bin = 10, 0.5
    kmin, kmax = 0, n_bin
    M = max([funcion_pmf_binomial(k, n_bin, p_bin) for k in range(kmin, kmax+1)])
    muestras_binomial = metodo_rechazo_discreto(lambda k: funcion_pmf_binomial(k, n_bin, p_bin), kmin, kmax, M, 2**16)

    plt.hist(muestras_binomial, bins=range(kmin, kmax+2), density=True, alpha=0.6, label='Binomial')
    x = np.arange(kmin, kmax+1)
    plt.plot(x, [funcion_pmf_binomial(k, n_bin, p_bin) for k in x], 'ro', label='Binomial PMF')
    plt.legend()
    plt.title("Binomial")
    plt.show()
    valores.extend(muestras_binomial)

  elif(distribucion == 'h'):

    # Distribución Hipergeométrica
    def funcion_hipergeometrica_pmf(k, N=50, K=10, n=5):
      return hypergeom.pmf(k, N, K, n)

    N, K, n_hip = 50, 10, 5
    kmin, kmax = max(0, n_hip+K-N), min(n_hip, K)
    M = max([funcion_hipergeometrica_pmf(k, N, K, n_hip) for k in range(kmin, kmax+1)])
    muestras_hipergeom = metodo_rechazo_discreto(lambda k: funcion_hipergeometrica_pmf(k, N, K, n_hip), kmin, kmax, M, 2**16)

    plt.hist(muestras_hipergeom, bins=range(kmin, kmax+2), density=True, alpha=0.6, label='Hipergeométrica')
    x = np.arange(kmin, kmax+1)
    plt.plot(x, [funcion_hipergeometrica_pmf(k, N, K, n_hip) for k in x], 'ro', label='Hipergeométrica PMF')
    plt.legend()
    plt.title("Hipergeométrica")
    plt.show()
    valores.extend(muestras_hipergeom)

  elif(distribucion == 'po'):

    # Distribución Poisson
    def funcion_poisson_pmf(k, mu=3):
      return poisson.pmf(k, mu)

    mu = 3
    kmin, kmax = 0, 12
    M = max([funcion_poisson_pmf(k, mu) for k in range(kmin, kmax+1)])
    muestras_poisson = metodo_rechazo_discreto(lambda k: funcion_poisson_pmf(k, mu), kmin, kmax, M, 2**16)

    plt.hist(muestras_poisson, bins=range(kmin, kmax+2), density=True, alpha=0.6, label='Poisson')
    x = np.arange(kmin, kmax+1)
    plt.plot(x, [funcion_poisson_pmf(k, mu) for k in x], 'ro', label='Poisson PMF')
    plt.legend()
    plt.title("Poisson")
    plt.show()
    valores.extend(muestras_poisson)

  elif(distribucion == 'ed'):
    # Distribución Empírica Discreta
    valores_empirica = [1, 2, 3]
    probs_empirica = [0.2, 0.5, 0.3]
    def funcion_empirica_discreta_pmf(k):
      return probs_empirica[valores_empirica.index(k)] if k in valores_empirica else 0

    kmin, kmax = min(valores_empirica), max(valores_empirica)
    M = max(probs_empirica)
    muestras_empirica = metodo_rechazo_discreto(funcion_empirica_discreta_pmf, kmin, kmax, M, 2**16)

    plt.hist(muestras_empirica, bins=np.arange(kmin, kmax+2)-0.5, density=True, alpha=0.6, label='Empírica')
    x = np.array(valores_empirica)
    plt.plot(x, [funcion_empirica_discreta_pmf(k) for k in x], 'ro', label='Empírica PMF')
    plt.legend()
    plt.title("Empírica Discreta")
    plt.show()
    valores.extend(muestras_empirica)
  return valores

numeros_aleatorios = generar_valores(distribucion)

def evaluar_test(resultado):
   if(resultado < 0.01):
      return "FALSE"
   else:
      return "TRUE"

## Funciones para los tests

def generar_valor_binario(n):
  if isinstance(n, float):
    n = int(n * 1e6)  # Escala y trunca, puedes ajustar el factor
  n = str(bin(n)) 
  n = n.split('b')
  n = n[1]

  sum = 0
  for i in range(len(n)):
    sum += int(n[i])
   
  bin_final = 0 if (sum % 2) == 0 else 1
   
  return bin_final


#test frecuencia 
def test_frecuencia_bloque(valores, tamanio_bloque): 
    # Convertir la secuencia a bits (0s y 1s)
    #secuencia_bits = [int(bin(x)[-1]) for x in valores]  # Tomar el último bit de cada número
    secuencia_bits = [generar_valor_binario(x) for x in valores] # El bit generado depende de la paridad de 1's

    # Dividir la secuencia en bloques
    cant_bloques = len(secuencia_bits) // tamanio_bloque
    if cant_bloques == 0:
        raise ValueError("El tamaño de los bloques es mayor que la longitud de la secuencia.")
    
    bloques = np.array_split(secuencia_bits[:cant_bloques * tamanio_bloque], cant_bloques)

    # Calcular la frecuencia de 1s en cada bloque
    frecuencia_observada = [np.sum(block) for block in bloques]
    valor_frecuencia_esperada = 0.5 * tamanio_bloque # Frecuencia esperada de 1s en un generador aleatorio
    
    # Asegurar que las sumas coincidan
    suma_observada = sum(frecuencia_observada)
    suma_esperada = valor_frecuencia_esperada * cant_bloques
    if not np.isclose(suma_observada, suma_esperada, rtol=1e-8):
        ajuste = suma_observada / suma_esperada
        valor_frecuencia_esperada *= ajuste

    frecuencia_esperada = [valor_frecuencia_esperada] * cant_bloques

    chi_stat, p_value = chisquare(frecuencia_observada, f_exp=frecuencia_esperada)

    return p_value

#Tesd suma acumulada
def test_suma_acumulada(valores):
   
   # Convertir la secuencia a bits (0s y 1s)
    #secuencia_bits = [int(bin(x)[-1]) for x in valores]  # Tomar el último bit de cada número
    secuencia_bits = [generar_valor_binario(x) for x in valores] # El bit generado depende de la paridad de 1's

    # Transformar los bits: 0 -> -1, 1 -> +1
    secuencia_transformada = [1 if bit == 1 else -1 for bit in secuencia_bits]

    # Calcular la suma acumulativa
    suma_acumulada = np.cumsum(secuencia_transformada)

    # Calcular la desviación máxima
    desvio_maximo = np.max(np.abs(suma_acumulada))

    # Calcular el p-value usando la fórmula del test cusum
    n = len(secuencia_bits)
    p_value = 2 * (1 - norm.cdf(desvio_maximo / np.sqrt(n)))

    return p_value

## Funciones para los tests

resultados_test_frecuencia = test_frecuencia_bloque(numeros_aleatorios, 2**7)

resultado_test_suma_acumulada = test_suma_acumulada(numeros_aleatorios)

def mostrar_resultados_en_tabla(resultados_tests):

    fig, ax = plt.subplots(figsize=(12.5, len(resultados_tests) * 0.5))
    ax.axis('tight')
    ax.axis('off')

    # Crear la tabla
    tabla = plt.table(cellText=[resultados_tests],
                      colLabels=["Distribución", "Test1: Frecuencia(bloques)", "Test2: Suma Acumulada"],
                      loc='center',
                      cellLoc='center')

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.auto_set_column_width(col=list(range(len(resultados_tests[0]))))

    plt.show()

datos_distribucion = [generar_nombre_distribucion(distribucion), evaluar_test(resultados_test_frecuencia), evaluar_test(resultado_test_suma_acumulada)]

mostrar_resultados_en_tabla(datos_distribucion)