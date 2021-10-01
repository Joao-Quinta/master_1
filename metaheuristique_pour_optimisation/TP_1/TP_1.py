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


def deterministic_hill_climb(N, k):
    X = generate_X(N)
    X_fitness = compute_fitness(X, k)
    X_neighbors = generate_neighbors(X)
    com = 0
    while True:
        X_neighbors_fitness_str, X_neighbors_fitness_val, = find_best_in_neighborhood(X_neighbors, k)
        if X_neighbors_fitness_val > X_fitness:
            X = X_neighbors_fitness_str
            X_fitness = X_neighbors_fitness_val
            X_neighbors = generate_neighbors(X)
            com = com + 1
        else:
            print(com)
            break
    return X


"""
X = generate_X(5)
print(X)
X_neighbors = generate_neighbors(X)
print(X_neighbors)
"""
print(deterministic_hill_climb(50, 2))
