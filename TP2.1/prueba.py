import random
import matplotlib.pyplot as plt
import numpy as np
from funciones import son_coprimos

valores = [19283, 1293, 8542, 958423, 19237]

def generar_valor_binario(n):
  x = str(bin(n))
  x = x.split('b')
  x = x[1]

  sum = 0
  for i in range(len(x)):
    sum += int(x[i])

  bin_final = 0 if (sum % 2) == 0 else 1
  print(f"Valor binario: {x}  |  Suma: {sum}  |  Binario Final: {bin_final}")

  return bin_final

nuevos_valores = [generar_valor_binario(x) for x in valores]

print(nuevos_valores)