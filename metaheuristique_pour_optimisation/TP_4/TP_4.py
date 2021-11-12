import math
import random
import copy
import numpy as np
import matplotlib.pyplot as plt


def rouletteMethod(P_comul):
    val = random.random()
    for i in range(len(P_comul)):
        # we look for the first value larger than the random value we got
        if P_comul[i] > val:
            return i


def compute_P_comul(P):
    return [np.sum(P[0:j + 1]) for j in range(len(P))]


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


# computes total distance of path, needs coordinates for each city, array for x coordinate and array for y coordinate
def compute_energy(path, x_cc, y_cc):
    distance = 0
    for i in range(len(path) - 1):
        distance = distance + compute_distance_points(x_cc[path[i]], y_cc[path[i]], x_cc[path[i + 1]],
                                                      y_cc[path[i + 1]])
    return distance


# computes matrix D -> D[i][j] = distance between city i and j -> D[i][j] = D[j][i]
def compute_distance_matrix(x_cc, y_cc):
    dists = []
    for i in range(len(x_cc)):
        dist_i = []
        for j in range(len(x_cc)):
            dist_i.append(compute_distance_points(x_cc[i], y_cc[i], x_cc[j], y_cc[j]))
        dists.append(dist_i)
    return dists


# computes 1/d[i][j]
def compute_inverse_distance(d):
    n_ = copy.deepcopy(d)
    for i in range(len(n_)):
        for j in range(len(n_[i])):
            if n_[i][j] != 0:
                n_[i][j] = 1 / n_[i][j]
    return n_


def initialize_tao(n, v):
    tao = []
    for i in range(n):
        arr = []
        for j in range(n):
            arr.append(v)
        tao.append(arr)
    return tao


def print_matrix(m):
    print(len(m), " x ", len(m[0]))
    for i in range(len(m)):
        print(m[i])


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
    dist = compute_energy(path, x_cc, y_cc)
    return path, dist
    # plot_cities_path(path, x_cc, y_cc)


def ant_system_formula_1(current_pos, tao, n_, a, b, unvisited):
    p_ = []
    for i in range(len(unvisited)):
        p_.append(np.power(tao[current_pos][unvisited[i]], a) * np.power(n_[current_pos][unvisited[i]], b))
    p_ = p_ / np.sum(p_)
    return p_


def ant_system_formula_2(tao, p, new_pheromones):
    new_tao = copy.deepcopy(tao)
    for i in range(len(tao)):
        for j in range(i, len(tao[i])):
            new_val = (tao[i][j] * (1 - p)) + new_pheromones[i][j]
            new_tao[i][j] = new_val
            new_tao[j][i] = new_val
    return new_tao


def ant_system_formula_3(current_it_trail, path, path_energy, Q):
    new_trail = copy.deepcopy(current_it_trail)
    val = Q / path_energy
    for i in range(len(path) - 2):
        new_trail[path[i]][path[i + 1]] = new_trail[path[i]][path[i + 1]] + val
    return new_trail


# computes matrix of size n x n where we will keep the pheromones total for the iteration
def initialize_pheromone(n):
    total_pheromone_iteration = []
    for _ in range(n):
        it = []
        for _2 in range(n):
            it.append(0)
        total_pheromone_iteration.append(it)
    return total_pheromone_iteration


def ant_system_algorithm(a, b, p, Q, tao, tmax, k, i_distance, x_cc, y_cc):
    best_over_path = []
    cost_best_over_path = np.inf
    for t in range(tmax):
        best_path = []
        cost_best_path = np.inf
        pheromone = initialize_pheromone(len(x_cc))
        for ant in range(k):
            cities_to_visit = []
            for i in range(1, len(x_cc)):
                cities_to_visit.append(i)
            ant_path = [0]
            while len(cities_to_visit) > 0:
                p_ = ant_system_formula_1(ant_path[-1], tao, i_distance, a, b, cities_to_visit)
                p_comul = compute_P_comul(p_)
                next_city_index = rouletteMethod(p_comul)
                ant_path.append(cities_to_visit[next_city_index])
                cities_to_visit.pop(next_city_index)
            ant_path.append(0)
            energy_ant_path = compute_energy(ant_path, x_cc, y_cc)
            pheromone = ant_system_formula_3(pheromone, ant_path, energy_ant_path, Q)

            if energy_ant_path < cost_best_path:
                best_path = copy.copy(ant_path)
                cost_best_path = energy_ant_path

        tao = ant_system_formula_2(tao, p, pheromone)

        if cost_best_path < cost_best_over_path:
            cost_best_over_path = cost_best_path
            best_over_path = best_path
        print("at iteration : ", t, " - cost of best path found is : ", cost_best_over_path)

    return best_over_path, cost_best_over_path


# #### CONSTANTS ETC
chosen_problem = 'cities2.dat'
x_cc, y_cc = extractCities(chosen_problem)
alpha = 1
beta = 5
small_p = 0.1
path_greedy, dist_path_greedy = greedy_implementation(chosen_problem, chosen_problem)
L_nn = dist_path_greedy
tao_0 = 1 / L_nn
tao_init = initialize_tao(len(x_cc), tao_0)
distance_matrix = compute_distance_matrix(x_cc, y_cc)
inverse_distance = compute_inverse_distance(distance_matrix)
t_max = 5
k = len(x_cc) * 50

p, c = ant_system_algorithm(alpha, beta, small_p, L_nn, tao_init, t_max, k, inverse_distance, x_cc, y_cc)
plot_cities_path(p, x_cc, y_cc)