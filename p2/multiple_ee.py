from cmath import sqrt
import math
from time import sleep
import requests
from random import randint, uniform, gauss
import glob
import matplotlib.pyplot as plt
from threading import Thread
import statistics
import time
from heapq import heappop, heappush



url = "http://memento.evannai.inf.uc3m.es/age/robot4?"


def my_call(url, subject):
    params = ""
    for i, gen in enumerate(subject, start=1):
        params += "c" + str(i) + "=" + str(gen) + "&"
    try:
        my_request = requests.get(url + params[:-1])
    except:
        print("Intentando reconectar ...")
        sleep(0.2)
        my_call(url, subject)
    return my_request.text


def evaluate(subject):
    return float(my_call(url, subject))


def create_initial(poblations_size, gens_number):
    initial_poblation = []
    for _ in range(poblations_size):
        subject = [uniform(-180,180) for _ in range(gens_number)] 
        heappush(initial_poblation, (evaluate(subject), subject, [uniform(1000, 10000) for _ in range(gens_number)]))
    return initial_poblation


def make_generation(poblation, replacement_rate=5, family_size=2, gens_number=4):
    parents = get_parents(poblation, replacement_rate, family_size)
    sons = [mix_and_mutation(parents[i : i + family_size], family_size, gens_number) for i in range(0, len(parents), family_size)]
    new_poblation = remplacement(poblation, sons)
    return new_poblation


def remplacement(poblation, sons):
    poblation_size = len(poblation)
    for elem in sons:
        heappush(poblation, elem)
    return poblation[:poblation_size]


def mix_and_mutation(parents, family_size, gens_number, b=1):
    # Mix
    son = [sum([parents[i][1][j] for i in range(family_size)]) / family_size for j in range(gens_number)]
    son_variances = [parents[randint(0, family_size - 1)][2][j] for j in range(gens_number)]
    # Mutation
    son = [max(min(gen + gauss(0, variance), 180), -180) for gen, variance in zip(son, son_variances)]
    learning_rate = b / sqrt(2 * sqrt(gens_number)) 
    prime_learning_rate =  b / sqrt(2 * gens_number) 
    print("UNO")
    son_variances = [variance * math.exp(gauss(0, learning_rate)) * math.exp(gauss(0, prime_learning_rate)) for variance in son_variances]
    # Evaluation
    print("DOS")
    son_fitness = evaluate(son)
    return (son_fitness, son, son_variances)


def mutation(son):
    return son


def get_parents(poblation, replacement_rate, family_size):
    parents = []
    index = 0
    while len(parents) < replacement_rate * family_size:
        real_index = index % len(poblation)
        if real_index / len(poblation) >= uniform(0,1):
            parents.append(poblation[real_index])
        index += 1
    return parents


def run(poblations_size=1, rounds=200, gens_number=4):
    start_time = time.time()
    poblation = create_initial(poblations_size, gens_number)
    data_file = open(str(poblations_size) + "_pob_" +  str(rounds) +  "_runs_.txt", "w+")
    try:
        for i in range(1, rounds + 1):
            print("\nRealizando generacion", i)
            poblation = make_generation(poblation, gens_number)
            best_one_fitness = poblation[0][0]





            #genetic_diversity = statistics.mean([statistics.pstdev([elem[column] for elem in poblation]) for column in range(gens_number)])
            # print("Mejor fitness", best_one_fitness, "Diversidad genetica", genetic_diversity)
            # data_file.write(str(best_one_fitness) + "," + str(genetic_diversity) + "\n")
            if best_one_fitness <= 1.0e-06:
                data_file.close()
                print("Finalizado con:", poblations_size, "poblacion//", i, "rondas//", poblations_size * i, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
                print("La solucion encontrada es:", poblation[0][1], "con un valor de fitness", best_one_fitness, "Varianzas", poblation[0][2])
                return
        data_file.close()
        print("Finalizado normal con:", poblations_size, "poblacion//", rounds, "rondas//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
    except:
        data_file.close()
        print("Excepcion con:", poblations_size, "poblacion//", rounds, "rondas//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")


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
# run_multiple([ 
# [10, 2, 4]
# ])
run(10,2,4)
# /////////////////////




# COMENTAR PARA NO GENERAR LAS GRAFICAS
collect_data()
# /////////////////////
