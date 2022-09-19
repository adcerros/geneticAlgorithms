from time import sleep
import requests
from random import randint

mutation_factor = 0.05
chromosome = '0000000000000000000000000000000'
url = "http://memento.evannai.inf.uc3m.es/age/test?c="

def my_call(url, chromosome):
    try:
        my_request = requests.get(url + "".join(chromosome))
    except:
        print("Intentando reconectar ...")
        sleep(1)
        my_call(url, chromosome)
    print("\nEl resultado es:" + my_request.text) 
    return my_request.text

def evaluate(poblation, fitness_matrix):
    for i in range(len(fitness_matrix)):
        fitness_matrix[i] = my_call(url, poblation[i])


def create_initial():
    poblation = [[ str(randint(0,1)) for x in range(32)] for x in range (100)]
    fitness_matrix = [ 0 for x in range(100)]
    return poblation, fitness_matrix

def tournament():
    for i in range(len(fitness_matrix)):
        for j in range(4):
            

poblation, fitness_matrix = create_initial()
evaluate(poblation, fitness_matrix)