from time import sleep
import requests
from random import uniform, gauss, randint
import glob
import matplotlib.pyplot as plt
from threading import Thread
import statistics
import time


url = "http://memento.evannai.inf.uc3m.es/age/robot4?"



def my_call(url, chromosome):
    params = ""
    for i, gen in enumerate(chromosome, start=1):
        params += "c" + str(i) + "=" + str(gen) + "&"
    try:
        my_request = requests.get(url + params[:-1])
    except:
        print("Intentando reconectar ...")
        sleep(0.2)
        my_call(url, chromosome)
    return my_request.text


def evaluate(poblation):
    return [float(my_call(url, elem)) for elem in poblation]


def create_initial(poblations_size, gens_number):
    return [[uniform(-180,180) for _ in range(gens_number)] for _ in range(poblations_size)]


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


def mutation(son, gens_number, mutation_factor, standard_derivation, mean=0):
    if randint(0,100) < mutation_factor:
        pos = randint(0, gens_number - 1)
        new_gen = son[pos] + (gauss(mean, standard_derivation))
        # PONER AQUI UNA VARIABLE DE LIMITE MAXIMO Y MINIMO Y UN ALEATORIO PARA QUE NO CONVERJAN A LOS VALORES DE 180 
        # ES DECIR QUE SEA 180 +/- NUM_ALEATORIO
        if new_gen < -180:
            new_gen = -180 + uniform(0, 20)
        elif new_gen > 180:
            new_gen = 180 - uniform(0, 20)
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
    return new_poblation, best_one_fitness, genetic_diversity, best_one


def run(poblations_size=200, rounds=200, mutation_factor=5, gens_number=10, tournament_size=2, standard_derivation=15):
    start_time = time.time()
    poblation = create_initial(poblations_size, gens_number)
    genetic_diversity = statistics.mean([statistics.pstdev([elem[column] for elem in poblation]) for column in range(gens_number)])
    data_file = open(str(poblations_size) + "_pob_" +  str(rounds) +  "_runs_" + str(mutation_factor) + "_mut_" + str(tournament_size) + "_tornmnt_siz_" + str(standard_derivation) + "_std_dev.txt", "w+")
    try:
        for i in range(rounds):
            print("\nRealizando generacion", i)
            # Calculo dinamico del factor de mutacion y su desviacion tipica
            mutation_factor = min(max(int((100 - genetic_diversity) / 8), 3), 25)
            standard_derivation = min(max(100 - int(genetic_diversity), 10), 150)
            poblation, best_one_fitness, genetic_diversity, best_one = make_generation(poblation, mutation_factor, gens_number, tournament_size, standard_derivation)
            print("Mejor fitness", best_one_fitness, "Diversidad genetica", genetic_diversity)
            print("Mejor individuo", best_one)
            data_file.write(str(best_one_fitness) + "," + str(genetic_diversity) + "\n")
            if best_one_fitness == 0:
                data_file.close()
                print("Finalizado con:", poblations_size, "poblacion//", i, "rondas//", mutation_factor, "factor de mutacion//", tournament_size, "tamaño de torneo//", poblations_size * i, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
                print("La solucion encontrada es:", best_one, "con un valor de fitness", best_one_fitness)
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


def run_multiple(params):
    threads = [Thread(target=run, args=param) for param in params]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()







# COMENTAR SI SE DESEA UNICAMENTE GENERAR LAS GRAFICAS
# params = poblation_size, rounds, mutation_factor, gens_number, tournament_size, standard_derivation
run_multiple([ 
[100, 50, 10, 4, 4, 20]
])

# /////////////////////




# COMENTAR PARA NO GENERAR LAS GRAFICAS
collect_data()
# /////////////////////
