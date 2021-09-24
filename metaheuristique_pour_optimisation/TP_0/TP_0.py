# Joao Quinta
# metaheuristique pour l optimisation

import numpy as np
import functions


# N -> number of faces, n -> number of rolls
def exo_1(N, n):
    print()
    print("balanced dice: ", n, " rolls, ", N, " sides.")
    print()
    arr = [functions.balancedDice(N) for _ in range(n)]

    for i in range(0, N):
        print("val -> ", i, " : ", arr.count(i))


exo_1(6, 1000)


# P -> array of probabilities, n -> number of rolls
def exo_2(P, n):
    print()
    print("biased dice: ", n, " rolls, ", P, " -> Pi")
    print()

    transformed_dice = functions.transform_biased_balanced(P)
    number_of_faces = len(transformed_dice)

    arr = [transformed_dice[functions.balancedDice(number_of_faces)] for _ in range(n)]

    for i in range(0, len(P)):
        print("val -> ", i, " : ", arr.count(i))


exo_2([1 / 4, 1 / 4, 1 / 4, 1 / 8, 1 / 16, 1 / 16], 1000)


# p = probability of tail, n = number o tosses, type -> fast use with other function
def exo_3(p, n):
    print()
    print("coin toss: ", n, " tosses, ", p, " probability of tail")
    print()

    # gamma is either 1 or 0 -> arr is filled with 0 and 1
    # 1 has probability of p, and 0 probability of 1 - p
    # lets say p = 1, math.floor(random.random() + p) = 1, for all random.random()
    # 1 is tail, 0 is head
    arr = [functions.coinToss(p) for _ in range(n)]

    print("tail -> ", arr.count(1))
    print("head -> ", arr.count(0))

    arr = np.array(arr)
    arr = arr * p + (1 - arr) * (1 - p)


exo_3(0.7, 1000)


# n -> number of rolls, P -> probabilities
def exo_4(P, n):
    print()
    print("dice roll (biased coin): ", n, " rolls, ", P, " -> Pi")
    print()

    arr = [functions.biasedDice_biasedCoin(P) for _ in range(n)]

    for i in range(0, len(P)):
        print("val -> ", i, " : ", arr.count(i))


exo_4([1 / 4, 1 / 4, 1 / 4, 1 / 8, 1 / 16, 1 / 16], 1000)


# n -> number of rolls, P -> probabilities
def exo_5(P, n):
    print()
    print("roulette roll: ", n, " rolls, ", P, " -> Pi")
    print()

    P_comul = functions.compute_P_comul(P)

    arr = [functions.rouletteMethod(P_comul) for _ in range(n)]

    for i in range(0, len(P)):
        print("val -> ", i, " : ", arr.count(i))


exo_5([1 / 4, 1 / 4, 1 / 4, 1 / 8, 1 / 16, 1 / 16], 1000)
