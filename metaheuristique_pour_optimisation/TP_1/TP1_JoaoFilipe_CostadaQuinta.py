# Joao Quinta
# metaheuristique pour l optimisation _ TP1

import math
import random
import numpy as np


def compute_fitness(X, k):
    # computes fitness of an x -> based on the tables found in hte pdf
    fitness = 0
    if k == 0:
        for i in range(len(X) - k):
            str_comp = X[i:i + 1 + k]
            if str_comp == "0":
                val = 2
            else:
                val = 1
            fitness = fitness + val

    elif k == 1:
        for i in range(len(X) - k):
            str_comp = X[i:i + 1 + k]
            if str_comp == "00":
                val = 2
            elif str_comp == "01":
                val = 3
            elif str_comp == "10":
                val = 2
            else:
                val = 0
            fitness = fitness + val

    else:
        for i in range(len(X) - k):
            str_comp = X[i:i + 1 + k]
            if str_comp == "001" or str_comp == "010":
                val = 1
            elif str_comp == "100":
                val = 2
            else:
                val = 0
            fitness = fitness + val

    return fitness


def coinToss(p):
    # same computation as shown in the TP question
    # taken from TP0 code, used to compute each bit -> 0 or 1 p is always 0.5
    return math.floor(random.random() + p)


def generate_X(N):
    # generates X of size N using coin toss
    X_str = ""
    for _ in range(N):
        X_str += str(coinToss(0.5))
    return X_str


def invert(x_i):
    # if input is 1 output is 0, if input is 0 output is 1
    return str(np.abs(int(x_i) - 1))


def generate_neighbors(X):
    # for every bit in X, it generates a new X' neighbor to X, that is at 1 hamming distance
    list_neighbors = []
    for i in range(len(X)):
        list_neighbors.append(X[:i] + invert(X[i]) + X[i + 1:])
    return list_neighbors


def find_best_in_neighborhood(array_neighbors, k):
    # it computes all the fitness of the neighborhood, to find the best one, and returns it
    max_fitness_value = -1
    best_x = ""
    for neighbor in array_neighbors:
        neighbor_fit = compute_fitness(neighbor, k)
        if neighbor_fit > max_fitness_value:
            max_fitness_value = neighbor_fit
            best_x = neighbor

    return best_x, max_fitness_value


def compute_probabilistic_neighborhood(array_neighbors, k, best_ever):
    # it computes all the fitness of the neighborhood
    # if it finds one that is best fitted than the best_ever it returns it
    # if it doesnt, it returns a normalised probability for each neighbor
    array_neighbors_fitness = [compute_fitness(neighbor, k) for neighbor in array_neighbors]
    if best_ever < np.max(array_neighbors_fitness):
        return array_neighbors[np.argmax(array_neighbors_fitness)], np.max(array_neighbors_fitness)
    array_neighbors_fitness = array_neighbors_fitness / np.sum(array_neighbors_fitness)
    return array_neighbors_fitness


def compute_P_comul(P):
    # computes p comul from TP0, required for the roulette method
    return [np.sum(P[0:j + 1]) for j in range(len(P))]


def rouletteMethod(P_comul):
    val = random.random()
    for i in range(len(P_comul)):
        # we look for the first value larger than the random value we got
        if P_comul[i] > val:
            return i


def hamming_distance(str1, str2):
    # computes hamming distance
    dif = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            dif += 1
    return dif


def compute_all_distances(array_X):
    # computes the all the hamming distances between all the X in the array
    return [hamming_distance(array_X[i], array_X[j]) for i in range(len(array_X)) for j in range(i + 1, len(array_X))]


def deterministic_hill_climb(N, k):
    # main function that implements the deterministic hill climbing, explained in the pdf file
    X = generate_X(N)
    X_fitness = compute_fitness(X, k)
    X_neighbors = generate_neighbors(X)
    while True:
        X_neighbors_fitness_str, X_neighbors_fitness_val = find_best_in_neighborhood(X_neighbors, k)
        if X_neighbors_fitness_val > X_fitness:
            X = X_neighbors_fitness_str
            X_fitness = X_neighbors_fitness_val
            X_neighbors = generate_neighbors(X)
        else:
            break

    return X


def probabilistic_hill_climb(N, k):
    # main function that implements the probabilistic hill climbing, explained in the pdf file
    if k == 0:
        r = 11 * 10
    elif k == 1:
        r = 6 * 10
    else:
        r = 6 * 10
    X = generate_X(N)
    X_fitness = compute_fitness(X, k)
    X_neighbors = generate_neighbors(X)
    all_time_X = [X]
    all_time_fitness = [X_fitness]
    all_time_best_fitness = X_fitness
    for _ in range(r):
        X_neighbors_fitness = compute_probabilistic_neighborhood(X_neighbors, k, all_time_best_fitness)
        if type(X_neighbors_fitness) is tuple:
            X = X_neighbors_fitness[0]
            all_time_best_fitness = X_neighbors_fitness[1]
        else:
            p_comul = compute_P_comul(X_neighbors_fitness)
            X = X_neighbors[rouletteMethod(p_comul)]
        all_time_X.append(X)
        all_time_fitness.append(compute_fitness(X, k))
        X_neighbors = generate_neighbors(X)
    return all_time_X[np.argmax(all_time_fitness)]


def main(N, k, r, mode):
    all_x_max = []
    if mode == "deterministic":
        for i in range(r):
            all_x_max.append(deterministic_hill_climb(N, k))
    elif mode == "probabilistic":
        for i in range(r):
            all_x_max.append(probabilistic_hill_climb(N, k))
    # distances_to_plot = compute_all_distances(all_x_max)
    return all_x_max
