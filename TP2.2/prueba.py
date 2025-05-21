# PROBÁ EL TEST DE CHI CUADRADO PARA VER SI FUNCIONA CORRECTAMENTE
# AJUSTÁ EL TAMAÑO DE LA TABLA GENERADA
# TERMINÁ CON LOS CHICOS EL INFORME

import random
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gamma, nbinom, binom, hypergeom, poisson, norm, expon, chisquare, kstest

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
    # Distribución Gamma (función inversa)
    k, theta = 2, 3
    n = 2**16
    u = np.random.rand(n)
    muestras_gamma = gamma.ppf(u, a=k, scale=theta)
    valores.extend(muestras_gamma)

    x = np.linspace(0, np.max(muestras_gamma), 200)
    plt.hist(muestras_gamma, bins=30, density=True, alpha=0.6, label='Muestras (inversa)')
    plt.plot(x, gamma.pdf(x, a=k, scale=theta), 'r-', label='Gamma PDF teórica')
    plt.legend()
    plt.title("Gamma (Función inversa)")
    plt.xlabel('x')
    plt.ylabel('Densidad')
    plt.show()
    valores.extend(muestras_gamma)

  elif(distribucion == 'p'):
    # Distribución Pascal
    r, p_pascal = 5, 0.4
    n = 2**16
    u = np.random.rand(n)
    muestras_pascal = nbinom.ppf(u, r, p_pascal)
    valores.extend(muestras_pascal)

    x = np.arange(0, np.max(muestras_pascal)+1)
    plt.hist(muestras_pascal, bins=range(0, int(np.max(muestras_pascal))+2), density=True, alpha=0.6, label='Muestras (inversa)')
    plt.plot(x, nbinom.pmf(x, r, p_pascal), 'ro', label='Pascal PMF teórica')
    plt.legend()
    plt.title("Pascal (Función inversa)")
    plt.xlabel('k')
    plt.ylabel('Probabilidad')
    plt.show()
    valores.extend(muestras_pascal)

  elif(distribucion == 'b'):
    # Distribución Binomial
    n_bin, p_bin = 10, 0.5
    n = 2**16
    u = np.random.rand(n)
    muestras_binomial = binom.ppf(u, n_bin, p_bin)
    valores.extend(muestras_binomial)

    x = np.arange(0, n_bin+1)
    plt.hist(muestras_binomial, bins=range(0, n_bin+2), density=True, alpha=0.6, label='Muestras (inversa)')
    plt.plot(x, binom.pmf(x, n_bin, p_bin), 'ro', label='Binomial PMF teórica')
    plt.legend()
    plt.title("Binomial (Función inversa)")
    plt.xlabel('k')
    plt.ylabel('Probabilidad')
    plt.show()
    valores.extend(muestras_binomial)

  elif(distribucion == 'h'):

    # Distribución Hipergeométrica
    N, K, n_hip = 50, 10, 5
    n = 2**16
    u = np.random.rand(n)
    muestras_hipergeom = hypergeom.ppf(u, N, K, n_hip)
    valores.extend(muestras_hipergeom)

    kmin, kmax = max(0, n_hip+K-N), min(n_hip, K)
    x = np.arange(kmin, kmax+1)
    plt.hist(muestras_hipergeom, bins=range(kmin, kmax+2), density=True, alpha=0.6, label='Muestras (inversa)')
    plt.plot(x, hypergeom.pmf(x, N, K, n_hip), 'ro', label='Hipergeométrica PMF teórica')
    plt.legend()
    plt.title("Hipergeométrica (Función inversa)")
    plt.xlabel('k')
    plt.ylabel('Probabilidad')
    plt.show()
    valores.extend(muestras_hipergeom)

  elif(distribucion == 'po'):

    # Distribución Poisson
    mu = 3
    n = 2**16
    u = np.random.rand(n)
    muestras_poisson = poisson.ppf(u, mu)
    valores.extend(muestras_poisson)

    x = np.arange(0, np.max(muestras_poisson)+1)
    plt.hist(muestras_poisson, bins=range(0, int(np.max(muestras_poisson))+2), density=True, alpha=0.6, label='Muestras (inversa)')
    plt.plot(x, poisson.pmf(x, mu), 'ro', label='Poisson PMF teórica')
    plt.legend()
    plt.title("Poisson (Función inversa)")
    plt.xlabel('k')
    plt.ylabel('Probabilidad')
    plt.show()
    valores.extend(muestras_poisson)

  elif(distribucion == 'ed'):
    # Distribución Empírica Discreta
    valores_empirica = [1, 2, 3]
    probs_empirica = [0.2, 0.5, 0.3]
    n = 2**16
    cdf = np.cumsum(probs_empirica)
    u = np.random.rand(n)
    muestras_empirica = []
    for ui in u:
        for i, c in enumerate(cdf):
            if ui < c:
                muestras_empirica.append(valores_empirica[i])
                break
    valores.extend(muestras_empirica)

    x = np.array(valores_empirica)
    plt.hist(muestras_empirica, bins=np.arange(min(x)-0.5, max(x)+1.5), density=True, alpha=0.6, label='Muestras (inversa)')
    plt.plot(x, probs_empirica, 'ro', label='Empírica PMF teórica')
    plt.legend()
    plt.title("Empírica Discreta (Función inversa)")
    plt.xlabel('k')
    plt.ylabel('Probabilidad')
    plt.show()
  return valores

numeros_aleatorios = generar_valores(distribucion)

def evaluar_test(resultado):
   if(resultado == ''):
      return resultado
   elif(resultado < 0.01):
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

#Test suma acumulada
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

def generar_pmf_dist_discretas(distribucion):
    # Devuelve la función PMF, kmin y kmax para el test chi-cuadrado
    if distribucion == 'p':
        # Pascal (binomial negativa)
        r, p_pascal = 5, 0.4
        pmf = lambda k: nbinom.pmf(k, r, p_pascal)
        kmin, kmax = 0, int(nbinom.ppf(0.999, r, p_pascal))
        return pmf, kmin, kmax
    elif distribucion == 'b':
        # Binomial
        n_bin, p_bin = 10, 0.5
        pmf = lambda k: binom.pmf(k, n_bin, p_bin)
        kmin, kmax = 0, n_bin
        return pmf, kmin, kmax
    elif distribucion == 'h':
        # Hipergeométrica
        N, K, n_hip = 50, 10, 5
        pmf = lambda k: hypergeom.pmf(k, N, K, n_hip)
        kmin, kmax = max(0, n_hip+K-N), min(n_hip, K)
        return pmf, kmin, kmax
    elif distribucion == 'po':
        # Poisson
        mu = 3
        pmf = lambda k: poisson.pmf(k, mu)
        kmin, kmax = 0, int(poisson.ppf(0.999, mu))
        return pmf, kmin, kmax
    elif distribucion == 'ed':
        # Empírica Discreta
        valores_empirica = [1, 2, 3]
        probs_empirica = [0.2, 0.5, 0.3]
        pmf = lambda k: probs_empirica[valores_empirica.index(k)] if k in valores_empirica else 0
        kmin, kmax = min(valores_empirica), max(valores_empirica)
        return pmf, kmin, kmax
    else:
        raise ValueError("Distribución discreta no soportada para test chi-cuadrado")

# Test de bondad de ajuste: Chi-cuadrado para distribuciones discretas
def test_chi_cuadrado(valores, pmf, kmin, kmax, bins=None):
    # Contar frecuencias observadas
    if bins is None:
        bins = np.arange(kmin, kmax+2)
    obs, _ = np.histogram(valores, bins=bins)
    # Calcular frecuencias esperadas
    esperadas = [pmf(k) * len(valores) for k in range(kmin, kmax+1)]
    # Eliminar categorías con frecuencia esperada muy baja (<5)
    obs_filtrado = []
    esp_filtrado = []
    for o, e in zip(obs, esperadas):
        if e >= 5:
            obs_filtrado.append(o)
            esp_filtrado.append(e)
    # Normalizar esperadas para que sumen igual que observadas
    suma_obs = sum(obs_filtrado)
    suma_esp = sum(esp_filtrado)
    if suma_esp > 0:
        esp_filtrado = [e * suma_obs / suma_esp for e in esp_filtrado]
    # Test chi-cuadrado
    chi2, p_value = chisquare(obs_filtrado, f_exp=esp_filtrado)
    return p_value

def generar_cdf_dist_continuas(distribucion):
   # Devuelve la función CDF y los parámetros para el test KS
    if distribucion == 'u':
        # Uniforme en [a, b]
        a, b = 0, 1
        return (lambda x, *args: (x - a) / (b - a)), a, b  # CDF manual
    elif distribucion == 'e':
        # Exponencial con lambda=1
        lambd = 1
        return expon.cdf, 0, 1/lambd  # loc=0, scale=1/lambda
    elif distribucion == 'n':
        # Normal estándar
        mu, sigma = 0, 1
        return norm.cdf, mu, sigma
    elif distribucion == 'g':
        # Gamma con k=2, theta=3
        k, theta = 2, 3
        return gamma.cdf, k, 0, theta  # a, loc, scale
    else:
        raise ValueError("Distribución continua no soportada para test KS")

# Test de bondad de ajuste: Kolmogorov-Smirnov para distribuciones continuas
def test_ks(valores, cdf, *params):
    # cdf: función de distribución acumulada teórica (por ejemplo, gamma.cdf)
    # params: parámetros de la distribución
    # kstest espera una función que reciba un solo argumento x
    p_value = kstest(valores, cdf, args=tuple(params)).pvalue
    return p_value

## Funciones para los tests

resultado_test_frecuencia = test_frecuencia_bloque(numeros_aleatorios, 2**7)

resultado_test_suma_acumulada = test_suma_acumulada(numeros_aleatorios)

resultado_test_chi_cuadrado = ''
resultado_test_KS = ''
if(distribucion == 'u' or distribucion == 'e' or distribucion == 'n' or distribucion == 'g'):
   cdf, *params = generar_cdf_dist_continuas(distribucion)
   resultado_test_KS = test_ks(numeros_aleatorios, cdf, *params)
else:
   pmf, kmin, kmax = generar_pmf_dist_discretas(distribucion)
   resultado_test_chi_cuadrado = test_chi_cuadrado(numeros_aleatorios, pmf, kmin, kmax)


def mostrar_resultados_en_tabla(resultados_tests):

    fig, ax = plt.subplots(figsize=(11, len(resultados_tests) * 0.5))
    ax.axis('tight')
    ax.axis('off')

    # Crear la tabla
    tabla = plt.table(cellText=resultados_tests,
                      colLabels=["Distribución", "Test1: Frecuencia(bloques)", "Test2: Suma Acumulada", "Test3: Chi-Cuadrado", "Test4: Kolmogorov-Smirnov"],
                      loc='center',
                      cellLoc='center')

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.auto_set_column_width(col=list(range(len(resultados_tests[0]))))

    plt.show()

datos_distribucion = [generar_nombre_distribucion(distribucion), evaluar_test(resultado_test_frecuencia), evaluar_test(resultado_test_suma_acumulada), evaluar_test(resultado_test_chi_cuadrado), evaluar_test(resultado_test_KS)]
datos = [datos_distribucion]

mostrar_resultados_en_tabla(datos)