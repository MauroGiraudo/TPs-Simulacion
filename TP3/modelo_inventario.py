import math
import random

# Variables globales (equivalentes a las del C)
amount = 0
bigs = 0
initial_inv_level = 0
inv_level = 0
next_event_type = 0
num_events = 4
num_months = 0
num_values_demand = 0
smalls = 0

area_holding = 0.0
area_shortage = 0.0
holding_cost = 0.0
incremental_cost = 0.0
maxlag = 0.0
mean_interdemand = 0.0
minlag = 0.0
prob_distrib_demand = [0.0]*26
setup_cost = 0.0
shortage_cost = 0.0
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
    i = 1
    while i < len(prob_distrib) and u >= prob_distrib[i]:
        i += 1
    return i

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
    print(f"\n\n({smalls:3},{bigs:3}){total_cost:15.2f}{avg_ordering_cost:15.2f}{avg_holding_cost:15.2f}{avg_shortage_cost:15.2f}", file=outfile)

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
    # Abrir archivos
    with open("inv.in", "r") as infile, open("inv.out", "w") as outfile:
        # Leer parámetros iniciales
        global initial_inv_level, num_months, num_values_demand, mean_interdemand
        global setup_cost, incremental_cost, holding_cost, shortage_cost
        global minlag, maxlag, num_events, prob_distrib_demand, num_policies

        line = infile.readline()
        vals = line.split()
        initial_inv_level = int(vals[0])
        num_months = int(vals[1])
        num_policies = int(vals[2])
        num_values_demand = int(vals[3])
        mean_interdemand = float(vals[4])
        setup_cost = float(vals[5])
        incremental_cost = float(vals[6])
        holding_cost = float(vals[7])
        shortage_cost = float(vals[8])
        minlag = float(vals[9])
        maxlag = float(vals[10])

        # Leer distribución de demanda acumulada (debe estar acumulada)
        for i in range(1, num_values_demand+1):
            prob_distrib_demand[i] = float(infile.readline())

        # Escribir encabezado en archivo
        print("Single-product inventory system\n", file=outfile)
        print(f"Initial inventory level{initial_inv_level:24d} items\n", file=outfile)
        print(f"Number of demand sizes{num_values_demand:25d}\n", file=outfile)
        print("Distribution function of demand sizes ", end="", file=outfile)
        for i in range(1, num_values_demand+1):
            print(f"{prob_distrib_demand[i]:8.3f}", end="", file=outfile)
        print("\n", file=outfile)
        print(f"Mean interdemand time{mean_interdemand:26.2f}\n", file=outfile)
        print(f"Delivery lag range{minlag:29.2f} to{maxlag:10.2f} months\n", file=outfile)
        print(f"Length of the simulation{num_months:23d} months\n", file=outfile)
        print(f"K ={setup_cost:6.1f} i ={incremental_cost:6.1f} h ={holding_cost:6.1f} pi ={shortage_cost:6.1f}\n", file=outfile)
        print(f"Number of policies{num_policies:29d}\n", file=outfile)
        print(" Average Average Average Average", file=outfile)
        print(" Policy total cost ordering cost holding cost shortage cost", file=outfile)

        # Simulación para cada política (smalls, bigs)
        for _ in range(num_policies):
            line = infile.readline()
            vals = line.split()
            smalls = int(vals[0])
            bigs = int(vals[1])

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
                    report(outfile)
                    break

if __name__ == "__main__":
    main()
