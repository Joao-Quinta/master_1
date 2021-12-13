import numpy as np
import random
import math


def balancedDice(N):
    # same computation as shown in the TP question
    return math.floor(random.random() * N)


def compute_P_comul(P):
    return [np.sum(P[0:j + 1]) for j in range(len(P))]


def rouletteMethod(P_comul):
    val = random.random()
    for i in range(len(P_comul)):
        # we look for the first value larger than the random value we got
        if P_comul[i] > val:
            return i


def generate_population(N):
    population = []
    for _ in range(N):
        x = bin(balancedDice(990) + 10)[2:]
        y = bin(balancedDice(990) + 10)[2:]
        while len(x) < 10:
            x = '0' + x
        while len(y) < 10:
            y = '0' + y
        population.append(x + y)
    return population


def map_value(v):
    return ((v / np.power(2, 10)) * (1000 - 10)) + 10


# TODO -> compute fitness function, receives single individual
def compute_fitness(individual):
    x = map_value(int(individual[:10], 2))
    y = map_value(int(individual[10:], 2))
    return - np.abs((x/2) * np.sin(np.sqrt(np.abs(x)))) - np.abs(y * np.sin(np.power(np.abs(x/y), (1/30))))


# selection step, randomly selects individual from the population with weighted randomness based on fitness
def selection_random(population):
    fit_population = [compute_fitness(population[i]) for i in range(len(population))]
    fit_total = np.sum(fit_population)
    random_weights = [fit_population[i] / fit_total for i in range(len(fit_population))]
    return [fit_population[rouletteMethod(random_weights)] for _ in
            range(len(population))]  # TODO check if this works well


# selection step, based on tournament 5 strategy
def selection_tournament_5(population):  # TODO check if this works well
    new_gen_pop = []
    fit_population = [compute_fitness(population[i]) for i in range(len(population))]
    for l in range(len(population)):
        index_of_selection = [balancedDice(len(population)) for _ in range(5)]
        selection_of_5 = [fit_population[i] for i in index_of_selection]
        new_gen_pop.append(population[index_of_selection[np.argmax(selection_of_5)]])
    return new_gen_pop


pop = generate_population(100)
fit = [compute_fitness(pop[i]) for i in range(len(pop))]
print(fit)
print(np.max(fit))

