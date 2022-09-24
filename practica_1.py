from time import sleep
import requests
from random import randint

MUTATION_FACTOR = 5
POBLATION_SIZE = 100
CRHOMOSOME_SIZE = 80
ROUNDS = 5000
REPLACE_SIZE = 10
GEN_SIZE = 8
url = "http://memento.evannai.inf.uc3m.es/age/test?c="


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
    for i in range(POBLATION_SIZE - 1):
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
        first_son, second_son = mutation(first_son), mutation(second_son)
        new_poblation.append(first_son)
        new_poblation.append(second_son)
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
    # Utilizando torneos
    return mix(tournament(poblation, fitness_matrix)), min(fitness_matrix), int(sum(fitness_matrix) / POBLATION_SIZE)
    # Sustituyendo a los 10 peores en cada ciclo
    # return mix_and_replace(poblation, fitness_matrix), min(fitness_matrix), int(sum(fitness_matrix) / POBLATION_SIZE)

def run():
    poblation = create_initial()
    for i in range(ROUNDS):
        print("Realizando generacion", i , "...")
        poblation, best, fitness_mean = make_generation(poblation)
        print("Mejor resultado: ", best, "Fitness medio:", fitness_mean)


print("\nEl mejor resultado obtenido ha sido:", run(), "\n")

# MANTENER A LOS 2 MEJORES EN CADA RONDA Y CREAR UN CRITERIO DE PARADA EFICIENTE