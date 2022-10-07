from time import sleep
import requests
from random import randint, gauss
import glob
import matplotlib.pyplot as plt
from threading import Thread
import statistics
import time




url = "http://163.117.164.219/age/test?c="
#url = "http://163.117.164.219/age/alfa?c="


def my_call(url, chromosome):
    binary_cromosome = "".join(["{0:08b}".format(gen) for gen in chromosome])
    try:
        my_request = requests.get(url + binary_cromosome)
    except:
        print("Intentando reconectar ...")
        sleep(0.2)
        my_call(url, chromosome)
    return my_request.text

def evaluate(poblation):
    return [float(my_call(url, elem)) for elem in poblation]


def create_initial(poblations_size, gens_number):
    return [[randint(0,255) for _ in range(gens_number)] for _ in range(poblations_size)]

def tournament(poblation, fitness_matrix, tournament_size):
    winners = []
    for _ in range(len(poblation)):
        round_competitors = []
        for _ in range(tournament_size):
            pos = randint(0, len(poblation) - 1)
            round_competitors.append([fitness_matrix[pos], pos])
        winners.append(poblation[round_competitors[round_competitors.index(min(round_competitors))][1]])
    return winners

def sort_by_fitness(poblation, fitness_matrix):
    return [x for _, x in sorted(zip(fitness_matrix, poblation))]

# def sort_and_replace(poblation, fitness_matrix, replace_size):
#     new_poblation = sort_by_fitness(poblation, fitness_matrix)
#     if replace_size <= 0:
#         return new_poblation
#     for i in range(replace_size):  
#         new_poblation[-i] = new_poblation[i] 
#     return new_poblation

def mix(winners, mutation_factor, gens_number, standard_derivation):
    new_poblation = []
    for i in range(0, len(winners), 2):
        first_son, second_son = get_sons(winners[i], winners[i+1], gens_number) 
        new_poblation.append(mutation(first_son, gens_number, mutation_factor, standard_derivation))
        new_poblation.append(mutation(second_son, gens_number, mutation_factor, standard_derivation))
    return new_poblation


# Se toma el cromosoma entero de uno de los progenitores
def get_sons(first_parent, second_parent, gens_number):
    first_son, second_son = [], []
    for i in range(gens_number):
        first_son.append(first_parent[i]) if randint(0,1) == 0 else first_son.append(second_parent[i])
        second_son.append(first_parent[i]) if randint(0,1) == 0 else second_son.append(second_parent[i])
    return first_son, second_son


# def gets_sons_with_best_parts(first_parent, second_parent, gens_number):
#     first_son, second_son = [], []
#     base_chromosome = [0 for _ in range(gens_number)]
#     for i in range(gens_number):
#         first_parent_selection_fitness = float(my_call(url, base_chromosome[:i] + [first_parent[i]] + base_chromosome[i + 1 :]))
#         second_parent_selection_fitness = float(my_call(url, base_chromosome[:i] + [second_parent[i]] + base_chromosome[i + 1 :]))
#         first_son.append(first_parent[i]) if first_parent_selection_fitness >= second_parent_selection_fitness else first_son.append(second_parent[i])
#         second_son.append(first_parent[i]) if first_parent_selection_fitness < second_parent_selection_fitness else second_son.append(second_parent[i])
#     return first_son, second_son


def mutation(son, gens_number, mutation_factor, standard_derivation, mean=0):
    if randint(0,100) < mutation_factor:
        pos = randint(0, gens_number - 1)
        new_gen = son[pos] + int(gauss(mean, standard_derivation))
        if new_gen < 0:
            new_gen = 0
        elif new_gen > 255:
            new_gen = 255
        son[pos] = new_gen
    return son


def multiple_clone(best_ones, poblation):
    for i in range(len(best_ones)):
        poblation[randint(0, len(poblation) - 1)] = best_ones[i]
    return poblation

def clone(best_one, poblation):
    poblation[randint(0, len(poblation) - 1)] = best_one
    return poblation

def make_generation(poblation, mutation_factor, gens_number, tournament_size, standard_derivation):
    fitness_matrix = evaluate(poblation)
    #Calculo de homogeneidad de los datos mediante desviacion tipica
    genetic_diversity = statistics.mean([statistics.pstdev([elem[column] for elem in poblation]) for column in range(gens_number)])
    
    winners = tournament(poblation, fitness_matrix, tournament_size)
    new_poblation = mix(winners, mutation_factor, gens_number, standard_derivation)

    #Clonacion del mejor individuo
    best_one_fitness = min(fitness_matrix)
    best_one = poblation[fitness_matrix.index(best_one_fitness)]
    new_poblation = clone(best_one, new_poblation)

    return new_poblation, best_one_fitness, genetic_diversity



def run(poblations_size=200, rounds=200, mutation_factor=5, gens_number=10, tournament_size=2, standard_derivation=15):
    start_time = time.time()
    poblation = create_initial(poblations_size, gens_number)
    data_file = open(str(poblations_size) + "_pob_" +  str(rounds) +  "_runs_" + str(mutation_factor) + "_mut_" + str(tournament_size) + "_tornmnt_siz_" + str(standard_derivation) + "_std_dev.txt", "w+")
    try:
        for i in range(rounds):
            poblation, best_one_fitness, genetic_diversity = make_generation(poblation, mutation_factor, gens_number, tournament_size, standard_derivation)
            data_file.write(str(best_one_fitness) + "," + str(genetic_diversity) + "\n")
            if best_one_fitness == 0:
                data_file.close()
                print("Finalizado con:", poblations_size, "poblacion//", i, "rondas//", mutation_factor, "factor de mutacion//", tournament_size, "tamaño de torneo//", poblations_size * i, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
                return
        data_file.close()
        print("Finalizado con:", poblations_size, "poblacion//", rounds, "rondas//", mutation_factor, "factor de mutacion//", tournament_size, "tamaño de torneo//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
    except:
        data_file.close()
        print("Finalizado con:", poblations_size, "poblacion//", rounds, "rondas//", mutation_factor, "factor de mutacion//", tournament_size, "tamaño de torneo//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")

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

# params = poblation_size, rounds, mutation_factor, gens_number, tournament_size, standard_derivation
def run_multiple(params=[[200, 200, 7, 10, 2, 15]]):
    threads = [Thread(target=run, args=param) for param in params]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


# params = poblation_size, rounds, mutation_factor, gens_number, tournament_size, standard_derivation

rounds, gens_number, tournament_size, standard_derivation = 100, 10, 2, 15
run_multiple([
[400, rounds, 10, gens_number, 4, 50], 
[800, rounds, 10, gens_number, 4, 50],
[1500, rounds, 10, gens_number, 4, 50]])

collect_data()


#OPCIONES
# Forzar mutaciones a los peores
# Coger la mejor parte de cada padre evaluandolos por partes
# juntar a los mejores padres
# eliminar a un numero n de sujetos y clonar a los mejores (aumentando asi la probabilidad) -> mezclarlos
# mantener un numero de clones de los n mejores en cada ronda


#TAREAS
# hacer que muten mas al principio y menos al final
# evaluar la diversidad genetica en cada ronda
