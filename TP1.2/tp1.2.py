import random
import sys
import matplotlib.pyplot as plt
from funciones import convertir_a_color, definir_capital, nuevo_valor_apuesta, generar_secuencia_fibonacci, definir_apuesta_inicial, nuevo_valor_contador_sec_fibonacci, calcular_monto_total_observado


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
if(num_tiradas <= 0 or num_corridas <= 0 or (valor_elegido != "rojo" and valor_elegido != "negro") or (estrategia_elegida != "m" and estrategia_elegida != "a" and estrategia_elegida != "f" and estrategia_elegida != "o") or (capital_disponible != "finito" and capital_disponible != "infinito")):
  print("El número de tiradas y corridas debe ser mayor a 0, el valor elegido debe ser [rojo] o [negro], las estrategias son m(Martingala), a(D'Alembert), f(Fibonacci) u o() y el capital puede ser finito o infinito")
  sys.exit(1)

valores_corridas = []
capital_inicial = definir_capital(capital_disponible)
monto_total_corridas = []
secuencia_fibonacci = generar_secuencia_fibonacci(num_tiradas)

def experiencia(corridas, tiradas, eleccion, estrategia, capital_inicial):
  apuesta_inicial = definir_apuesta_inicial(estrategia)
  apuesta = apuesta_inicial 
  contador_secuencia_fibonacci = 0
  for j in range(corridas):
    valores = []
    monto_total = []
    for i in range(tiradas):
      if(capital_inicial != 0 and i > 0):
        if(monto_total[-1] < apuesta):
          monto_total.append(monto_total[-1])
          continue
      #Simulamos el uso de la ruleta, obteniendo un valor (rojo o negro)
      valor = random.randint(0, 1)
      resultado = convertir_a_color(valor)
      if(resultado == eleccion):
        if(i == 0):
          monto_total.append(capital_inicial + apuesta) # En la primer apuesta, sumamos al capital inicial el monto ganado
        else:
          monto_total.append(monto_total[-1] + apuesta) # Sumamos al monto total(hasta el momento) el monto ganado
        
        # Actualizamos el contador para la estrategia de Fibonacci
        contador_secuencia_fibonacci= nuevo_valor_contador_sec_fibonacci(contador_secuencia_fibonacci, secuencia_fibonacci, 1)
        
        # Actualizamos el valor de la apuesta según la estrategia elegida
        apuesta = nuevo_valor_apuesta(estrategia, apuesta_inicial, 1, apuesta, secuencia_fibonacci, contador_secuencia_fibonacci)

      else:
        if(i == 0):
          monto_total.append(capital_inicial - apuesta) # En la primer apuesta, restamos al capital inicial el monto perdido
        else:
          monto_total.append(monto_total[-1] - apuesta) #Restamos al monto total(hasta el momento) el monto perdido
        
        # Actualizamos el contador para la estrategia de Fibonacci
        contador_secuencia_fibonacci = nuevo_valor_contador_sec_fibonacci(contador_secuencia_fibonacci, secuencia_fibonacci, 0) 

        # Actualizamos el valor de la apuesta según la estrategia elegida
        apuesta = nuevo_valor_apuesta(estrategia, apuesta_inicial,  0, apuesta, secuencia_fibonacci, contador_secuencia_fibonacci)

    # Almacenamos los valores de cada corrida
    valores_corridas.append(valores)
    monto_total_corridas.append(monto_total)



def elaborar_graficas(capital_inicial, estrategia_elegida):
 
 # Crear una función que devuelva el nombre completo de la estrategia empleada basado en el 
 # parámetro para ponerlo en el título de la gráfica


 monto_total_observado = calcular_monto_total_observado(monto_total_corridas, num_corridas, num_tiradas)

 x1 = list(range(1, num_tiradas + 1))
 plt.figure(figsize=(10, 8))
 plt.plot(x1, monto_total_observado, label="Monto total observado", color="blue")
 plt.plot(x1, [capital_inicial] * len(x1), label="Capital inicial", color="red", linestyle="--")
 plt.title("Monto total observado vs Capital inicial")
 plt.xlabel("Número de tiradas")
 plt.ylabel("Monto total")
 plt.grid(True)
 plt.legend()

 plt.tight_layout()
 plt.show()

experiencia(num_corridas, num_tiradas, valor_elegido, estrategia_elegida, capital_inicial)
elaborar_graficas(capital_inicial, estrategia_elegida)
