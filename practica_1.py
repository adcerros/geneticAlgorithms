from time import sleep
import requests
from random import randint

mutation_factor = 0.05
POBLATION_SIZE = 1000
CRHOMOSOME_SIZE = 32
ROUNDS = 20
url = "http://memento.evannai.inf.uc3m.es/age/test?c="

def my_call(url, chromosome):
    try:
        my_request = requests.get(url + "".join(chromosome))
    except:
        print("Intentando reconectar ...")
        sleep(0.1)
        my_call(url, chromosome)
    return my_request.text

def evaluate(poblation):
    return [float(my_call(url, poblation[i])) for i in range(len(poblation))]


def create_initial():
    return [[str(randint(0,1)) for x in range(CRHOMOSOME_SIZE)] for x in range (POBLATION_SIZE)]

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
        first_son, second_son = "", ""
        for j in range(CRHOMOSOME_SIZE):
            first_son += winners[i + randint(0,1)][j]
            second_son += winners[i + randint(0,1)][j]
        new_poblation.append(first_son)
        new_poblation.append(second_son)
    return new_poblation
    
def make_generation(poblation):
    fitness_matrix = evaluate(poblation)
    print("Mejor resultado: ", max(fitness_matrix))
    return mix(tournament(poblation, fitness_matrix))



poblation = create_initial()
for i in range(ROUNDS):
    print("Realizando generacion " + str(i) + " ...")
    poblation = make_generation(poblation)
fitness_matrix = evaluate(poblation)
print("Mejor resultado:" + str(max(fitness_matrix)) + "\n")
