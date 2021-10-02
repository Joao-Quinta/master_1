# Joao Quinta
# metaheuristique pour l optimisation _ TP1

import math
import random
import numpy as np


def compute_fitness(X, k):
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
    return math.floor(random.random() + p)


def generate_X(N):
    X_str = ""
    for _ in range(N):
        X_str += str(coinToss(0.5))
    return X_str


def invert(x_i):
    return str(np.abs(int(x_i) - 1))


def generate_neighbors(X):
    list_neighbors = []
    for i in range(len(X)):
        list_neighbors.append(X[:i] + invert(X[i]) + X[i + 1:])
    return list_neighbors


def find_best_in_neighborhood(array_neighbors, k):
    max_fitness_value = -1
    best_x = ""
    for neighbor in array_neighbors:
        neighbor_fit = compute_fitness(neighbor, k)
        if neighbor_fit > max_fitness_value:
            max_fitness_value = neighbor_fit
            best_x = neighbor

    return best_x, max_fitness_value


def compute_probabilistic_neighborhood(array_neighbors, k, best_ever):
    array_neighbors_fitness = [compute_fitness(neighbor, k) for neighbor in array_neighbors]
    if best_ever < np.max(array_neighbors_fitness):
        return array_neighbors[np.argmax(array_neighbors_fitness)], np.max(array_neighbors_fitness)
    array_neighbors_fitness = array_neighbors_fitness / np.sum(array_neighbors_fitness)
    return array_neighbors_fitness


def compute_P_comul(P):
    return [np.sum(P[0:j + 1]) for j in range(len(P))]


def rouletteMethod(P_comul):
    val = random.random()
    for i in range(len(P_comul)):
        # we look for the first value larger than the random value we got
        if P_comul[i] > val:
            return i


def hamming_distance(str1, str2):
    dif = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            dif += 1
    return dif


def deterministic_hill_climb(N, k):
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
    X = generate_X(N)
    X_fitness = compute_fitness(X, k)
    X_neighbors = generate_neighbors(X)
    all_time_X = [X]
    all_time_fitness = [X_fitness]
    all_time_best_fitness = X_fitness
    for _ in range(10):
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


"""
X = generate_X(5)
print(X)
X_neighbors = generate_neighbors(X)
print(X_neighbors)


array_neighbors1 = ["001", "001", "000", "111"]
k1 = 0
print(deterministic_hill_climb(50, 0))
x = compute_probabilistic_neighborhood(array_neighbors1, k1, 0)
print(x)
if type(x) is tuple:
    print("sa")
"""
