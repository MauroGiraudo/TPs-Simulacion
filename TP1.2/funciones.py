import random

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