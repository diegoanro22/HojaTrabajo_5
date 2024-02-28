import simpy
import random


# Definimos valores iniciales
RANDOM_SEED = 42
RAM_CAPACITY = 100 #capacidad de la ram
CPU_SPEED = 3 #velocidad del CPU
INTERVAL = 1
NUM_PROCESSES = 201

#lista que almacena los tiempos de ejecucion
tiempos = []

def process(env, name, cpu, ram, memory_needed, cpu_speed, instructions):
    arrive_time = env.now
    
    yield ram.get(memory_needed)
    print(f"{name} obtuvo {memory_needed} de memoria RAM en tiempo {env.now}")
    
    # READY: Esperar por el CPU
    with cpu.request() as req:
        yield req
        
        # RUNNING: Ejecutar instrucciones
        while instructions > 0:
            yield env.timeout(1) 
            instructions -= min(cpu_speed, instructions)
            print(f"{name} ejecutó instrucciones, restantes: {instructions} en tiempo {env.now}")
            
            # Decidir el próximo estado
            if instructions <= 0:
                print(f"{name} terminó en tiempo {env.now}")
                tiempos.append(env.now - arrive_time)
                break
            else:
                next_state = random.randint(1, 21)
                if next_state == 1:
                    yield env.timeout(1) 
                    print(f"{name} realizando I/O en tiempo {env.now}")
    
    # Devolver la RAM utilizada
    yield ram.put(memory_needed)

def setup(env, num_processes, interval, cpu_speed, ram_capacity):
    # Crear recursos
    cpu = simpy.Resource(env, capacity=2)
    ram = simpy.Container(env, init=ram_capacity, capacity=ram_capacity)
    
    # Generar procesos
    for i in range(num_processes):
        memory_needed = random.randint(1, 10)
        instructions = random.randint(1, 10)
        env.process(process(env, f'Proceso {i}', cpu, ram, memory_needed, cpu_speed, instructions))
        
        yield env.timeout(random.expovariate(1.0 / interval))

# Start processes and run
env = simpy.Environment()
env.process(setup(env, NUM_PROCESSES, INTERVAL, CPU_SPEED, RAM_CAPACITY))
env.run()

