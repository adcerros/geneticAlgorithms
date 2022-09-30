from time import sleep
import requests
from random import randint

MUTATION_FACTOR = 5
POBLATION_SIZE = 100
CRHOMOSOME_SIZE = 80
ROUNDS = 5000
REPLACE_SIZE = 10
GEN_SIZE = 8

#url = "http://163.117.164.219/age/test?c="
url = "http://163.117.164.219/age/alfa?c="


def my_call(url, chromosome):
    try:
        my_request = requests.get(url + ''.join(str(x) for x in chromosome))
    except:
        print("Intentando reconectar ...")
        sleep(0.2)
        my_call(url, chromosome)
    return my_request.text

def evaluate(poblation):
    return [float(my_call(url, poblation[i])) for i in range(len(poblation))]


def create_initial():
    return [[randint(0,1) for x in range(CRHOMOSOME_SIZE)] for x in range (POBLATION_SIZE)]

def tournament(poblation, fitness_matrix):
    winners = []
    for i in range(POBLATION_SIZE):
        round_competitors = []
        for j in range(4):
            pos = randint(0,99)
            round_competitors.append([fitness_matrix[pos], pos])
        winners.append(poblation[round_competitors[round_competitors.index(min(round_competitors))][1]])
    return winners

def sort_by_fitness(poblation, fitness_matrix):
    return [x for _, x in sorted(zip(fitness_matrix, poblation))]

def mix_and_replace(poblation, fitness_matrix):
    new_poblation = sort_by_fitness(poblation, fitness_matrix)
    for i in range(REPLACE_SIZE):  
        new_poblation[-i], new_poblation[-(i+1)] = get_sons(new_poblation[i], new_poblation[i+1]) 
    return new_poblation

def mix(winners):
    new_poblation = []
    for i in range(0, POBLATION_SIZE, 2):
        first_son, second_son = get_sons(winners[i], winners[i+1]) 
        new_poblation.append(mutation(first_son))
        new_poblation.append(mutation(second_son))
    return new_poblation

# Se toman los valores bit a bit
def get_sons_complete_mix(first_parent, second_parent):
    first_son, second_son = [], []
    for j in range(CRHOMOSOME_SIZE):
        first_son.append(first_parent[j] if randint(0,1) == 0 else second_parent[j])
        second_son.append(first_parent[j] if randint(0,1) == 0 else second_parent[j])
    return first_son, second_son

# Se toma el cromosoma entero de uno de los progenitores
def get_sons(first_parent, second_parent):
    first_son, second_son = [], []
    for j in range(0, CRHOMOSOME_SIZE, GEN_SIZE):
        first_son += first_parent[j : j + GEN_SIZE] if randint(0,1) == 0 else second_parent[j : j + GEN_SIZE]
        second_son += first_parent[j : j + GEN_SIZE] if randint(0,1) == 0 else second_parent[j : j + GEN_SIZE]
    return first_son, second_son


def mutation(son):
    if randint(0,100) < MUTATION_FACTOR:
        pos = randint(0, CRHOMOSOME_SIZE - 1)
        son[pos] = 0 if son[pos] == 1 else 1
    return son

def make_generation(poblation):
    fitness_matrix = evaluate(poblation)
    # Utilizando torneos y manteniendo al mejor de cada generacion
    best_one = poblation[fitness_matrix.index(min(fitness_matrix))]
    new_poblation = mix(tournament(poblation, fitness_matrix))
    new_poblation[fitness_matrix.index(max(fitness_matrix))] = best_one
    return new_poblation, min(fitness_matrix)
    # Sustituyendo a los 10 peores en cada ciclo
    # return mix_and_replace(poblation, fitness_matrix), min(fitness_matrix), int(sum(fitness_matrix) / POBLATION_SIZE)

def run():
    #best_ones_list = []
    poblation = create_initial()
    for i in range(ROUNDS):
        print("Realizando generacion", i , "...")
        poblation, best = make_generation(poblation)
        print("Mejor valor de la generacion:", best)
        #best_ones_list.append(best)
        # if i > 10 and abs(best_ones_list[-10] - best_ones_list[0]) < 0.10:
        #     print("Se ha alcanzado un minimo local")
        #     return min(best_ones_list)
        if best == 0:
            print("Se ha alcanzado el resultado optimo")
            return best



print("\nEl mejor resultado obtenido ha sido:", run(), "\n")

# MANTENER A LOS 2 MEJORES EN CADA RONDA Y CREAR UN CRITERIO DE PARADA EFICIENTE
# Añadir una distribucion gaussiana para las mutaciones