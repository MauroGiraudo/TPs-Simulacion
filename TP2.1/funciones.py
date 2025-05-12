import sys
from math import gcd

def obtener_numeros_centrales(valor):
  return ((valor // 100) % 10000)

def generar_valor_a(n):
  return (4*n - 1)

def son_coprimos(c, m):
    return gcd(c, m) == 1

def evaluar_test(resultado):
   if(resultado < 0.01):
      return "FALSE"
   else:
      return "TRUE"
   
def generar_valor_binario(n):
   n = str(bin(n))
   n = n.split('b')
   n = n[1]

   sum = 0
   for i in range(len(n)):
      sum += int(n[i])
   
   bin_final = 0 if (sum % 2) == 0 else 1
   
   return bin_final