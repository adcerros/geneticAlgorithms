from time import sleep
import requests
from random import randint

MUTATION_FACTOR = 15
POBLATION_SIZE = 100
CRHOMOSOME_SIZE = 32
ROUNDS = 4000
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
    for i in range(POBLATION_SIZE):
        round_competitors = []
        for j in range(4):
            pos = randint(0,99)
            round_competitors.append([fitness_matrix[pos], pos])
        winners.append(poblation[round_competitors[round_competitors.index(max(round_competitors))][1]])
    return winners

def mix(winners):
    new_poblation = []
    for i in range(0, POBLATION_SIZE, 2):
        first_son, second_son = [], []
        for j in range(CRHOMOSOME_SIZE):
            first_son.append(winners[i + randint(0,1)][j])
            if randint(0,100) < MUTATION_FACTOR:
                first_son[-1] = '0' if first_son[-1] == '1' else '1'
            second_son.append(winners[i + randint(0,1)][j])
            if randint(0,100) < MUTATION_FACTOR:
                second_son[-1] = '0' if second_son[-1] == '1' else '1' 
        new_poblation.append(first_son)
        new_poblation.append(second_son)
    return new_poblation
    
def make_generation(poblation):
    fitness_matrix = evaluate(poblation)
    return mix(tournament(poblation, fitness_matrix)), max(fitness_matrix)

def run():
    best_fitness = []
    poblation = create_initial()
    for i in range(ROUNDS):
        print("Realizando generacion", i , "...")
        poblation, best = make_generation(poblation)
        print("Mejor resultado: ", best)
        best_fitness.append(best)
        if i > 10 and abs(best_fitness[-1] - best_fitness[-10]) < 50:
            return max(best_fitness)


print("\El mejor resultado obtenido ha sido:", run(), "\n")

