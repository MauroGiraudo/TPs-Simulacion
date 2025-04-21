import random
import sys
import matplotlib.pyplot as plt
import numpy as np

# Validamos que la ejecución del programa sea correcta
if(len(sys.argv) != 7 or sys.argv[1] != '-c' or sys.argv[3] != '-n' or sys.argv[5] != '-z'):
  print("Uso: python tp1.py -c <numero_tiradas> -n <numero_corridas> -z <valor_elegido>")
  sys.exit(1)

# Recuperamos los argumentos ingresados por la consola
num_tiradas = int(sys.argv[2])
num_corridas = int(sys.argv[4])
valor_elegido = int(sys.argv[6])
# Validamos los argumentos
if(num_tiradas <= 0 or num_corridas <= 0 or valor_elegido < 0 or valor_elegido > 36):
  print("El número de tiradas y corridas debe ser mayor a 0, mientras que el valor elegido debe estar entre 0 y 36")
  sys.exit(1)

# valores = [] [SEGURAMENTE NO SE UTILICE]
for i in range(num_corridas):
  valores_corrida = []
  frec_absoluta = 0
  frec_relativas = []
  medias = []
  varianzas = []
  desvios_estandar = []
  varianzas_valor_elegido = []
  desvios_estandar_valor_elegido = []
  for _ in range(num_tiradas):

    #Simulamos el uso de la ruleta, obteniendo un valor entre 0 y 36
    valor = random.randint(0, 36)

    #Calculamos y almacenamos los valores de las características estudiadas en cada tirada
    valores_corrida.append(valor)
    if valor == valor_elegido:
      frec_absoluta += 1
    frec_relativas.append(round(frec_absoluta / len(valores_corrida), 4))
    medias.append(round(sum(valores_corrida) / len(valores_corrida), 4))
    var = round(sum((x - medias[-1]) ** 2 for x in valores_corrida) / (len(valores_corrida)), 4)
    varianzas.append(var)
    desvios_estandar.append(round(var ** 0.5, 4))
    var_val_eleg = round(sum((x - valor_elegido) ** 2 for x in valores_corrida) / len(valores_corrida), 4)
    varianzas_valor_elegido.append(var_val_eleg)
    desvios_estandar_valor_elegido.append(round(var_val_eleg ** 0.5, 4))
    
  # valores.extend(valores_corrida) [SEGURAMENTE NO SE UTILICE]

  #Obtenemos los valores esperados
  frec_relativa_esperada = round(1 / 37, 4)
  media_esperada = sum(list(range(0, 37))) / 37
  varianza_esperada = sum((x - media_esperada) ** 2 for x in range(0, 37)) / 37
  desvio_est_esperado = round(varianza_esperada ** 0.5, 4)
  varianza_valor_elegido_esperada = sum((x - valor_elegido) ** 2 for x in range(0, 37)) / 37
  desvio_estandar_valor_elegido_esperado = round(varianza_valor_elegido_esperada ** 0.5, 4)
  
  #Elaboramos los gráficos pertinentes para comparar los valores esperados con los obtenidos
  x1 = list(range(1, num_tiradas + 1))
  fig, axs = plt.subplots(3, 2, figsize=(14, 6))
  axs[0, 0].plot(x1, [frec_relativa_esperada] * len(x1), color='blue', label="Frecuencia Relativa Esperada")
  axs[0, 0].plot(x1, frec_relativas, color='purple', label=f"Frecuencia Relativa del número {valor_elegido} luego de {num_tiradas} tiradas")
  axs[0, 0].set_title(f'Frecuencia relativa respecto al número {valor_elegido}')
  axs[0, 0].set_xlabel('Número de tiradas')
  axs[0, 0].set_ylabel('Frecuencia relativa')
  axs[0, 0].legend()
  axs[0, 0].grid(True)
  axs[0, 1].plot(x1, [media_esperada] * len(x1), color='red', label="Media Esperada")
  axs[0, 1].plot(x1, medias, color='black', label=f"Media de valores luego de {num_tiradas} tiradas")
  axs[0, 1].set_title('Media')
  axs[0, 1].set_xlabel('Número de tiradas')
  axs[0, 1].set_ylabel('Media')
  axs[0, 1].legend()
  axs[0, 1].grid(True)
  axs[1, 0].plot(x1, [varianza_esperada] * len(x1), color='green', label="Varianza Esperada")
  axs[1, 0].plot(x1, varianzas, color='gray', label=f"Varianza luego de {num_tiradas} tiradas")
  axs[1, 0].set_title('Varianza')
  axs[1, 0].set_xlabel('Número de tiradas')
  axs[1, 0].set_ylabel('Varianza')
  axs[1, 0].legend()
  axs[1, 0].grid(True)
  axs[1, 1].plot(x1, [desvio_est_esperado] * len(x1), color='orange', label="Desvio Estandar Esperado")
  axs[1, 1].plot(x1, desvios_estandar, color='brown', label=f"Desvio Estandar luego de {num_tiradas} tiradas")
  axs[1, 1].set_title('Desvio estandar')
  axs[1, 1].set_xlabel('Número de tiradas')
  axs[1, 1].set_ylabel('Desvio estandar')
  axs[1, 1].legend()
  axs[1, 1].grid(True)
  axs[2, 0].plot(x1, [varianza_valor_elegido_esperada] * len(x1), color='yellow', label="Desvio Cuadratico Esperado")
  axs[2, 0].plot(x1, varianzas_valor_elegido, color='pink', label=f"Desvio Cuadratico del número {valor_elegido} luego de {num_tiradas} tiradas")
  axs[2, 0].set_title(f'Varianza respecto al número {valor_elegido}')
  axs[2, 0].set_xlabel('Número de tiradas')
  axs[2, 0].set_ylabel('Varianza')
  axs[2, 0].legend()
  axs[2, 0].grid(True)
  axs[2, 1].plot(x1, [desvio_estandar_valor_elegido_esperado] * len(x1), color='purple', label="Desvio Estandar Esperado")
  axs[2, 1].plot(x1, desvios_estandar_valor_elegido, color='blue', label=f"Desvio Estandar del número {valor_elegido} luego de {num_tiradas} tiradas")
  axs[2, 1].set_title(f'Desvio estandar respecto al número {valor_elegido}')
  axs[2, 1].set_xlabel('Número de tiradas')
  axs[2, 1].set_ylabel('Desvio estandar')
  axs[2, 1].legend()
  axs[2, 1].grid(True)
  plt.tight_layout()
  plt.show()
