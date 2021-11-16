import math
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import time


def extractCities(file):
    data = np.genfromtxt(file, dtype=None, encoding=None, comments='#', delimiter=None)
    x_cc = []
    y_cc = []
    for d in data:
        x_cc.append(d[1])
        y_cc.append(d[2])
    return x_cc, y_cc


def plot_cities_path(path, x_cc, y_cc):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.plot(x_cc[0], y_cc[0], 'ro', label="cities")
    ax1.annotate('start', (x_cc[0], y_cc[0]))
    for i in range(1, len(x_cc)):
        ax1.plot(x_cc[i], y_cc[i], 'ro')
    x_path = []
    y_path = []
    for i in range(len(path)):
        x_path.append(x_cc[path[i]])
        y_path.append(y_cc[path[i]])
    for i in range(1, len(path) - 1):
        ax1.annotate(str(i), (x_cc[path[i]], y_cc[path[i]]))
    energy = compute_energy(path, x_cc, y_cc)
    ax1.plot(x_path, y_path, 'b', label="path")
    ax1.legend()
    ax1.set_title('Energy of path : ' + str(energy), fontsize=16)
    plt.xticks([])
    plt.yticks([])
    plt.show()


def balancedDice(N):
    # same computation as shown in the TP question
    return math.floor(random.random() * N)


# computes the coordinates of n villages if they are all in the unit circle
def compute_n_circle_coordinates(n):
    angle_rad = (360 / n) * 0.0174533
    x = []
    y = []
    for i in range(n):
        x.append(math.cos(i * angle_rad))
        y.append(math.sin(i * angle_rad))
    return x, y


# compute distance between 2 cardinal points -> distance between any two cities
def compute_distance_points(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


# computes a random initial state where we visit all the n cities once, the first city and last are the same an always 0
def compute_random_state(n):
    cities_left = []
    for i in range(1, n):
        cities_left.append(i)

    # always start at city 0
    path = [0]
    while len(cities_left) > 0:
        index = balancedDice(len(cities_left))
        path.append(cities_left[index])
        cities_left.pop(index)

    # back to the beginning
    path.append(0)
    return path


# computes total distance of path, needs coordinates for each city, array for x coordinate and array for y coordinate
def compute_energy(path, x_cc, y_cc):
    distance = 0
    for i in range(len(path) - 1):
        distance = distance + compute_distance_points(x_cc[path[i]], y_cc[path[i]], x_cc[path[i + 1]],
                                                      y_cc[path[i + 1]])
    return distance


# computes a list of all transitions -> [(1, 2), (1, 3), (1, 4), (1, 5) ...] -> we never change the 1st and last city
# path [0, 3, 2, 4, 1, 0] : we can only change the positions of [3, 2, 4, 1]
def compute_possible_transitions(path, v):
    transitions = []
    for i in range(1, len(path) - 1):
        for j in range(i + 1, len(path) - 1):
            transitions.append((i, j))
    if v == 0:
        while len(transitions) > 100:
            transitions.pop(balancedDice(len(transitions)))
    return transitions


# execute all the transitions in the array transitions from the state s
def execute_transitions(s, transitions):
    neighborhood = []
    for transition in transitions:
        s_nei = copy.copy(s)
        s_nei[transition[0]], s_nei[transition[1]] = s_nei[transition[1]], s_nei[transition[0]]
        neighborhood.append(s_nei)
    return neighborhood


def compute_initial_temperature(energy, nei_energy):
    s = 0
    for x in nei_energy:
        s = s + np.abs(energy - x)
    return -((s / len(nei_energy)) / np.log(0.5))


def check_last_three_elements(arr):
    if len(arr) > 2:
        return not (arr[-1] == arr[-2] == arr[-3])
    return True


def simulated_annealing(state, temp, x_cc, y_cc, n):
    energy_state = compute_energy(state, x_cc, y_cc)
    temp_best = []
    while check_last_three_elements(temp_best):
        n_iter = 0  # 100 * n (max)
        n_accept = 0  # 12 * n (max)
        while (n_iter < 100 * n) and (n_accept < 12 * n):
            n_iter = n_iter + 1
            transitions = compute_possible_transitions(state, 1)
            chosen_transition = transitions[balancedDice(len(transitions))]
            state_update = execute_transitions(state, [chosen_transition])[0]
            energy_state_update = compute_energy(state_update, x_cc, y_cc)
            delta_energy = energy_state_update - energy_state
            p = np.min([1, np.exp(-delta_energy / temp)])
            res = math.floor(random.random() + p)
            if res == 1:
                state = state_update
                energy_state = energy_state_update
                n_accept = n_accept + 1
        temp_best.append(energy_state)
        temp = 0.9 * temp
    return state


def generate_random_problem(n):
    x_cc = []
    y_cc = []
    couple = []
    i = 0
    while i < n:
        x = balancedDice(20)
        y = balancedDice(20)
        if (x, y) not in couple:
            couple.append((x, y))
            x_cc.append(x)
            y_cc.append(y)
            i = i + 1
    return x_cc, y_cc


def greedy_implementation(n, file):
    if file == 'cities.dat' or file == 'cities2.dat':
        x_cc, y_cc = extractCities(file)
        n = len(x_cc)
    else:
        x_cc, y_cc = compute_n_circle_coordinates(n)
    path = [0]
    cities_left = []
    for i in range(1, n):
        cities_left.append(i)
    while len(cities_left) > 0:
        dists = []
        for i in range(len(cities_left)):
            dists.append(
                compute_distance_points(x_cc[path[-1]], y_cc[path[-1]], x_cc[cities_left[i]], y_cc[cities_left[i]]))
        index = int(np.argmin(dists))
        path.append(cities_left[index])
        cities_left.pop(index)
    path.append(0)
    plot_cities_path(path, x_cc, y_cc)


def main(n, file):
    if file == 'cities.dat' or file == 'cities2.dat':
        x_cc, y_cc = extractCities(file)
        n = len(x_cc)
    elif file == 'random_gene':
        x_cc, y_cc = generate_random_problem(n)
    else:
        x_cc, y_cc = compute_n_circle_coordinates(n)
    path = compute_random_state(n)
    energy_path = compute_energy(path, x_cc, y_cc)
    transitions = compute_possible_transitions(path, 0)
    path_nei = execute_transitions(path, transitions)
    energy_path_nei = [compute_energy(nei, x_cc, y_cc) for nei in path_nei]
    initial_temp = compute_initial_temperature(energy_path, energy_path_nei)
    #plot_cities_path(path, x_cc, y_cc)
    chosen_path = simulated_annealing(path, initial_temp, x_cc, y_cc, n)
    energy = compute_energy(chosen_path, x_cc, y_cc)
    return chosen_path
    #plot_cities_path(chosen_path, x_cc, y_cc)


# greedy_implementation(16, 'cities2.dat')
current_time = time.time()
x = main(16, 'cities2s.dat')
current_time = time.time() - current_time
print(current_time)

"""
n = 50
greedy ->  136.10167235669732
0  ->  121.8503322693159
1  ->  120.23569535197426
2  ->  115.85840238872018
3  ->  130.1075458925273
4  ->  129.53396256567947
5  ->  130.48577741754957
6  ->  118.1483092082967
7  ->  121.44993783927099
8  ->  129.8973765749438
9  ->  118.996863174492
123.65642026827702

n = 100
greedy ->  205.24900439280066
0  ->  207.05111439506115
1  ->  215.07642718196416
2  ->  196.1505037106572
3  ->  205.2212213745203
4  ->  212.98420769220465
5  ->  196.0480257665792
6  ->  185.1802151759119
7  ->  198.74040572714455
8  ->  201.98329833938433
9  ->  188.22224835558393
200.66576677190113

n = 150
greedy ->  243.7793288034895
0  ->  273.4503517572665
1  ->  246.502732107357
2  ->  264.9290836756653
3  ->  258.1251233223197
4  ->  273.4162694755884
5  ->  266.30214090790764
6  ->  266.9749686722609
7  ->  240.9260684880397
8  ->  253.8887905225519
9  ->  252.35459311878077
259.6870122047738


it 
for n :  50  || count was ->  166428
for n :  100  || count was ->  417140
for n :  150  || count was ->  668437

it_2
for n :  50  || count was ->  158229
for n :  100  || count was ->  441456
for n :  150  || count was ->  773288
"""
