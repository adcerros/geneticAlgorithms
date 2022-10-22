from time import sleep
import requests
from random import uniform, gauss, randint
import glob
import matplotlib.pyplot as plt
from threading import Thread
import statistics
import time



url = "http://memento.evannai.inf.uc3m.es/age/robot4?"



def my_call(url, subject):
    params = ""
    for i, gen in enumerate(subject, start=1):
        params += "c" + str(i) + "=" + str(gen) + "&"
    try:
        my_request = requests.get(url + params[:-1])
    except:
        print("Intentando reconectar ...")
        sleep(0.2)
        my_call(url, subject)
    return my_request.text


def evaluate(subject):
    return float(my_call(url, subject))


def create_initial(poblations_size, gens_number):
    initial_poblation = [[uniform(-180,180) for _ in range(gens_number)] for _ in range(poblations_size)]
    initial_variances = [[1.0 for _ in range(gens_number)] for _ in range(poblations_size)]
    fitness_matrix = [evaluate(subject) for subject in initial_poblation]
    last_results = [[] for _ in range(poblations_size)]
    return initial_poblation, initial_variances, fitness_matrix, last_results


def mutation(subject, improvements):
    for gen, gen_variance, _ in subject:
        print(gen, gen_variance)
    new_subject = [gen + (gauss(0, gen_variance)) for gen, gen_variance, _ in subject]
    if new_gen < -180:
        new_gen = -180 + uniform(0, 20)
    elif new_gen > 180:
        new_gen = 180 - uniform(0, 20)
    return subject

#DIVERSIDAD GENETICA!!!!!!!!!!
# genetic_diversity = statistics.mean([statistics.pstdev([elem[column] for elem in poblation]) for column in range(gens_number)])

def check_last_results(subject_last_results, window_size=10):
    if len(subject_last_results) < window_size:
        return False




def mutate_and_compare(subject, subject_variances, subject_fitness, subject_last_results):
    new_subject = [(gen + subject_variance) for gen, subject_variance in zip(subject, subject_variances)]
    new_subject_fitness = evaluate(new_subject)
    if new_subject_fitness < subject_fitness:
        subject_last_results



def make_generation(poblation, pob_variances, fitness_matrix, last_results):
    for subject, subject_variance, subject_fitness, subject_last_results in poblation, pob_variances, fitness_matrix, last_results:
        subject, subject_variance, subject_fitness, subject_last_results = mutate_and_compare(subject, subject_variance, subject_fitness, subject_last_results)
    best_one_fitness = min(fitness_matrix)
    best_one = poblation[fitness_matrix.index(best_one_fitness)]
    return poblation, best_one_fitness, best_one


def run(poblations_size=1, rounds=200, gens_number=10):
    start_time = time.time()
    poblation, pob_variances, fitness_matrix, last_results = create_initial(poblations_size, gens_number)
    data_file = open(str(poblations_size) + "_pob_" +  str(rounds) +  "_runs_.txt", "w+")
    try:
        for i in range(rounds):
            print("\nRealizando generacion", i + 1)
            poblation, pob_variances, fitness_matrix, last_results = make_generation(poblation, pob_variances, fitness_matrix, last_results)
            best_one_fitness = min(fitness_matrix)
            best_one = poblation[fitness_matrix.index(best_one_fitness)]
            print("Mejor fitness", best_one_fitness)
            print("Mejor individuo", best_one)
            data_file.write(str(best_one_fitness) + "\n")
            if best_one_fitness == 0:
                data_file.close()
                print("Finalizado con:", poblations_size, "poblacion//", i, "rondas//", poblations_size * i, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
                print("La solucion encontrada es:", best_one, "con un valor de fitness", best_one_fitness)
                return
        data_file.close()
        print("Finalizado con:", poblations_size, "poblacion//", rounds, "rondas//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
    except:
        data_file.close()
        print("Finalizado con:", poblations_size, "poblacion//", rounds, "rondas//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")


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
# params = poblation_size, rounds, gens_number
run_multiple([ 
[10, 500, 4]
])

# /////////////////////




# COMENTAR PARA NO GENERAR LAS GRAFICAS
collect_data()
# /////////////////////
