import math
import random
import sys
import matplotlib.pyplot as plt

# Validamos que la ejecución del programa sea correcta
if(len(sys.argv) != 7 or sys.argv[1] != '-s' or sys.argv[3] != '-S' or sys.argv[5] != '-e'):
  print("Uso: python modelo_inventario.py -s <punto de pedido> -S <cantidad a ordenar> -e <número de ejecuciones/corridas>")
  sys.exit(1)

num_corridas = int(sys.argv[6])

# Variables globales (equivalentes a las del C)
amount = 0
bigs = 60
initial_inv_level = 60
inv_level = 0
next_event_type = 0
num_events = 4
num_months = 120
num_values_demand = 4
smalls = 20
num_policies = 2

area_holding = 0.0
area_shortage = 0.0
holding_cost = 1.0
incremental_cost = 3.0
maxlag = 1.0
mean_interdemand = 0.1
minlag = 0.5
prob_distrib_demand = {1: 0.167, 2: 0.500, 3: 0.833, 4: 1.000}
setup_cost = 32.0
shortage_cost = 5.0
sim_time = 0.0
time_last_event = 0.0
time_next_event = [0.0]*5  # indices 1..4 usados
total_ordering_cost = 0.0

# Funciones de generación de números aleatorios

def expon(mean):
    """Genera una variable exponencial con media 'mean'."""
    u = random.random()
    return -mean * math.log(u)

def uniform(a, b):
    """Genera variable uniforme entre a y b."""
    u = random.random()
    return a + u * (b - a)

def random_integer(prob_distrib):
    """Genera un entero basado en distribución acumulativa."""
    u = random.random()
    # Ordenar las claves para recorrer en orden
    claves = sorted(prob_distrib.keys())
    for i in claves:
        if u < prob_distrib[i]:
            return i
    # Si no retorna antes, devuelve la última clave (por seguridad)
    return claves[-1]

# Funciones principales del modelo

def initialize():
    global sim_time, inv_level, time_last_event, total_ordering_cost
    global area_holding, area_shortage, time_next_event

    sim_time = 0.0
    inv_level = initial_inv_level
    time_last_event = 0.0
    total_ordering_cost = 0.0
    area_holding = 0.0
    area_shortage = 0.0
    time_next_event[1] = 1.0e+30  # No hay pedido pendiente
    time_next_event[2] = sim_time + expon(mean_interdemand)  # próxima demanda
    time_next_event[3] = num_months  # fin simulación
    time_next_event[4] = 0.0  # evaluación inventario

def order_arrival():
    global inv_level, time_next_event
    inv_level += amount
    time_next_event[1] = 1.0e+30  # se elimina evento llegada pedido

def demand():
    global inv_level, time_next_event, sim_time
    d = random_integer(prob_distrib_demand)
    inv_level -= d
    time_next_event[2] = sim_time + expon(mean_interdemand)

def evaluate():
    global inv_level, amount, total_ordering_cost, time_next_event, sim_time
    if inv_level < smalls:
        amount = bigs - inv_level
        total_ordering_cost += setup_cost + incremental_cost * amount
        time_next_event[1] = sim_time + uniform(minlag, maxlag)
    time_next_event[4] = sim_time + 1.0  # programar próxima evaluación

def report(outfile):
    avg_ordering_cost = total_ordering_cost / num_months
    avg_holding_cost = holding_cost * area_holding / num_months
    avg_shortage_cost = shortage_cost * area_shortage / num_months
    total_cost = avg_ordering_cost + avg_holding_cost + avg_shortage_cost
    output = f"\n\n({smalls:3},{bigs:3}){total_cost:15.2f}{avg_ordering_cost:15.2f}{avg_holding_cost:15.2f}{avg_shortage_cost:15.2f}"
    costos_orden.append(avg_ordering_cost)
    costos_mantenimiento.append(avg_holding_cost)
    costos_faltante.append(avg_shortage_cost)
    costos_totales.append(total_cost)
    if outfile is None:
        print(output)
    else:
        print(output, file=outfile)

def update_time_avg_stats():
    global area_holding, area_shortage, time_last_event, sim_time, inv_level
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time
    if inv_level < 0:
        area_shortage -= inv_level * time_since_last_event
    elif inv_level > 0:
        area_holding += inv_level * time_since_last_event

def timing():
    global next_event_type, sim_time, time_next_event
    min_time_next_event = 1.0e+29
    next_event_type = 0
    for i in range(1, num_events+1):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i
    sim_time = min_time_next_event

def main():
    global smalls, bigs
    # Definí los parámetros directamente
    initial_inv_level = 60
    num_months = 120
    num_policies = 2
    num_values_demand = 4
    mean_interdemand = 0.1
    setup_cost = 32.0
    incremental_cost = 3.0
    holding_cost = 1.0
    shortage_cost = 5.0
    minlag = 0.5
    maxlag = 1.0

    # Distribución acumulada de demanda (ejemplo)
    prob_distrib_demand = {1: 0.167, 2: 0.500, 3: 0.833, 4: 1.000}

    # Políticas (smalls, bigs) para cada política a simular
    politicas = [(20, 60)]  # Ejemplo: dos políticas

    print("Single-product inventory system\n")
    print(f"Initial inventory level{initial_inv_level:24d} items\n")
    print(f"Number of demand sizes{num_values_demand:25d}\n")
    print("Distribution function of demand sizes ", end="")
    for i in range(1, num_values_demand+1):
        print(f"{prob_distrib_demand[i]:8.3f}", end="")
    print("\n")
    print(f"Mean interdemand time{mean_interdemand:26.2f}\n")
    print(f"Delivery lag range{minlag:29.2f} to{maxlag:10.2f} months\n")
    print(f"Length of the simulation{num_months:23d} months\n")
    print(f"K ={setup_cost:6.1f} i ={incremental_cost:6.1f} h ={holding_cost:6.1f} pi ={shortage_cost:6.1f}\n")
    print(f"Number of policies{num_policies:29d}\n")
    print(" Average Average Average Average")
    print(" Policy total cost ordering cost holding cost shortage cost")

    # Simulación para cada política (smalls, bigs)
    for idx, (smalls, bigs) in enumerate(politicas):
        # Asignar valores globales si es necesario
        globals()['smalls'] = smalls
        globals()['bigs'] = bigs

        initialize()

        # Simulación ciclo principal
        while True:
            timing()
            update_time_avg_stats()

            if next_event_type == 1:
                order_arrival()
            elif next_event_type == 2:
                demand()
            elif next_event_type == 4:
                evaluate()
            elif next_event_type == 3:
                report(None)  # Cambia report para imprimir por pantalla si usaba outfile
                break

costos_orden = []
costos_mantenimiento = []
costos_faltante = []
costos_totales = []
x1 = list(range(1, num_corridas + 1))

def graficar():
    plt.figure(figsize=(10, 6))
    plt.plot(x1, costos_orden, label='Costo de Orden', marker='o')
    plt.plot(x1, costos_mantenimiento, label='Costo de Mantenimiento', marker='o')
    plt.plot(x1, costos_faltante, label='Costo de Faltante', marker='o')
    plt.plot(x1, costos_totales, label='Costo Total', marker='o')
    
    plt.title('Costos del Modelo de Inventario')
    plt.xlabel('Número de Corrida')
    plt.ylabel('Costo')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    for i in range(num_corridas):
      main()
    graficar()