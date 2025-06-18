import random
import math
import sys
import matplotlib.pyplot as plt

def exponencial(media):
    return -media * math.log(random.random())

def inicializar():
    global tiempo_simulacion, estado_servidor, num_en_cola, tiempo_ultimo_evento, tiempo_llegada
    global num_clientes_retrasados, total_retrasos, area_num_en_cola, area_estado_servidor
    global tiempo_siguiente_evento, tiempo_medio_entre_llegadas
    global num_llegadas_denegadas
    num_llegadas_denegadas = 0
    # Inicializar el reloj de simulación
    tiempo_simulacion = 0.0

    # Inicializar las variables de estado
    estado_servidor = 'LIBRE'  # Equivalente a IDLE
    num_en_cola = 0
    tiempo_ultimo_evento = 0.0

    # Inicializar los contadores estadísticos
    num_clientes_retrasados = 0
    total_retrasos = 0.0
    area_num_en_cola = 0.0
    area_estado_servidor = 0.0

    # Inicializar la lista de eventos
    # Como no hay clientes presentes, se elimina el evento de salida (finalización de servicio)
    tiempo_siguiente_evento = {1: tiempo_simulacion + exponencial(tiempo_medio_entre_llegadas),
                               2: 1.0e+30}
    tiempo_llegada = []

def temporizar():
    global tipo_siguiente_evento, tiempo_simulacion, tiempo_siguiente_evento, archivo_salida
    global num_eventos

    min_tiempo_siguiente_evento = 1.0e+29
    tipo_siguiente_evento = 0

    # Determinar el tipo del próximo evento a ocurrir
    for i in range(1, num_eventos + 1):
        if tiempo_siguiente_evento[i] < min_tiempo_siguiente_evento:
            min_tiempo_siguiente_evento = tiempo_siguiente_evento[i]
            tipo_siguiente_evento = i

    # Verificar si la lista de eventos está vacía
    if tipo_siguiente_evento == 0:
        # La lista de eventos está vacía, terminar la simulación
        archivo_salida.write(f"\nLa lista de eventos está vacía en el tiempo {tiempo_simulacion:.3f}")
        sys.exit(1)

    # La lista de eventos no está vacía, avanzar el reloj de simulación
    tiempo_simulacion = min_tiempo_siguiente_evento

def actualizar_estadisticas():
    global tiempo_simulacion, tiempo_ultimo_evento
    global num_en_cola, area_num_en_cola
    global estado_servidor, area_estado_servidor

    # Calcular el tiempo transcurrido desde el último evento
    tiempo_desde_ultimo_evento = tiempo_simulacion - tiempo_ultimo_evento
    tiempo_ultimo_evento = tiempo_simulacion

    # Actualizar el área bajo la función número en cola
    area_num_en_cola += num_en_cola * tiempo_desde_ultimo_evento

    # Actualizar el área bajo la función del indicador de servidor ocupado
    if estado_servidor == 'OCUPADO':
        area_estado_servidor += 1 * tiempo_desde_ultimo_evento
    else:
        area_estado_servidor += 0 * tiempo_desde_ultimo_evento

def llegada():
    global tiempo_siguiente_evento, tiempo_simulacion, tiempo_medio_entre_llegadas, tiempo_medio_servicio
    global estado_servidor, num_en_cola, tiempo_llegada, num_clientes_retrasados, num_llegadas_denegadas
    global total_retrasos, archivo_salida, LIMITE_COLA
    LIMITE_COLA = 100 
    # Programar la próxima llegada
    tiempo_siguiente_evento[1] = tiempo_simulacion + exponencial(tiempo_medio_entre_llegadas)

    # Verificar si el servidor está ocupado
    if estado_servidor == 'OCUPADO':
        # El servidor está ocupado, se incrementa el número de clientes en la cola
        num_en_cola += 1

        # Verificar si existe una condición de desborde de la cola
        if num_en_cola >= LIMITE_COLA:
            num_llegadas_denegadas += 1
            # Simplemente no se agrega a la cola ni se programa salida
            return

        # Todavía hay lugar en la cola, se guarda el tiempo de llegada del nuevo cliente
        
        #tiempo_llegada[num_en_cola-1] = tiempo_simulacion
        tiempo_llegada.append(tiempo_simulacion)  # Agregar el tiempo de llegada al final de la lista

    else:
        # El servidor está libre, el cliente que llega no tiene demora
        demora = 0.0
        total_retrasos += demora

        # Incrementar la cantidad de clientes atendidos y poner el servidor como ocupado
        num_clientes_retrasados += 1
        estado_servidor = 'OCUPADO'

        # Programar una salida (finalización de servicio)
        tiempo_siguiente_evento[2] = tiempo_simulacion + exponencial(tiempo_medio_servicio)

def salida():
    global num_en_cola, tiempo_siguiente_evento, tiempo_simulacion, tiempo_medio_servicio
    global estado_servidor, tiempo_llegada, total_retrasos, num_clientes_retrasados

    # Verificar si la cola está vacía
    if num_en_cola == 0:
        # La cola está vacía, poner el servidor como libre y eliminar evento de salida
        estado_servidor = 'LIBRE'
        tiempo_siguiente_evento[2] = 1.0e+30
    else:
        # La cola no está vacía, disminuir el número de clientes en cola
        num_en_cola -= 1

        # Calcular la demora del cliente que comienza el servicio y actualizar total de retrasos
        demora = tiempo_simulacion - tiempo_llegada[0]
        total_retrasos += demora

        # Incrementar el número de clientes que han sido atendidos
        num_clientes_retrasados += 1

        # Programar la salida (finalización de servicio) del cliente actual
        tiempo_siguiente_evento[2] = tiempo_simulacion + exponencial(tiempo_medio_servicio)

        # Mover cada cliente en la cola una posición hacia adelante
        for i in range(1, num_en_cola):
            tiempo_llegada[i-1] = tiempo_llegada[i]

def generar_informe():
    global total_retrasos, num_clientes_retrasados
    global area_num_en_cola, tiempo_simulacion, area_estado_servidor
    global num_llegadas_denegadas, tiempo_medio_servicio

    if num_clientes_retrasados > 0:
        tiempo_promedio_en_cola = total_retrasos / num_clientes_retrasados
    else:
        tiempo_promedio_en_cola = 0.0

    promedio_en_cola = area_num_en_cola / tiempo_simulacion
    utilizacion_servidor = area_estado_servidor / tiempo_simulacion
    tiempo_promedio_en_sistema = tiempo_promedio_en_cola + tiempo_medio_servicio
    promedio_en_sistema = promedio_en_cola + utilizacion_servidor
    total_llegadas = num_clientes_retrasados + num_llegadas_denegadas
    if total_llegadas > 0:
        probabilidad_denegacion = num_llegadas_denegadas / total_llegadas
    else:
        probabilidad_denegacion = 0.0

    # Mostrar resultados
    print("\n\n--- RESULTADOS DE LA SIMULACIÓN ---")
    print(f"Tiempo promedio en cola:           {tiempo_promedio_en_cola:10.3f} minutos")
    print(f"Tiempo promedio en el sistema:     {tiempo_promedio_en_sistema:10.3f} minutos")
    print(f"Promedio de clientes en cola:      {promedio_en_cola:10.3f}")
    print(f"Promedio de clientes en el sistema:{promedio_en_sistema:10.3f}")
    print(f"Utilización del servidor:          {utilizacion_servidor:10.3f}")
    print(f"Probabilidad de denegación:        {probabilidad_denegacion:10.3f}")
    print(f"Llegadas denegadas:                {num_llegadas_denegadas}")
    print(f"Tiempo total simulado:             {tiempo_simulacion:.3f} minutos")

def main():
    global num_eventos, tiempo_medio_entre_llegadas, tiempo_medio_servicio, num_retrasos_requeridos
    global num_clientes_retrasados

    # Leer los parámetros desde consola
    print("Simulador M/M/1")
    tiempo_medio_entre_llegadas = float(sys.argv[2])
    tiempo_medio_servicio = float(sys.argv[4])
    num_retrasos_requeridos = int(sys.argv[6])

    num_eventos = 2

    # Mostrar resumen de entrada
    print("\n--- Parámetros de entrada ---")
    print(f"Tiempo medio entre llegadas: {tiempo_medio_entre_llegadas:.3f} minutos")
    print(f"Tiempo medio de servicio:    {tiempo_medio_servicio:.3f} minutos")
    print(f"Número de clientes a simular: {num_retrasos_requeridos}")

    # Inicializar la simulación
    inicializar()

    # Ejecutar la simulación
    while num_clientes_retrasados < num_retrasos_requeridos:
        temporizar()
        actualizar_estadisticas()
        if tipo_siguiente_evento == 1:
            llegada()
        elif tipo_siguiente_evento == 2:
            salida()

    # Mostrar informe final
    generar_informe()


if __name__ == "__main__":
    main()

# Validamos que la ejecución del programa sea correcta
if(len(sys.argv) != 7 or sys.argv[1] != '-a' or sys.argv[3] != '-s' or sys.argv[5] != '-c'):
  print("Uso: python modelo_mm1.py -a <tiempo medio entre arribos> -s <tiempo medio de servicio> -c <cantidad de clientes a simular>")
  sys.exit(1)

# Lista de tamaños de cola que queremos evaluar
limites_cola = [0, 2, 5, 10, 50]

# Guardar métricas para graficar
clientes_en_sistema_prom = []
clientes_en_cola_prom = []
tiempos_en_sistema_prom = []
tiempos_en_cola_prom = []
utilizaciones = []
prob_denegacion = []
prob_n_en_cola = []  # Lista de listas: una por cada n de clientes

# Valor fijo para cada simulación
tiempo_medio_entre_llegadas = 1.0
tiempo_medio_servicio = 0.5
num_retrasos_requeridos = 1000
# En inicializar():
historial_num_en_cola = []

# En actualizar_estadisticas():
historial_num_en_cola.append(num_en_cola)



for limite in limites_cola:
    # Reiniciar globals necesarios antes de cada simulación
    # Asumimos que podés pasar el límite como parámetro global o argumento a `main()`
    LIMITE_COLA = limite

    # Ejecutar simulación
    # Aquí deberías adaptar tu código principal para aceptar LIMITE_COLA como argumento
    # Por ejemplo: main_simulacion(llegada, servicio, clientes, LIMITE_COLA)
    main()  # Suponiendo que el código toma `LIMITE_COLA` como global

    # Calcular métricas
    promedio_en_cola = area_num_en_cola / tiempo_simulacion
    promedio_en_sistema = promedio_en_cola + (num_clientes_retrasados / tiempo_simulacion)
    tiempo_en_cola = total_retrasos / num_clientes_retrasados
    tiempo_en_sistema = tiempo_en_cola + tiempo_medio_servicio
    utilizacion = area_estado_servidor / tiempo_simulacion
    denegados = num_llegadas_denegadas if limite > 0 else 0
    prob_den = denegados / (num_clientes_retrasados + denegados)

    # Almacenar resultados
    clientes_en_sistema_prom.append(promedio_en_sistema)
    clientes_en_cola_prom.append(promedio_en_cola)
    tiempos_en_sistema_prom.append(tiempo_en_sistema)
    tiempos_en_cola_prom.append(tiempo_en_cola)
    utilizaciones.append(utilizacion)
    prob_denegacion.append(prob_den)

    # Probabilidad de n clientes en cola (estimado por fracción de tiempo)
    # Podés contar cuántas veces hubo exactamente n clientes en cola
    prob_por_n = []
    total_eventos = len(historial_num_en_cola)
    for n in range(0, max(historial_num_en_cola) + 1):
        prob_por_n.append(historial_num_en_cola.count(n) / total_eventos)
    prob_n_en_cola.append(prob_por_n)

# Graficar cada métrica
plt.figure(figsize=(12, 8))

# Clientes en sistema
plt.subplot(2, 3, 1)
plt.plot(limites_cola, clientes_en_sistema_prom, marker='o')
plt.title("Promedio de clientes en el sistema")
plt.xlabel("Tamaño máximo de cola")
plt.ylabel("Clientes")
plt.grid(True)

# Clientes en cola
plt.subplot(2, 3, 2)
plt.plot(limites_cola, clientes_en_cola_prom, marker='o', color='orange')
plt.title("Promedio de clientes en cola")
plt.xlabel("Tamaño máximo de cola")
plt.ylabel("Clientes")
plt.grid(True)

# Tiempo en sistema
plt.subplot(2, 3, 3)
plt.plot(limites_cola, tiempos_en_sistema_prom, marker='o', color='green')
plt.title("Tiempo promedio en el sistema")
plt.xlabel("Tamaño máximo de cola")
plt.ylabel("Tiempo (min)")
plt.grid(True)

# Tiempo en cola
plt.subplot(2, 3, 4)
plt.plot(limites_cola, tiempos_en_cola_prom, marker='o', color='red')
plt.title("Tiempo promedio en cola")
plt.xlabel("Tamaño máximo de cola")
plt.ylabel("Tiempo (min)")
plt.grid(True)

# Utilización del servidor
plt.subplot(2, 3, 5)
plt.plot(limites_cola, utilizaciones, marker='o', color='purple')
plt.title("Utilización del servidor")
plt.xlabel("Tamaño máximo de cola")
plt.ylabel("Porcentaje")
plt.grid(True)

# Probabilidad de denegación
plt.subplot(2, 3, 6)
plt.plot(limites_cola, prob_denegacion, marker='o', color='brown')
plt.title("Probabilidad de denegación")
plt.xlabel("Tamaño máximo de cola")
plt.ylabel("Probabilidad")
plt.grid(True)

plt.tight_layout()
plt.show()