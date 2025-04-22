

def calcular_frec_relativa_total(frecuencias):
  num_tiradas = len(frecuencias[0])
  num_corridas = len(frecuencias)
  frec_relativas_final = []
  for i in range(num_tiradas):
    frec_relativa_sumada = 0
    for j in range(num_corridas):
      frec_relativa_sumada += frecuencias[j][i]
    frec_relativa_promedio = round(frec_relativa_sumada / num_corridas, 4)
    frec_relativas_final.append(frec_relativa_promedio)
  return frec_relativas_final

def calcular_media_total(medias):
  num_tiradas = len(medias[0])
  num_corridas = len(medias)
  medias_finales = []
  for i in range(num_tiradas):
    media_sumada = 0
    for j in range(num_corridas):
      media_sumada += medias[j][i]
    media_promedio = round(media_sumada / num_corridas, 4)
    medias_finales.append(media_promedio)
  return medias_finales

def calcular_varianza_total(varianzas):
  num_tiradas = len(varianzas[0])
  num_corridas = len(varianzas)
  varianzas_finales = []
  for i in range(num_tiradas):
    varianza_sumada = 0
    for j in range(num_corridas):
      varianza_sumada += varianzas[j][i]
    varianza_promedio = round(varianza_sumada / num_corridas, 4)
    varianzas_finales.append(varianza_promedio)
  return varianzas_finales

def calcular_desvio_estandar_total(desvios_estandar):
  num_tiradas = len(desvios_estandar[0])
  num_corridas = len(desvios_estandar)
  desvios_estandar_finales = []
  for i in range(num_tiradas):
    desvio_sumado = 0
    for j in range(num_corridas):
      desvio_sumado += desvios_estandar[j][i]
    desvio_promedio = round(desvio_sumado / num_corridas, 4)
    desvios_estandar_finales.append(desvio_promedio)
  return desvios_estandar_finales

def calcular_varianza_valor_elegido_total(varianzas_valor_elegido):
  num_tiradas = len(varianzas_valor_elegido[0])
  num_corridas = len(varianzas_valor_elegido)
  varianzas_valor_elegido_finales = []
  for i in range(num_tiradas):
    varianza_sumada = 0
    for j in range(num_corridas):
      varianza_sumada += varianzas_valor_elegido[j][i]
    varianza_promedio = round(varianza_sumada / num_corridas, 4)
    varianzas_valor_elegido_finales.append(varianza_promedio)
  return varianzas_valor_elegido_finales

def calcular_desvio_estandar_valor_elegido_total(desvios_estandar_valor_elegido):
  num_tiradas = len(desvios_estandar_valor_elegido[0])
  num_corridas = len(desvios_estandar_valor_elegido)
  desvios_estandar_valor_elegido_finales = []
  for i in range(num_tiradas):
    desvio_sumado = 0
    for j in range(num_corridas):
      desvio_sumado += desvios_estandar_valor_elegido[j][i]
    desvio_promedio = round(desvio_sumado / num_corridas, 4)
    desvios_estandar_valor_elegido_finales.append(desvio_promedio)
  return desvios_estandar_valor_elegido_finales

