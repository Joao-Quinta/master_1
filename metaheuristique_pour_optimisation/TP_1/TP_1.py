# Joao Quinta
# metaheuristique pour l optimisation _ TP1

import math
import random
import numpy as np


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


X = generate_X(5)
print(X)
X_neighbors = generate_neighbors(X)
print(X_neighbors)

# 1110 - 0010 - 0100 - 0111
