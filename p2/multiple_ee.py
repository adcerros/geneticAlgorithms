from math import sqrt, exp
from time import sleep
import requests
from random import randint, uniform, gauss
import glob
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from threading import Thread
import statistics
import time


url = "http://memento.evannai.inf.uc3m.es/age/robot10?"


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
        subject = [uniform(0, 360) for _ in range(gens_number)] 
        initial_poblation.append((evaluate(subject), subject, [uniform(100, 1000) for _ in range(gens_number)]))
    initial_poblation.sort()
    return initial_poblation


def make_generation(poblation, remplacement_rate, gens_number, learning_rate, prime_learning_rate, family_size):
    parents = get_parents(poblation, family_size, remplacement_rate)
    sons = [mix_and_mutation(parents[i : i + family_size], family_size, gens_number, learning_rate, prime_learning_rate) for i in range(0, len(parents), family_size)]
    new_poblation = remplacement(poblation, sons)
    # if statistics.mean([statistics.pstdev([elem[1][column] for elem in poblation]) for column in range(gens_number)]) < 50:
    #     print("Activada alerta de diversidad genetica!")
    #     random_pob = create_initial(int(len(poblation) / 2), gens_number)
    #     new_poblation = new_poblation[:-len(random_pob)] + random_pob
    #     new_poblation.sort()
    #     return new_poblation
    return new_poblation


def remplacement(poblation, sons):
    poblation_size = len(poblation)
    poblation = poblation + sons
    poblation.sort()
    return poblation[:poblation_size]


def mix_and_mutation(parents, family_size, gens_number, learning_rate, prime_learning_rate):
    # Mix
    son = [statistics.mean([parents[i][1][j] for i in range(family_size)]) for j in range(gens_number)]
    son_variances = [parents[randint(0, family_size - 1)][2][j] for j in range(gens_number)]
    # Mutation
    son = [(gen + gauss(0, variance)) % 360 for gen, variance in zip(son, son_variances)]
    son_variances = [variance * exp(gauss(0, learning_rate)) * exp(gauss(0, prime_learning_rate)) for variance in son_variances]
    # Evaluation
    son_fitness = evaluate(son)
    return (son_fitness, son, son_variances)


def get_parents(poblation, family_size, replacement_rate):
    parents = []
    index = 0
    while replacement_rate * family_size > len(parents):
        real_index = index % len(poblation)
        if real_index / len(poblation) <= uniform(0,1):
            parents.append(poblation[real_index])
        index += 1
    return parents


def get_and_check_data(poblation, data_file, gens_number):
    best_one_fitness = poblation[0][0]
    variances_mean = statistics.mean([statistics.mean(elem[2]) for elem in poblation])
    genetic_diversity = statistics.mean([statistics.pstdev([elem[1][column] for elem in poblation]) for column in range(gens_number)])
    data_file.write(str(best_one_fitness) + "," + str(variances_mean) + "," + str(genetic_diversity) + "\n")
    # Descomentar para obtener datos cada ciclo
    # print("Mejor fitness:", best_one_fitness)
    # print("Media de las varianzas:", variances_mean)
    # print("Diversidad genetica", genetic_diversity)
    if best_one_fitness <= 1.0e-06 or variances_mean <= 1.0e-15:
        print("La solucion encontrada es:", poblation[0][1], "con un valor de fitness", best_one_fitness, "Varianzas", poblation[0][2])
        return True
    return False


def collect_data():
    files = glob.glob("*.txt")
    rounds_data = [[line[:-2].split(',') for line in open(file)] for file in files]
    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure()
    ax1 = fig.add_subplot(gs[0, 0])
    for index, data in enumerate(rounds_data):
        ax1.plot([x for x in range(1, len(data) + 1)], [float(elem[0]) for elem in data], label=files[index])
    ax1.set_title("Fitness")
    ax1.legend(loc="upper right", prop={'size': 6})

    ax2 = fig.add_subplot(gs[0, 1])
    for index, data in enumerate(rounds_data):
        ax2.plot([x for x in range(1, len(data) + 1)], [float(elem[0]) for elem in data], label=files[index])
    ax2.set_title("Fitness (log)")
    ax2.legend(loc="upper right", prop={'size': 6})
    ax2.set_yscale('log')  
 
    ax3 = fig.add_subplot(gs[1, 0])
    for index, data in enumerate(rounds_data):
        ax3.plot([x for x in range(1, len(data) + 1)], [float(elem[1]) for elem in data], label=files[index])
    ax3.set_title("Media de varianzas")
    ax3.legend(loc="upper right", prop={'size': 6})
   
    ax4 = fig.add_subplot(gs[1, 1])
    for index, data in enumerate(rounds_data):
        ax4.plot([x for x in range(1, len(data) + 1)], [float(elem[2]) for elem in data], label=files[index])
    ax4.set_title("Variedad genetica (desviacion tipica media)")
    ax4.legend(loc="upper right", prop={'size': 6})
    plt.show()


def run(poblations_size=1, rounds=200, gens_number=4, remplacement_rate=5, family_size=2, b=1):
    start_time = time.time()
    poblation = create_initial(poblations_size, gens_number)
    data_file = open(str(poblations_size) + "_pob_" + str(family_size) + "_fmly_" + str(remplacement_rate) +  "_rmplcment_.txt", "w+")
    learning_rate = b / sqrt(2 * sqrt(gens_number)) 
    # prime_learning_rate =  b / sqrt(2 * gens_number) 
    try:
        for i in range(1, rounds + 1):
            # print("\nRealizando generacion", i)
            poblation = make_generation(poblation, int(len(poblation) * remplacement_rate / 100), gens_number, learning_rate, 1, family_size)
            if get_and_check_data(poblation, data_file, gens_number):
                data_file.close()
                print("Finalizado con:", poblations_size, "poblacion//", i, "rondas//", poblations_size * i, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
                return
        data_file.close()
        print("Finalizado normal con:", poblations_size, "poblacion//", rounds, "rondas//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
    except:
        data_file.close()
        print("Excepcion con:", poblations_size, "poblacion//", rounds, "rondas//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")


def run_multiple(params):
    threads = [Thread(target=run, args=param) for param in params]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()







# COMENTAR SI SE DESEA UNICAMENTE GENERAR LAS GRAFICAS
# params = poblation_size, rounds, gens_number, replacement, family
poblation_size, rounds, gens_number = 1000, 100000, 10
run_multiple([
[poblation_size, rounds, gens_number, 75, 2],
[poblation_size, rounds, gens_number, 75, 4],
[poblation_size, rounds, gens_number, 50, 2],
[5000, rounds, gens_number, 50, 4]
])
# /////////////////////




# COMENTAR PARA NO GENERAR LAS GRAFICAS
collect_data()
# /////////////////////
