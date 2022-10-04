from time import sleep
import requests
from random import randint, gauss



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

def tournament(poblation, fitness_matrix, tournament_size = 2):
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

def mix(winners, mutation_factor, gens_number):
    new_poblation = []
    for i in range(0, len(winners), 2):
        first_son, second_son = get_sons(winners[i], winners[i+1], gens_number) 
        new_poblation.append(mutation(first_son, gens_number, mutation_factor))
        new_poblation.append(mutation(second_son, gens_number, mutation_factor))
    return new_poblation


# Se toma el cromosoma entero de uno de los progenitores
def get_sons(first_parent, second_parent, gens_number):
    first_son, second_son = [], []
    for i in range(gens_number):
        first_son.append(first_parent[i]) if randint(0,1) == 0 else first_son.append(second_parent[i])
        second_son.append(first_parent[i]) if randint(0,1) == 0 else second_son.append(second_parent[i])
    return first_son, second_son


def mutation(son, gens_number, mutation_factor, mean=0, standard_derivation=5):
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

def make_generation(poblation, mutation_factor, gens_number):
    fitness_matrix = evaluate(poblation)
    winners = tournament(poblation, fitness_matrix)
    new_poblation = mix(winners, mutation_factor, gens_number)

    #Clonacion del mejor individuo
    best_one_fitness = min(fitness_matrix)
    best_one = poblation[fitness_matrix.index(best_one_fitness)]
    new_poblation = clone(best_one, new_poblation)
    return new_poblation, best_one_fitness, best_one



def run(poblations_size=100, rounds=5000, mutation_factor=3, gens_number=10):
    #best_ones_list = []
    poblation = create_initial(poblations_size, gens_number)
    for i in range(rounds):
        print("Realizando generacion", i , "...")
        poblation, best_one_fitness, best_one = make_generation(poblation, mutation_factor, gens_number)
        print("Mejor valor de la generacion:", best_one_fitness)
        #best_ones_list.append(best)
        # if i > 10 and abs(best_ones_list[-10] - best_ones_list[0]) < 0.10:
        #     print("Se ha alcanzado un minimo local")
        #     return min(best_ones_list)
        if best_one_fitness == 0:
            print("Se ha alcanzado el resultado optimo")
            print("La solucion optima es:", best_one, "Fitness:", best_one_fitness)
            return best_one_fitness



run()
#OPCIONES
# Coger la mejor parte de cada padre evaluandolos por partes
# juntar a los mejores padres
# eliminar a un numero n de sujetos y clonar a los mejores (aumentando asi la probabilidad) -> mezclarlos
# mantener un numero de clones de los n mejores en cada ronda


#TAREAS
# QUE EL CRUZAMIENTO SEA DE DISTINTOS TIPOS, POR EJEMEPLO COGIENDO SIEMPRE EL MEJOR O UNA GRAN PARTE DEL MEJOR
# hacer que muten mas al principio y menos al final
# evaluar la diversidad genetica en cada ronda
# almacenar los resultados de las rondas y la diversidad genetica
