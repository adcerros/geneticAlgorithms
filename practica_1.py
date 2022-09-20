from time import sleep
import requests
from random import randint

mutation_factor = 0.05
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
    fitness_matrix = []
    for i in range(len(poblation)):
        fitness_matrix.append(float(my_call(url, poblation[i])))
    return fitness_matrix


def create_initial():
    poblation = [[ str(randint(0,1)) for x in range(32)] for x in range (100)]
    return poblation

def tournament(poblation, fitness_matrix):
    winners = []
    for i in range(len(fitness_matrix)):
        round_competitors = []
        for j in range(4):
            pos = randint(0,99)
            round_competitors.append([fitness_matrix[pos], pos])
        winners.append(poblation[round_competitors[round_competitors.index(max(round_competitors))][1]])
    return winners

def mix(winners):
    new_poblation = []
    for i in range(len(winners) - 1):
        first_son, second_son = "", ""
        for j in range(len(winners[i])):
            first_son += winners[i + randint(0,1)][j]
            second_son += winners[i + randint(0,1)][j]
        new_poblation.append(first_son)
        new_poblation.append(second_son)
    return new_poblation
    
def make_generation(poblation):
    fitness_matrix = evaluate(poblation)
    return mix(tournament(poblation, fitness_matrix))



poblation = create_initial()
for i in range(25):
    print("Realizando generacion " + str(i) + " ...")
    poblation = make_generation(poblation)
fitness_matrix = evaluate(poblation)
print("Mejor resultado:" + str(max(fitness_matrix)) + "\n")
