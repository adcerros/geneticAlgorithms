from time import sleep
import requests
from random import uniform, gauss, randint
import glob
import matplotlib.pyplot as plt
from threading import Thread
import statistics
import time


url = "http://memento.evannai.inf.uc3m.es/age/robot4?"



def my_call(url, chromosome):
    params = ""
    for i, gen in enumerate(chromosome, start=1):
        params += "c" + str(i) + "=" + str(gen) + "&"
    try:
        my_request = requests.get(url + params[:-1])
    except:
        print("Intentando reconectar ...")
        sleep(0.2)
        my_call(url, chromosome)
    return my_request.text


def evaluate(poblation):
    return [float(my_call(url, elem)) for elem in poblation]


def create_initial(poblations_size, gens_number):
    return [[uniform(-180,180) for _ in range(gens_number)] for _ in range(poblations_size)]


def mutation(son, gens_number, standard_derivation=10, mean=0):
    pos = randint(0, gens_number - 1)
    new_gen = son[pos] + (gauss(mean, standard_derivation))
    if new_gen < -180:
        new_gen = -180 + uniform(0, 20)
    elif new_gen > 180:
        new_gen = 180 - uniform(0, 20)
    son[pos] = new_gen
    return son

#DIVERSIDAD GENETICA!!!!!!!!!!
# genetic_diversity = statistics.mean([statistics.pstdev([elem[column] for elem in poblation]) for column in range(gens_number)])

def make_generation(poblation, gens_number):
    fitness_matrix = evaluate(poblation)
    best_one_fitness = min(fitness_matrix)
    best_one = poblation[fitness_matrix.index(best_one_fitness)]
    return new_poblation, best_one_fitness, best_one


def run(poblations_size=1, rounds=200, gens_number=10):
    start_time = time.time()
    poblation = create_initial(poblations_size, gens_number)
    data_file = open(str(poblations_size) + "_pob_" +  str(rounds) +  "_runs_.txt", "w+")
    try:
        for i in range(rounds):
            print("\nRealizando generacion", i + 1)
            poblation, best_one_fitness, best_one = make_generation(poblation, gens_number)
            print("Mejor fitness", best_one_fitness)
            print("Mejor individuo", best_one)
            data_file.write(str(best_one_fitness) + "\n")
            if best_one_fitness == 0:
                data_file.close()
                print("Finalizado con:", poblations_size, "poblacion//", i, "rondas//", poblations_size * i, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
                print("La solucion encontrada es:", best_one, "con un valor de fitness", best_one_fitness)
                return
        data_file.close()
        print("Finalizado con:", poblations_size, "poblacion//", rounds, "rondas//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
    except:
        data_file.close()
        print("Finalizado con:", poblations_size, "poblacion//", rounds, "rondas//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")


def collect_data():
    files = glob.glob("*.txt")
    rounds_data = [[line[:-2].split(',') for line in open(file)] for file in files]
    plt.subplot(1,2,1)
    plt.title("Fitness")
    for index, data in enumerate(rounds_data):
        plt.plot([x for x in range(1, len(data) + 1)], [float(elem[0]) for elem in data], label=files[index])
    plt.legend(loc="upper right", prop={'size': 6})
    plt.subplot(1,2,2)
    plt.title("Variedad genetica (desviacion tipica media)")
    for index, data in enumerate(rounds_data):
        plt.plot([x for x in range(1, len(data) + 1)], [float(elem[1]) for elem in data], label=files[index])
    plt.legend(loc="upper right", prop={'size': 6})
    plt.show()


def run_multiple(params):
    threads = [Thread(target=run, args=param) for param in params]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()







# COMENTAR SI SE DESEA UNICAMENTE GENERAR LAS GRAFICAS
# params = poblation_size, rounds, gens_number
run_multiple([ 
[800, 500, 4, 4, 20]
])

# /////////////////////




# COMENTAR PARA NO GENERAR LAS GRAFICAS
collect_data()
# /////////////////////
