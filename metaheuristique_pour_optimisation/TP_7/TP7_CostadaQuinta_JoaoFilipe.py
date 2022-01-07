import random
import math
import numpy as np


# This is the machine on which programs are executed
# The output is the value on top of the pile. 
class CPU:
    def __init__(self):
        self.pile = []

    def reset(self):
        while len(self.pile) > 0: self.pile.pop()


# These are the instructions
def AND(cpu, data):
    if len(cpu.pile) >= 2 and (cpu.pile[-1] == 1 or cpu.pile[-1] == 0) and (cpu.pile[-2] == 1 or cpu.pile[-2] == 0):
        l = cpu.pile.pop()
        ll = cpu.pile.pop()
        if l == 1 and ll == 1:
            cpu.pile.append(1)
        else:
            cpu.pile.append(0)
        return "done AND"
    else:
        return "error"


def OR(cpu, data):
    if len(cpu.pile) >= 2 and (cpu.pile[-1] == 1 or cpu.pile[-1] == 0) and (cpu.pile[-2] == 1 or cpu.pile[-2] == 0):
        l = cpu.pile.pop()
        ll = cpu.pile.pop()
        if l == 1 or ll == 1:
            cpu.pile.append(1)
        else:
            cpu.pile.append(0)
        return "done OR"
    else:
        return "error"


def XOR(cpu, data):
    if len(cpu.pile) >= 2 and (cpu.pile[-1] == 1 or cpu.pile[-1] == 0) and (cpu.pile[-2] == 1 or cpu.pile[-2] == 0):
        l = cpu.pile.pop()
        ll = cpu.pile.pop()
        if (l == 0 and ll == 1) or (l == 1 and ll == 0):
            cpu.pile.append(1)
        else:
            cpu.pile.append(0)
        return "done XOR"
    else:
        return "error"


def NOT(cpu, data):
    if len(cpu.pile) >= 1 and (cpu.pile[-1] == 1 or cpu.pile[-1] == 0):
        l = cpu.pile.pop()
        if l == 1:
            cpu.pile.append(0)
        else:
            cpu.pile.append(1)
        return "done NOT"
    else:
        return "error"


# Push values of variables on the stack.      
def X1(cpu, data):
    cpu.pile.append(data[0])
    return "done X1"


def X2(cpu, data):
    cpu.pile.append(data[1])
    return "done X2"


def X3(cpu, data):
    cpu.pile.append(data[2])
    return "done X3"


def X4(cpu, data):
    cpu.pile.append(data[3])
    return "done X4"


# Execute a program
def execute(program, cpu, data):
    for i in program:
        if i == "X1":
            a = X1(cpu, data)
        elif i == "X2":
            a = X2(cpu, data)
        elif i == "X3":
            a = X3(cpu, data)
        elif i == "X4":
            a = X4(cpu, data)
        elif i == "AND":
            a = AND(cpu, data)
        elif i == "OR":
            a = OR(cpu, data)
        elif i == "NOT":
            a = NOT(cpu, data)
        elif i == "XOR":
            a = XOR(cpu, data)
        else:
            a = "error"

        if a == "error":
            return "error"
    if len(cpu.pile) > 1:
        return "error"
    else:
        return cpu.pile[0]


# Generate a random program
def randomProg(length, functionSet, terminalSet):
    prog = []
    for i in range(length):
        x = math.floor(random.random() * (len(functionSet) + len(terminalSet)))
        if x >= len(functionSet):
            prog.append(terminalSet[x - len(functionSet)])
        else:
            prog.append(functionSet[x])
    if execute(prog, CPU(), [0, 0, 0, 0]) == "error":
        return randomProg(length, functionSet, terminalSet)
    return prog


# Computes the fitness of a program.
# The fitness counts how many instances of data in dataSet are correctly computed by the program
def computeFitness(prog, cpu, dataSet):
    total = 0
    for data in dataSet:
        a = execute(prog, CPU(), data)
        if a == data[-1]:
            total = total + 1
    return total


# Selection using 2-tournament.
def selection(Population, cpu, dataSet):
    listOfFitness = []
    for i in range(len(Population)):
        prog = Population[i]
        f = computeFitness(prog, cpu, dataSet)
        listOfFitness.append((i, f))

    newPopulation = []
    n = len(Population)
    for i in range(n):
        i1 = random.randint(0, n - 1)
        i2 = random.randint(0, n - 1)
        if listOfFitness[i1][1] > listOfFitness[i2][1]:
            newPopulation.append(Population[i1])
        else:
            newPopulation.append(Population[i2])
    return newPopulation


def crossover(Population, p_c):
    newPopulation = []
    n = len(Population)
    i = 0
    while (i < n):
        p1 = Population[i]
        p2 = Population[(i + 1) % n]
        m = len(p1)
        if random.random() < p_c:  # crossover
            k = random.randint(1, m - 1)
            newP1 = p1[0:k] + p2[k:m]
            newP2 = p2[0:k] + p1[k:m]
            p1 = newP1
            p2 = newP2
        newPopulation.append(p1)
        newPopulation.append(p2)
        i += 2
    return newPopulation


def mutation(Population, p_m, terminalSet, functionSet):
    newPopulation = []
    nT = len(terminalSet) - 1
    nF = len(functionSet) - 1
    for p in Population:
        for i in range(len(p)):
            if random.random() > p_m: continue
            if random.random() < 0.5:
                p[i] = terminalSet[random.randint(0, nT)]
            else:
                p[i] = functionSet[random.randint(0, nF)]
        newPopulation.append(p)
    return newPopulation


def generate_population(size_p, t, functionSet, terminalSet):
    return [randomProg(t, functionSet, terminalSet) for _ in range(size_p)]


def check_viable(population, n_population):
    p = True
    pp = True
    for i in range(min(len(n_population), len(population))):
        if execute(population[i], CPU(), [0, 0, 0, 0, 0]) == "error":
            p = False
        if execute(n_population[i], CPU(), [0, 0, 0, 0, 0]) == "error":
            pp = False
    print(p, pp)
    final_p = []
    for i in range(min(len(n_population), len(population))):

        if execute(n_population[i], CPU(), [0, 0, 0, 0, 0]) == "error":
            final_p.append(population[i])
        else:
            final_p.append(n_population[i])

    ppp = True
    for i in range(len(final_p)):
        if execute(final_p[i], CPU(), [0, 0, 0, 0, 0]) == "error":
            ppp = False

    return final_p


def genetic_algorithm(N, p_m, max_generation, t, functionSet, terminalSet, dataSet, p_c):
    generation = 0
    population = generate_population(N, t, functionSet, terminalSet)
    while generation < max_generation:
        generation = generation + 1
        population = selection(population, CPU(), dataSet)
        population = crossover(population, p_c)
        population = mutation(population, p_m, terminalSet, functionSet)
        # population = check_viable(population, n_population)
    return population[np.argmax([computeFitness(population[i], CPU(), dataSet) for i in range(len(population))])]


# -------------------------------------

# LOOK-UP TABLE YOU HAVE TO REPRODUCE.
nbVar = 4
dataSet = [[0, 0, 0, 0, 0], [0, 0, 0, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 1, 0], [0, 1, 0, 0, 0], [0, 1, 0, 1, 0],
           [0, 1, 1, 0, 0], [0, 1, 1, 1, 1], [1, 0, 0, 0, 0], [1, 0, 0, 1, 1], [1, 0, 1, 0, 0], [1, 0, 1, 1, 0],
           [1, 1, 0, 0, 0], [1, 1, 0, 1, 0], [1, 1, 1, 0, 0], [1, 1, 1, 1, 0]]

# print(dataSet)

cpu = CPU()

# Function and terminal sets.
functionSet = ["AND", "OR", "NOT", "XOR"]
terminalSet = ["X1", "X2", "X3", "X4"]

# Parameters
popSize = 1000
p_c = 0.6
p_m = 0.1
max_generation = 100
progLength = 10
r = []
for i in range(10):
    pr = genetic_algorithm(popSize, p_m, max_generation, progLength, functionSet, terminalSet, dataSet, p_c)
    print(pr, " fit -> ", computeFitness(pr,CPU(), dataSet))
    r.append(computeFitness(pr,CPU(), dataSet))
print("avg -> ", np.sum(r)/len(r))
# Generate the initial population 

# Evolution. Loop on the creation of population at generation i+1 from population at generation i, through selection, crossover and mutation.
