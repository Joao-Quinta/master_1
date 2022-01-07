# Joao Quinta
# metaheuristique pour l optimisation

import numpy as np
import matplotlib as plt
import copy
import math
import random


def balancedDice(N):
    # same computation as shown in the TP question
    return math.floor(random.random() * N)


def transform_biased_balanced(P):
    minVal = np.min(P)

    # computation of the list containing the real face of the corresponding to each event
    realEvent = []
    for i in range(len(P)):
        for j in range(int(P[i] / minVal)):
            realEvent.append(i)

    return realEvent


def coinToss(p):
    # same computation as shown in the TP question
    return math.floor(random.random() + p)


def biasedDice_biasedCoin(P):
    P_temp = copy.copy(P)
    for i in range(len(P)):
        # we try the first value of P_temp
        first = P_temp.pop(0)
        if coinToss(first) == 1:
            return i
        else:
            # if coin toss 'fails' we normalise the probabilities
            sumP = np.sum(P_temp)
            P_temp = [P_temp[j]/sumP for j in range(len(P_temp))]


def compute_P_comul(P):
    return [np.sum(P[0:j + 1]) for j in range(len(P))]


def rouletteMethod(P_comul):
    val = random.random()
    for i in range(len(P_comul)):
        # we look for the first value larger than the random value we got
        if P_comul[i] > val:
            return i


