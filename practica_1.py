from time import sleep
import requests
from random import randint



url = "http://163.117.164.219/age/test?c="
#url = "http://163.117.164.219/age/alfa?c="


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


def create_initial(poblations_size, gens_number, gen_size):
    return [[randint(0,1) for x in range(gens_number * gen_size)] for x in range (poblations_size)]

def tournament(poblation, fitness_matrix, tournament_size = 4):
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

def replace(poblation, fitness_matrix, replace_size):
    if replace_size <= 0:
        return poblation
    new_poblation = sort_by_fitness(poblation, fitness_matrix)
    for i in range(replace_size):  
        new_poblation[-i] = new_poblation[i] 
    return new_poblation

def mix(winners, mutation_factor, gens_number, gen_size):
    new_poblation = []
    for i in range(0, len(winners), 2):
        first_son, second_son = get_sons(winners[i], winners[i+1], gens_number, gen_size) 
        new_poblation.append(mutation(first_son, gens_number, gen_size, mutation_factor))
        new_poblation.append(mutation(second_son, gens_number, gen_size, mutation_factor))
    return new_poblation


# Se toma el cromosoma entero de uno de los progenitores
def get_sons(first_parent, second_parent, gens_number, gen_size):
    first_son, second_son = [], []
    for j in range(0, gens_number * gen_size, gen_size):
        first_son += first_parent[j : j + gen_size] if randint(0,1) == 0 else second_parent[j : j + gen_size]
        second_son += first_parent[j : j + gen_size] if randint(0,1) == 0 else second_parent[j : j + gen_size]
    return first_son, second_son


def mutation(son, gens_number, gen_size, mutation_factor):
    if randint(0,100) < mutation_factor:
        pos = randint(0, gens_number - 1) * 8
        gen_to_change = int(''.join(str(x) for x in son[pos:pos + gen_size]), 2)
        new_gen = gen_to_change + randint(-5,5)
        if new_gen < 0:
            new_gen = 0
        elif new_gen > 255:
            new_gen = 255
        son = son[:pos] + [int(x) for x in "{0:08b}".format(int(new_gen))] + son[pos + gen_size:]
    return son


def clone(best_ones, poblation):
    for i in range(len(best_ones)):
        poblation[randint(0, len(poblation) - 1)] = best_ones[i]
    return poblation


def make_generation(poblation, mutation_factor, gens_number, gen_size, replace_size, clone_size):
    fitness_matrix = evaluate(poblation)
    sorted_and_replaced_poblation = replace(poblation, fitness_matrix, replace_size)
    winners = tournament(sorted_and_replaced_poblation, fitness_matrix)
    new_poblation = mix(winners, mutation_factor, gens_number, gen_size)
    new_poblation = clone(sorted_and_replaced_poblation[:clone_size], new_poblation)
    return new_poblation, min(fitness_matrix)



def run(poblations_size = 1000, rounds=500, mutation_factor=5, gens_number=10, gen_size=8, replace_size=5, clone_size=2):
    #best_ones_list = []
    poblation = create_initial(poblations_size, gens_number, gen_size)
    for i in range(rounds):
        print("Realizando generacion", i , "...")
        poblation, best = make_generation(poblation, mutation_factor, gens_number, gen_size, replace_size, clone_size)
        print("Mejor valor de la generacion:", best)
        #best_ones_list.append(best)
        # if i > 10 and abs(best_ones_list[-10] - best_ones_list[0]) < 0.10:
        #     print("Se ha alcanzado un minimo local")
        #     return min(best_ones_list)
        if best == 0:
            print("Se ha alcanzado el resultado optimo")
            return best



print("\nEl mejor resultado obtenido ha sido:", run(), "\n")
#OPCIONES
# Coger la mejor parte de cada padre evaluandolos por partes
# juntar a los mejores padres
# eliminar a un numero n de sujetos y clonar a los mejores (aumentando asi la probabilidad) -> mezclarlos
# mantener un numero de clones de los n mejores en cada ronda


#TAREAS
# hacer que muten mas al principio y menos al final
# evaluar la diversidad genetica en cada ronda
# almacenar los resultados de las rondas y la diversidad genetica
