import numpy as np
import matplotlib as plt
import math
import random


# N -> number of faces, n -> number of rolls
def balancedDice(N, n):
    print()
    print("balanced dice: ", n, " rolls, ", N, " sides.")
    print()
    arr = [math.floor(random.random() * N) for _ in range(n)]

    for i in range(0, N):
        print("val -> ", i, " : ", arr.count(i))


balancedDice(6, 1000)


# P -> array of probabilities, n -> number of rolls
def biasedDice(P, n):
    print()
    print("biased dice: ", n, " rolls, ", P, " Pi")
    print()
    min = np.min(P)

    realEvent = []
    for i in range(len(P)):
        for j in range(int(P[i] / min)):
            realEvent.append(i)

    arr = [realEvent[math.floor(random.random() * int(1 / min))] for _ in range(n)]

    for i in range(0, len(P)):
        print("val -> ", i, " : ", arr.count(i))


biasedDice([1 / 4, 1 / 4, 1 / 4, 1 / 8, 1 / 16, 1 / 16], 1000)


# p = probability of tail, n = number o tosses
def coinToss(p, n):
    print()
    print("coin toss: ", n, " tosses, ", p, " probability of tail")
    print()

    # gamma is either 1 or 0 -> arr is filled with 0 and 1
    # 1 has probability of p, and 0 probability of 1 - p
    # lets say p = 1, math.floor(random.random() + p) = 1, for all random.random()
    # 1 is tail, 0 is head
    arr = [math.floor(random.random() + p) for _ in range(n)]

    print("tail -> ", arr.count(1))
    print("head -> ", arr.count(0))

    arr = np.array(arr)
    arr = arr * p + (1 - arr) * (1 - p)

    for un in np.unique(arr):
        print(un, " -> ", np.where(arr = un))


coinToss(0.7, 1000)
