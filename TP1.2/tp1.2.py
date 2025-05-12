import random
import sys
import matplotlib.pyplot as plt
#from funciones import convertir_a_color, definir_capital, nuevo_valor_apuesta, generar_secuencia_fibonacci, definir_apuesta_inicial, nuevo_valor_contador_sec_fibonacci, calcular_monto_total_observado, generar_nombre_estrategia, calcular_promedio_apuestas_ganadas, generar_resultado_aleatorio, calcular_frec_bancarrota_observada, calcular_frec_relativa_victoria_observada


def generar_resultado_aleatorio(valor_elegido):
  valores = [0, 1]
  pesos = []
  prob_ganar = round(18/37, 4)
  prob_perder = round(19/37, 4)
  if(valor_elegido == "rojo"):
    pesos.extend([prob_ganar, prob_perder])
  else:
    pesos.extend([prob_perder, prob_ganar])
  return random.choices(valores, pesos, k=1)[0]

def convertir_a_color(resultado):
  if(resultado == 0):
    return "rojo"
  else:
    return "negro"
  


def definir_capital(capital):
  if(capital == "finito"):
    return 2000
  else:
    return 0
  


def generar_secuencia_fibonacci(tiradas):
  secuencia_fibonacci = [5, 5]
  for i in range(2, tiradas):
    secuencia_fibonacci.append(secuencia_fibonacci[i-1] + secuencia_fibonacci[i-2])
  return secuencia_fibonacci

def generar_nombre_estrategia(estrategia):
  if(estrategia == "m"):
    return "Martingala"
  elif(estrategia == "a"):
    return "D'Alembert"
  elif(estrategia == "f"):
    return "Fibonacci"
  else:
    return "Paroli" 

def definir_apuesta_inicial(estrategia):
  if(estrategia == "f"):
    return 5
  else:
    return 10



def nuevo_valor_contador_sec_fibonacci(contador_secuencia_fibonacci, resultado):
  if(resultado == 1):
    if(contador_secuencia_fibonacci - 2 >= 0):
      return contador_secuencia_fibonacci - 2
    else:
      return 0
  else:
    return contador_secuencia_fibonacci + 1



# 0 = Pierde la apuesta | 1 = Gana la apuesta
# 25 = Valor de la apuesta inicial
# D'Alembert:
#   Si gana, se resta 10 a la apuesta (hasta llegar al mínimo)
#   Si pierde, se suma 10 a la apuesta
#Fibonacci:
#   Si gana, se resta 2 a la secuencia de Fibonacci (hasta llegar al mínimo)
#   Si pierde, se suma 1 a la secuencia de Fibonacci 
def nuevo_valor_apuesta(estrategia, valor_minimo_apuesta, resultado_apuesta, valor_apuesta, secuencia_fibonacci, contador_secuencia_fibonacci, contador_paroli):
  if(resultado_apuesta == 1):
    if(estrategia == "m"):
      return valor_minimo_apuesta
    elif(estrategia == "a"):
      if(valor_apuesta - 15 > valor_minimo_apuesta):
        return valor_apuesta - 15
      else:
        return valor_minimo_apuesta
    elif(estrategia == "f"):
      return secuencia_fibonacci[contador_secuencia_fibonacci]
    else:
      if(contador_paroli <= 2):
        return valor_apuesta * 2
      else:
        return valor_minimo_apuesta
  else:
    if(estrategia == "m"):
      return valor_apuesta * 2
    elif(estrategia == "a"):
      return valor_apuesta + 10
    elif(estrategia == "f"):
      return secuencia_fibonacci[contador_secuencia_fibonacci]
    else:
      return valor_minimo_apuesta 
    


def calcular_monto_total_observado(monto_total_corridas, num_corridas, num_tiradas):
  monto_total_observado = []
  for i in range(num_tiradas):
    suma_monto_total_tirada = 0
    for j in range(num_corridas):
      suma_monto_total_tirada += monto_total_corridas[j][i]
    promedio_monto_total_tirada = suma_monto_total_tirada / num_corridas
    monto_total_observado.append(promedio_monto_total_tirada)
  return monto_total_observado


def calcular_frec_relativa_victoria_observada(frec_rel_victoria_corridas):
  frec_relativa_victoria_observada = []
  for i in range(len(frec_rel_victoria_corridas[0])):
    frec_sumada = 0
    for j in range(len(frec_rel_victoria_corridas)):
      frec_sumada += frec_rel_victoria_corridas[j][i]
    promedio_frec = round(frec_sumada / len(frec_rel_victoria_corridas), 4)
    frec_relativa_victoria_observada.append(promedio_frec)
  return frec_relativa_victoria_observada


def calcular_promedio_apuestas_ganadas(resultados_apuestas_corridas):
  resultado_apuestas_observado = []
  suma = 0
  for i in range(len(resultados_apuestas_corridas)):
    suma += resultados_apuestas_corridas[i]
    resultado_apuestas_observado.append(round(suma / (i+1), 0))
  return resultado_apuestas_observado


def calcular_frec_bancarrota_observada(bancarrota_corridas):
  frec_bancarrota_observada = []
  suma = 0
  for i in range(len(bancarrota_corridas)):
    suma += bancarrota_corridas[i]
    frec_bancarrota_observada.append(round(suma / (i+1), 4))
  return frec_bancarrota_observada






# Validamos que la ejecución del programa sea correcta
if(len(sys.argv) != 11 or sys.argv[1] != '-c' or sys.argv[3] != '-n' or sys.argv[5] != '-z' or sys.argv[7] != '-s' or sys.argv[9] != '-a'):
  print("Uso: python tp1.py -c <numero_tiradas> -n <numero_corridas> -z <valor_elegido> -s <estrategia> -a <capital>")
  sys.exit(1)

# Recuperamos los argumentos ingresados por la consola
num_tiradas = int(sys.argv[2])
num_corridas = int(sys.argv[4])
valor_elegido = sys.argv[6]
estrategia_elegida = sys.argv[8]
capital_disponible = sys.argv[10]

# Validamos los argumentos
if(num_tiradas <= 0 or num_corridas <= 0 or (valor_elegido != "rojo" and valor_elegido != "negro") or (estrategia_elegida != "m" and estrategia_elegida != "a" and estrategia_elegida != "f" and estrategia_elegida != "p") or (capital_disponible != "finito" and capital_disponible != "infinito")):
  print("El número de tiradas y corridas debe ser mayor a 0, el valor elegido debe ser [rojo] o [negro], las estrategias son m(Martingala), a(D'Alembert), f(Fibonacci) u p(Paroli) y el capital puede ser finito o infinito")
  sys.exit(1)

valores_corridas = []
capital_inicial = definir_capital(capital_disponible)
promedio_apuestas_para_ganar = round(1/(18/37), 0) #Aprox 2.056, valor que redondeamos a "2"
frecuencia_relativa_victoria_esperada = round(18/37, 4)
monto_total_corridas = []
secuencia_fibonacci = generar_secuencia_fibonacci(num_tiradas)

#Se utilizará para mostrar el promedio de apuestas que deben realizarse para lograr ganar una de ellas (respecto del total de ejecuciones / corridas de la experiencia)
resultados_apuestas_corridas = [] 

#Lista global donde se almacenará el total de bancarrotas ocurridas durante las experiencias
bancarrotas_corridas = []

#Lista global donde se almacenará la frecuencia relativa de apuestas ganadas durante las experiencias
frec_rel_victoria_corridas = []


def experiencia(corridas, tiradas, eleccion, estrategia, capital_inicial):
  apuesta_inicial = definir_apuesta_inicial(estrategia)
  apuesta = apuesta_inicial 
  contador_secuencia_fibonacci = 0
  for j in range(corridas):
    valores = []
    apuesta = apuesta_inicial
    monto_total = []
    frec_relativa_victoria = []
    cantidad_apuestas_ganadas = 0
    bancarrota = 0
    contador_paroli = 0
    for i in range(tiradas):
      #Si el capital es finito y el monto total es menor al valor de la apuesto, no se puede seguir apostando
      if(capital_inicial != 0 and i > 0):
        if(monto_total[-1] < apuesta):
          if(bancarrota == 0):
            bancarrota = 1
          #En caso de bancarrota, nos aseguramos de calcular igualmente la frecuencia relativa de victorias
          frec_relativa_tirada = round(cantidad_apuestas_ganadas / (i+1), 4)
          frec_relativa_victoria.append(frec_relativa_tirada)
          monto_total.append(monto_total[-1])
          continue
      #Simulamos el uso de la ruleta, obteniendo un valor (rojo o negro)
      valor = generar_resultado_aleatorio(valor_elegido)
      resultado = convertir_a_color(valor)
      monto = 0
      if(resultado == eleccion):
        cantidad_apuestas_ganadas += 1
        if(i == 0):
          monto = capital_inicial + apuesta
        else:
          monto = monto_total[-1] + apuesta
        monto_total.append(monto) 

        # Actualizamos el contador para la estrategia de Fibonacci
        contador_secuencia_fibonacci= nuevo_valor_contador_sec_fibonacci(contador_secuencia_fibonacci, 1)
        
        # Actualizamos el valor de la apuesta según la estrategia elegida
        apuesta = nuevo_valor_apuesta(estrategia, apuesta_inicial, 1, apuesta, secuencia_fibonacci, contador_secuencia_fibonacci, contador_paroli)

        # Para la estrategia Paroli, se actualiza el contador de la misma
        if(contador_paroli <= 2):
          contador_paroli += 1
        else:
          contador_paroli = 0
      else:
        # Para la estrategia Paroli, se actualiza el contador de la misma
        contador_paroli = 0
        monto = 0
        if(i == 0):
          monto = capital_inicial - apuesta 
        else:
          monto = monto_total[-1] - apuesta
        monto_total.append(monto)

        # Actualizamos el contador para la estrategia de Fibonacci
        contador_secuencia_fibonacci = nuevo_valor_contador_sec_fibonacci(contador_secuencia_fibonacci, 0) 

        # Actualizamos el valor de la apuesta según la estrategia elegida
        apuesta = nuevo_valor_apuesta(estrategia, apuesta_inicial,  0, apuesta, secuencia_fibonacci, contador_secuencia_fibonacci, contador_paroli)

      frec_relativa_tirada = round(cantidad_apuestas_ganadas / (i+1), 4)
      frec_relativa_victoria.append(frec_relativa_tirada)

    # Almacenamos los valores de cada corrida
    valores_corridas.append(valores)
    monto_total_corridas.append(monto_total)
    frec_rel_victoria_corridas.append(frec_relativa_victoria)

    if(cantidad_apuestas_ganadas != 0):
      resultados_apuestas_corridas.append(round(tiradas / cantidad_apuestas_ganadas, 0)) # Guardamos la cantidad de apuestas ganadas en cada corrida
    else:
      #Si no se ganaron apuestas, ¿Qué resultado debería guardarse? | Propuesta: El total de tiradas
      resultados_apuestas_corridas.append(tiradas)

    bancarrotas_corridas.append(bancarrota)



def elaborar_graficas(capital_inicial, estrategia_elegida):
 
 nombre_estrategia = generar_nombre_estrategia(estrategia_elegida)

 monto_total_observado = calcular_monto_total_observado(monto_total_corridas, num_corridas, num_tiradas)

 frec_relativa_victoria_observada = calcular_frec_relativa_victoria_observada(frec_rel_victoria_corridas)

 #print(frec_rel_victoria_corridas)
 #print(frec_relativa_victoria_observada)

 resultado_apuestas_observado = calcular_promedio_apuestas_ganadas(resultados_apuestas_corridas)

 frec_bancarrota_observada = calcular_frec_bancarrota_observada(bancarrotas_corridas)

#Graficar, además, el promedio de tiradas que se debe realizar para ganar una apuesta respecto a la cantidad de corridas de la experiencia

 x1 = list(range(1, num_tiradas + 1))
 x2 = list(range(1, num_corridas + 1))
 fig, axs = plt.subplots(2, 2, figsize=(10, 7))
 axs[0, 0].plot(x1, monto_total_observado, label="Monto total observado", color="blue")
 axs[0, 0].plot(x1, [capital_inicial] * len(x1), label="Capital inicial", color="red", linestyle="--")
 axs[0, 0].set_title(f"Monto total observado (Estrategia: {nombre_estrategia})")
 axs[0, 0].set_xlabel("Número de tiradas")
 axs[0, 0].set_ylabel("Monto total")
 axs[0, 0].grid(True)
 axs[0, 0].legend()
 axs[0, 1].plot(x2, [promedio_apuestas_para_ganar] * len(x2), label="Promedio de tiradas esperado para ganar", color="purple", linestyle="--")
 axs[0, 1].plot(x2, resultado_apuestas_observado, label="Promedio de tiradas observado para ganar", color="green")
 axs[0, 1].set_title("Promedio de tiradas para ganar una apuesta")
 axs[0, 1].set_xlabel("Número de corridas")
 axs[0, 1].set_ylabel("Promedio de tiradas")
 axs[0, 1].grid(True)
 axs[0, 1].legend()
 axs[1, 0].plot(x1, [frecuencia_relativa_victoria_esperada] * len(x1), label="Frecuencia relativa esperada", color="brown", linestyle="--")
 axs[1, 0].plot(x1, frec_relativa_victoria_observada, label="Frecuencia relativa observada", color="purple")
 axs[1, 0].set_title(f"Frecuencia relativa victoria (Estrategia: {nombre_estrategia})")
 axs[1, 0].set_xlabel("Número de tiradas")
 axs[1, 0].set_ylabel("Frecuencia relativa")
 axs[1, 0].grid(True)
 axs[1, 0].legend()
 if(capital_disponible == "finito"):
   axs[1, 1].plot(x2, frec_bancarrota_observada, label="Frecuencia de bancarrota observada", color="orange")
   axs[1, 1].set_title("Frecuencia de bancarrota observada")
   axs[1, 1].set_xlabel("Número de corridas")
   axs[1, 1].set_ylabel("Frecuencia de bancarrota")
   axs[1, 1].grid(True)
   axs[1, 1].legend()
 plt.tight_layout()
 #plt.savefig(f"resultados_{nombre_estrategia}_tir{num_tiradas}_ejec{num_corridas}_{capital_disponible}.png")
 plt.show()


experiencia(num_corridas, num_tiradas, valor_elegido, estrategia_elegida, capital_inicial)
elaborar_graficas(capital_inicial, estrategia_elegida)

