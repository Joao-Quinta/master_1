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


# randomly generates population, an individual is a concatenation of x and y in binary form, x and y are 10 bits each
# x and y are number between 10 and 1000
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


# maps binary value to real number between 10 and 1000
def map_value(v):
    return ((v / np.power(2, 10)) * (1000 - 10)) + 10


# computes fitness of an individual
def compute_fitness(individual):
    x = map_value(int(individual[:10], 2))
    y = map_value(int(individual[10:], 2))
    return - np.abs((x / 2) * np.sin(np.sqrt(np.abs(x)))) - np.abs(y * np.sin(np.power(np.abs(x / y), (1 / 30))))


# selection step, randomly selects individual from the population with weighted randomness based on fitness
def selection_random(population):
    fit_population = [compute_fitness(population[i]) for i in range(len(population))]
    fit_total = np.sum(fit_population)
    random_weights = [fit_population[i] / fit_total for i in range(len(fit_population))]
    return [fit_population[rouletteMethod(random_weights)] for _ in
            range(len(population))]


# selection step, based on tournament 5 strategy
def selection_tournament_5(population):
    new_gen_pop = []
    fit_population = [compute_fitness(population[i]) for i in range(len(population))]
    for l in range(len(population)):
        index_of_selection = [balancedDice(len(population)) for _ in range(5)]
        selection_of_5 = [fit_population[i] for i in index_of_selection]
        new_gen_pop.append(population[index_of_selection[np.argmax(selection_of_5)]])
    return new_gen_pop


# crossing of population with probability 0.6
def crossing(population):
    i = 0
    while i < len(population):
        if random.random() < 0.6:
            x1, x1_ = population[i][:5], population[i + 1][:5]
            x2, x2_ = population[i][5:10], population[i + 1][5:10]
            y1, y1_ = population[i][10:15], population[i + 1][10:15]
            y2, y2_ = population[i][15:], population[i + 1][15:]
            population[i] = x1 + x2_ + y1 + y2_
            population[i + 1] = x1_ + x2 + y1_ + y2
        i = i + 2
    return population


# computes mutations
def mutation(population, p):
    for i in range(len(population)):
        individual = list(population[i])
        for j in range(len(individual)):
            if random.random() < p:
                if individual[j] == '0':
                    individual[j] = '1'
                else:
                    individual[j] = '0'
        population[i] = ''.join(individual)
    return population


# global function
def genetic_algorithm(N, p, max_generation):
    generation = 0
    population = generate_population(N)
    while generation < max_generation:
        generation = generation + 1
        population = selection_tournament_5(population)
        # population = crossing(population)
        population = mutation(population, p)
    return population[np.argmax([compute_fitness(population[i]) for i in range(len(population))])]


x = [10, 100, 1000, 10000, 100000]
for x_ in x:
    r = genetic_algorithm(100, 0.01, x_)
    print(r, " - > ", compute_fitness(r))

"""
WITH CROSSING : 

p = 0.1

00100110100000000000  - >  -11.966731164990291
00000000010000000110  - >  -14.119453180124616
00000000000000000000  - >  -8.518127505726877
00000111100000000001  - >  -10.213980556320166
00000000000000000001  - >  -9.313415632112324

p = 0.01
00000111100000000000  - >  -9.394785809777554
00000111100000000000  - >  -9.394785809777554
00111101010000000000  - >  -9.460929749396577
00100110010000000000  - >  -8.915082864815007
01111010100000000000  - >  -9.737136305702137

WITHOUT CROSSING : 

p = 0.1
00010100010000000100  - >  -13.331906952554519
00000000000000000000  - >  -8.518127505726877
00000000000000000001  - >  -9.313415632112324
00000000000000000000  - >  -8.518127505726877
00000000000000000000  - >  -8.518127505726877

p = 0.01
00111101010000000000  - >  -9.460929749396577
10100000110000000000  - >  -9.147215243893433
00000000000000000000  - >  -8.518127505726877
00000000000000000000  - >  -8.518127505726877
00111101010000000000  - >  -9.460929749396577

"""