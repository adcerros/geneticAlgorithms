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
    return initial_poblation, [1000.0 for _ in range(poblations_size)], [evaluate(subject) for subject in initial_poblation], [[] for _ in range(poblations_size)]



#DIVERSIDAD GENETICA!!!!!!!!!!
# genetic_diversity = statistics.mean([statistics.pstdev([elem[column] for elem in poblation]) for column in range(gens_number)])


#Version que toma la ventana en cada iteraccion

#V_1
def variances_mutation(subject_variance, subject_last_results, c=0.817, window_size=10):
    if len(subject_last_results) < window_size:
        return subject_variance, subject_last_results
    elif len(subject_last_results) > window_size:
        subject_last_results.pop(0)
    hit_rate = subject_last_results.count(1) / window_size
    if hit_rate < 0.2:
        return c * subject_variance, subject_last_results
    elif hit_rate > 0.2:
        return subject_variance / c, subject_last_results
    return subject_variance, subject_last_results

# V_2     
# def variances_mutation(subject_variance, subject_last_results, c=0.817, window_size=10):
#     if len(subject_last_results) != window_size:
#         return subject_variance, subject_last_results
#     hit_rate = subject_last_results.count(1) / window_size
#     if hit_rate < 0.2:
#         return c * subject_variance, []
#     elif hit_rate > 0.2:
#         return subject_variance / c, []
#     return subject_variance, []



def mutate_and_compare(subject, subject_variance, subject_fitness, subject_last_results):
    new_subject = [max(min(gen + gauss(0, subject_variance), 180), -180) for gen in subject]
    new_subject_fitness = evaluate(new_subject)
    if new_subject_fitness < subject_fitness:
        subject_last_results.append(1)
        new_subject_variance, new_subject_last_results = variances_mutation(subject_variance, subject_last_results)
        return new_subject, new_subject_variance, new_subject_fitness, new_subject_last_results
    subject_last_results.append(0)
    subject_variance, subject_last_results = variances_mutation(subject_variance, subject_last_results)
    return subject, subject_variance, subject_fitness, subject_last_results



def make_generation(poblation, pob_variances, fitness_matrix, last_results):
    new_poblation, new_pob_variances, new_fitness_matrix, new_last_results = [], [], [], []
    for subject, subject_variance, subject_fitness, subject_last_results in zip(poblation, pob_variances, fitness_matrix, last_results):
        subject, subject_variance, subject_fitness, subject_last_results = mutate_and_compare(subject, subject_variance, subject_fitness, subject_last_results)
        new_poblation.append(subject)
        new_pob_variances.append(subject_variance)
        new_fitness_matrix.append(subject_fitness)
        new_last_results.append(subject_last_results)
    return new_poblation, new_pob_variances, new_fitness_matrix, new_last_results


def run(poblations_size=1, rounds=200, gens_number=4):
    start_time = time.time()
    poblation, pob_variances, fitness_matrix, last_results = create_initial(poblations_size, gens_number)
    data_file = open(str(poblations_size) + "_pob_" +  str(rounds) +  "_runs_.txt", "w+")
    try:
        for i in range(rounds):
            print("\nRealizando generacion", i + 1)
            poblation, pob_variances, fitness_matrix, last_results = make_generation(poblation, pob_variances, fitness_matrix, last_results)
            best_one_fitness = min(fitness_matrix)
            genetic_diversity = statistics.mean([statistics.pstdev([elem[column] for elem in poblation]) for column in range(gens_number)])
            print("Mejor fitness", best_one_fitness, "Diversidad genetica", genetic_diversity)
            data_file.write(str(best_one_fitness) + "," + str(genetic_diversity) + "\n")
            if best_one_fitness <= 1.0e-06:
                data_file.close()
                print("Finalizado con:", poblations_size, "poblacion//", i, "rondas//", poblations_size * i, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
                best_one = poblation[fitness_matrix.index(best_one_fitness)]
                best_one_variance = pob_variances[fitness_matrix.index(best_one_fitness)]
                print("La solucion encontrada es:", best_one, "con un valor de fitness", best_one_fitness, "Varianzas", best_one_variance)
                return
        data_file.close()
        print("Finalizado normal con:", poblations_size, "poblacion//", rounds, "rondas//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")
    except Exception as e:
        data_file.close()
        print("Excepcion con:", poblations_size, "poblacion//", rounds, "rondas//", poblations_size * rounds, "llamadas al sistema//", round((time.time() - start_time) / 60, 2), "min de tiempo transcurrido")


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
[2000, 100000, 4]
])

# /////////////////////




# COMENTAR PARA NO GENERAR LAS GRAFICAS
collect_data()
# /////////////////////
