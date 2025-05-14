import random
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare, norm, chi2
from math import sqrt, isnan
from funciones import obtener_numeros_centrales, generar_valor_a, son_coprimos, evaluar_test, generar_valor_binario

# Validamos que la ejecución del programa sea correcta
if(len(sys.argv) != 3 or sys.argv[1] != '-s'):
  print("Uso: python tp1.py -s <semilla>")
  sys.exit(1)

if(len(sys.argv[2]) != 4):
  print("La semilla debe ser un número de 4 dígitos")
  sys.exit(1)

# Definimos las variables globales necesarias 
semilla = int(sys.argv[2])
cantidad_numeros = 2**5 #Altura - Ancho de los bitmaps y sqrt() de la longitud de las secuencias aleatorias
tamanio_bloque = 2**7 # M 

def generador_medios_cuadrados(semilla):
  valores = []
  for i in range (cantidad_numeros**2):
    x = semilla**2
    y = str(x)
    while(len(y) < 8):
      y = '0' + y
    x = int(y)
    semilla = obtener_numeros_centrales(x)
    valores.append(x)
  return valores

def crear_bitmap(resultado, ancho, alto, tipo_generador):
    valores = resultado

    valores_normalizados = [int(v % cantidad_numeros) for v in valores]  # Escalar al rango 0-255

    if len(valores_normalizados) < ancho * alto:
        raise ValueError("No hay suficientes datos para llenar el bitmap.")

    matriz = np.array(valores_normalizados[:ancho * alto]).reshape((alto, ancho))

    plt.imshow(matriz, cmap='gray', interpolation='nearest')
    plt.title(f"Bitmap generado ({tipo_generador})")
    plt.axis('off')
    #plt.imsave(f'bitmap_{tipo_generador}.png', matriz, cmap='gray', format='png')
    plt.show()

# X(n+1) = (a * X(n) + c) % (m)
# Módulo m > 0
# Multiplicador  0 <= a <= m
# Incremento  c <= m
# Semilla  0 <= X(0) <= m

def generador_lineal_congruencial(semilla):
  m = 2**32
  a = generar_valor_a(659) #El valor ingresado debe ser un número entero
  c = 7919
  if(not son_coprimos(c, m)):
    print("El Módulo (m) y el Incremento (c) no son coprimos (divisor máximo = 1 entre si)")
    sys.exit(1)
  valores = []
  for _ in range(cantidad_numeros**2):
    x = (a * semilla + c) % m
    valores.append(x)
    semilla = x
  return valores


def generador_python(semilla):
  random.seed(semilla)
  valores = [random.randint(0, 75000) for _ in range(cantidad_numeros**2)]
  return valores
  
def generador_numpy(semilla):
   np.random.seed(semilla)
   valores = np.random.randint(0, 75000, size=(cantidad_numeros**2))
   return valores.tolist()


# Test de Frecuencia

"""
valores (listado): Secuencia de números generados.
tamanio_bloque (int): Tamaño de los bloques.
"""

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

# Test de Suma Acumulada
"""
valores (listado): Secuencia de números generados.
"""
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

# Test de Mayor Secuencia de 1's
"""
valores (listado): Secuencia de números generados.
tamanio_bloque (int): Tamaño de los bloques.
"""
def test_mayor_secuencia_unos(valores, tamanio_bloque): #Sólo para M = 128
   
  if(tamanio_bloque != 128):
     raise ValueError("El tamaño de los bloques debe ser 128 para este test.")
   
   # Convertir la secuencia a bits (0s y 1s)
  #secuencia_bits = [int(bin(x)[-1]) for x in valores]  # Tomar el último bit de cada número
  secuencia_bits = [generar_valor_binario(x) for x in valores] # El bit generado depende de la paridad de 1's

  # Dividir la secuencia en bloques
  cant_bloques = len(secuencia_bits) // tamanio_bloque
  if cant_bloques == 0:
    raise ValueError("El tamaño de los bloques es mayor que la longitud de la secuencia.")
    
  bloques = np.array_split(secuencia_bits[:cant_bloques * tamanio_bloque], cant_bloques)

  # Calcular la longitud de la secuencia más larga de 1's en cada bloque
  secuencias_maximas = []
  for bloque in bloques:
    secuencia_máxima = 0
    secuencia_actual = 0
    for bit in bloque:
      if bit == 1:
        secuencia_actual += 1
        secuencia_máxima = max(secuencia_máxima, secuencia_actual)
      else:
        secuencia_actual = 0
    secuencias_maximas.append(secuencia_máxima)

  #print(secuencias_maximas)

  # Categorizar las longitudes de las secuencias de 1's
  categorias = [4, 5, 6, 7, 8, 9]  
  conteo_observaciones = [0] * len(categorias)
  for secuencia in secuencias_maximas:
    #print(secuencia)
    for i, categoria in enumerate(categorias):
      if secuencia == categoria:
        conteo_observaciones[i] += 1
        break
      if secuencia > categorias[-1]:
        conteo_observaciones[-1] += 1
        break
      if secuencia < categorias[0]:
        conteo_observaciones[0] += 1
        break

  #print(conteo_observaciones)
  # Frecuencias esperadas (valores teóricos para una secuencia aleatoria) 
  probabilidades_esperadas = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]  
  conteo_esperado = [p * cant_bloques for p in probabilidades_esperadas]

  # Ajustar las frecuencias esperadas si las sumas no coinciden
  suma_observada = sum(conteo_observaciones)
  suma_esperada = sum(conteo_esperado)

  if not np.isclose(suma_observada, suma_esperada, rtol=1e-8):
    ajuste = suma_observada / suma_esperada
    conteo_esperado = [x * ajuste for x in conteo_esperado]

  # Realizar el test chi-cuadrado
  chi_stat, p_value = chisquare(conteo_observaciones, f_exp=conteo_esperado)

  if(isnan(p_value)):
     p_value = 0.001

  return p_value

# Test de Plantillas sin Superposición
"""
sequence (listado): Secuencia de números generados.
template (string): Plantilla binaria a buscar (ej: 101).
block_size (int): Tamaño de los bloques.
"""
def test_plantillas_sin_superposicion(valores, plantilla, tamanio_bloque):
    
    # Convertir la secuencia a bits (0s y 1s)
    #secuencia_bits = ''.join([bin(x)[-1] for x in valores])  # Convertir a cadena binaria
    secuencia_bits = ''.join([str(generar_valor_binario(x)) for x in valores]) # El bit generado depende de la paridad de 1's

    # Dividir la secuencia en bloques
    cant_bloques = len(secuencia_bits) // tamanio_bloque
    if cant_bloques == 0:
        raise ValueError("El tamaño de los bloques es mayor que la longitud de la secuencia.")
    
    bloques = [secuencia_bits[i * tamanio_bloque:(i + 1) * tamanio_bloque] for i in range(cant_bloques)]

    # Contar las apariciones de la plantilla en cada bloque
    longitud_plantilla = len(plantilla)
    valores_observados = []
    for bloque in bloques:
        count = 0
        for i in range(len(bloque) - longitud_plantilla + 1):
            if bloque[i:i + longitud_plantilla] == plantilla:
                count += 1
        valores_observados.append(count)

    #print(observed_counts)
    # Calcular la frecuencia esperada y la varianza
    media_esperada = (tamanio_bloque - longitud_plantilla + 1) * (2 ** -longitud_plantilla)
    varianza_esperada = tamanio_bloque * (2 ** -longitud_plantilla - 2**(-2*longitud_plantilla) * (2 * longitud_plantilla - 1))

    # Calcular el estadístico chi-cuadrado manualmente
    chi_stat = np.sum([(x - media_esperada)**2 / varianza_esperada for x in valores_observados])

    # Calcular el p-value usando la distribución chi-cuadrado
    grados_de_libertad = len(valores_observados)  
    p_value = 1 - chi2.cdf(chi_stat, df=grados_de_libertad)

    return p_value


# Valores aleatorios obtenido con el método de los cuadrados
resultado_medios_cuadrados = generador_medios_cuadrados(semilla)
#print(resultado_medios_cuadrados)

# Mapa de bits donde podemos observar visualmente la distribución de los valores generados
crear_bitmap(resultado_medios_cuadrados, ancho=cantidad_numeros, alto=cantidad_numeros, tipo_generador="medios_cuadrados")

# Resultado Test de Frecuencia
resultado_test_frecuencia1 = test_frecuencia_bloque(resultado_medios_cuadrados, tamanio_bloque)
print(f"F - MC:{resultado_test_frecuencia1}")

# Resultado Test de Suma Acumulada
resultado_test_suma_acumulada1 = test_suma_acumulada(resultado_medios_cuadrados)
print(f"SA - MC:{resultado_test_suma_acumulada1}")

# Resultado Test de Mayor Secuencia de 1's
resultado_test_mayor_secuencia1 = test_mayor_secuencia_unos(resultado_medios_cuadrados, tamanio_bloque)
print(f"MS - MC:{resultado_test_mayor_secuencia1}")

# Resultado Test de Plantillas sin Superposición
resultado_test_plantillas1 = test_plantillas_sin_superposicion(resultado_medios_cuadrados, '100', tamanio_bloque)
print(f"PS - MC:{resultado_test_plantillas1}")



# Valores aleatorios generados con el método GCL
resultado_gcl = generador_lineal_congruencial(semilla)
#print(resultado_gcl)

# Mapa de bits donde podemos observar visualmente la distribución de los valores generados
crear_bitmap(resultado_gcl, ancho=cantidad_numeros, alto=cantidad_numeros, tipo_generador="lineal_congruencial")

# Resultado Test de Frecuencia
resultado_test_frecuencia2 = test_frecuencia_bloque(resultado_gcl, tamanio_bloque)
print(f"F - GCL:{resultado_test_frecuencia2}")

# Resultado Test de Suma Acumulada
resultado_test_suma_acumulada2 = test_suma_acumulada(resultado_gcl)
print(f"SA - GCL:{resultado_test_suma_acumulada2}")

# Resultado Test de Mayor Secuencia de 1's
resultado_test_mayor_secuencia2 = test_mayor_secuencia_unos(resultado_gcl, tamanio_bloque)
print(f"MS - GCL:{resultado_test_mayor_secuencia2}")

# Resultado Test de Plantillas sin Superposición
resultado_test_plantillas2 = test_plantillas_sin_superposicion(resultado_gcl, '100', tamanio_bloque)
print(f"PS - GCL:{resultado_test_plantillas2}")



# Valores aleatorios obtenido con el generador de python
resultado_python = generador_python(semilla)
#print(resultado_python)

# Mapa de bits donde podemos observar visualmente la distribución de los valores generados
crear_bitmap(resultado_python, ancho=cantidad_numeros, alto=cantidad_numeros, tipo_generador="python")

# Resultado Test de Frecuencia
resultado_test_frecuencia3 = test_frecuencia_bloque(resultado_python, tamanio_bloque)
print(f"F - PY:{resultado_test_frecuencia3}")

# Resultado Test de Suma Acumulada
resultado_test_suma_acumulada3 = test_suma_acumulada(resultado_python)
print(f"SA - PY:{resultado_test_suma_acumulada3}")

# Resultado Test de Mayor Secuencia de 1's
resultado_test_mayor_secuencia3 = test_mayor_secuencia_unos(resultado_python, tamanio_bloque)
print(f"MS - PY:{resultado_test_mayor_secuencia3}")

# Resultado Test de Plantillas sin Superposición
resultado_test_plantillas3 = test_plantillas_sin_superposicion(resultado_python, '100', tamanio_bloque)
print(f"PS - PY:{resultado_test_plantillas3}")



# Valores aleatorios obtenido con el generador de numpy
resultado_numpy = generador_numpy(semilla)
#print(resultado_numpy)

# Mapa de bits donde podemos observar visualmente la distribución de los valores generados
crear_bitmap(resultado_numpy, ancho=cantidad_numeros, alto=cantidad_numeros, tipo_generador="numpy")

# Resultado Test de Frecuencia
resultado_test_frecuencia4 = test_frecuencia_bloque(resultado_numpy, tamanio_bloque)
print(f"F - NUMPY:{resultado_test_frecuencia4}")

# Resultado Test de Suma Acumulada
resultado_test_suma_acumulada4 = test_suma_acumulada(resultado_numpy)
print(f"SA - NUMPY:{resultado_test_suma_acumulada4}")

# Resultado Test de Mayor Secuencia de 1's
resultado_test_mayor_secuencia4 = test_mayor_secuencia_unos(resultado_numpy, tamanio_bloque)
print(f"MS - NUMPY:{resultado_test_mayor_secuencia4}")

# Resultado Test de Plantillas sin Superposición
resultado_test_plantillas4 = test_plantillas_sin_superposicion(resultado_numpy, '100', tamanio_bloque)
print(f"PS - NUMPY:{resultado_test_plantillas4}")


# Creación de una tabla donde mostramos los resultados de los tests para los generadores creados
"""
resultados_tests (lista de listas con: nombre del generador y resultados de los tests [5 elementos])
"""
def mostrar_resultados_en_tabla(resultados_tests):

    fig, ax = plt.subplots(figsize=(12.5, len(resultados_tests) * 0.5))
    ax.axis('tight')
    ax.axis('off')

    # Crear la tabla
    tabla = plt.table(cellText=resultados_tests,
                      colLabels=["Generador", "Test1: Frecuencia(bloques)", "Test2: Suma Acumulada", "Test3: Mayor secuencia de 1's", "Test4: Plantillas sin superposición"],
                      loc='center',
                      cellLoc='center')

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.auto_set_column_width(col=list(range(len(resultados_tests[0]))))

    plt.show()

# Tabla donde podemos observar el resultado de los tests ejecutados para ambos generadores
datos_metodo_cuadrados = ["Método de los Cuadrados", evaluar_test(resultado_test_frecuencia1), evaluar_test(resultado_test_suma_acumulada1), evaluar_test(resultado_test_mayor_secuencia1), evaluar_test(resultado_test_plantillas1)]
datos_gcl = ["GCL", evaluar_test(resultado_test_frecuencia2), evaluar_test(resultado_test_suma_acumulada2), evaluar_test(resultado_test_mayor_secuencia2), evaluar_test(resultado_test_plantillas2)]
datos_python = ["Python", evaluar_test(resultado_test_frecuencia3), evaluar_test(resultado_test_suma_acumulada3), evaluar_test(resultado_test_mayor_secuencia3), evaluar_test(resultado_test_plantillas3)]
datos_numpy = ["Numpy", evaluar_test(resultado_test_frecuencia4), evaluar_test(resultado_test_suma_acumulada4), evaluar_test(resultado_test_mayor_secuencia4), evaluar_test(resultado_test_plantillas4)]
datos = [datos_metodo_cuadrados, datos_gcl, datos_python, datos_numpy]
mostrar_resultados_en_tabla(datos)
