

def convertir_a_color(resultado):
  if(resultado == 0):
    return "rojo"
  else:
    return "negro"
  


def definir_capital(capital):
  if(capital == "finito"):
    return 500
  else:
    return 0
  


def generar_secuencia_fibonacci(tiradas):
  secuencia_fibonacci = [1, 1]
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
    return 1
  else:
    return 10



def nuevo_valor_contador_sec_fibonacci(contador_secuencia_fibonacci, secuencia_fibonacci, resultado):
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
#   Si gana, se resta 5 a la apuesta (hasta llegar al mínimo)
#   Si pierde, se suma 5 a la apuesta
#Fibonacci:
#   Si gana, se resta 2 a la secuencia de Fibonacci (hasta llegar al mínimo)
#   Si pierde, se suma 1 a la secuencia de Fibonacci 
def nuevo_valor_apuesta(estrategia, valor_minimo_apuesta, resultado_apuesta, valor_apuesta, secuencia_fibonacci, contador_secuencia_fibonacci, contador_paroli):
  if(resultado_apuesta == 1):
    if(estrategia == "m"):
      return valor_minimo_apuesta
    elif(estrategia == "a"):
      if(valor_apuesta - 5 > valor_minimo_apuesta):
        return valor_apuesta - 5
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
      return valor_apuesta + 5
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

def calcular_promedio_apuestas_ganadas(resultados_apuestas_corridas):
  resultado_apuestas_observado = []
  suma = 0
  for i in range(len(resultados_apuestas_corridas)):
    suma += resultados_apuestas_corridas[i]
    print(suma)
    resultado_apuestas_observado.append(round(suma / (i+1), 4))
  return resultado_apuestas_observado