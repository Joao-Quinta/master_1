# TP2_JoaoFilipe_CostadaQuinta
# meta
import numpy as np
import math
import random
import copy

# size of problem
n = 12
l = 1
t_max = 5000

# drs is a distance between locations r and s
D = np.array([[0, 1, 2, 3, 1, 2, 3, 4, 2, 3, 4, 5],
              [1, 0, 1, 2, 2, 1, 2, 3, 3, 2, 3, 4],
              [2, 1, 0, 1, 3, 2, 1, 2, 4, 3, 2, 3],
              [3, 2, 1, 0, 4, 3, 2, 1, 5, 4, 3, 2],
              [1, 2, 3, 4, 0, 1, 2, 3, 1, 2, 3, 4],
              [2, 1, 2, 3, 1, 0, 1, 2, 2, 1, 2, 3],
              [3, 2, 1, 2, 2, 1, 0, 1, 3, 2, 1, 2],
              [4, 3, 2, 1, 3, 2, 1, 0, 4, 3, 2, 1],
              [2, 3, 4, 5, 1, 2, 3, 4, 0, 1, 2, 3],
              [3, 2, 3, 4, 2, 1, 2, 3, 1, 0, 1, 2],
              [4, 3, 2, 3, 3, 2, 1, 2, 2, 1, 0, 1],
              [5, 4, 3, 2, 4, 3, 2, 1, 3, 2, 1, 0]])

# wij is the flow between facilities i and j
W = np.array([[0, 5, 2, 4, 1, 0, 0, 6, 2, 1, 1, 1],
              [5, 0, 3, 0, 2, 2, 2, 0, 4, 5, 0, 0],
              [2, 3, 0, 0, 0, 0, 0, 5, 5, 2, 2, 2],
              [4, 0, 0, 0, 5, 2, 2, 10, 0, 0, 5, 5],
              [1, 2, 0, 5, 0, 10, 0, 0, 0, 5, 1, 1],
              [0, 2, 0, 2, 10, 0, 5, 1, 1, 5, 4, 0],
              [0, 2, 0, 2, 0, 5, 0, 10, 5, 2, 3, 3],
              [6, 0, 5, 10, 0, 1, 10, 0, 0, 0, 5, 0],
              [2, 4, 5, 0, 0, 1, 5, 0, 0, 0, 10, 10],
              [1, 5, 2, 0, 5, 5, 2, 0, 0, 0, 5, 0],
              [1, 0, 2, 5, 1, 4, 3, 5, 10, 5, 0, 2],
              [1, 0, 2, 5, 1, 0, 3, 0, 10, 0, 2, 0]])

# a state will be of form : [12,11,10,9,8,7,6,5,4,3,2,1]
# it means that:
# facility 12 is in location 1
# facility 11 is in location 2
# facility 10 is in location 3

# ...

# facility s[i] is in location i

tabu_list = np.zeros((12, 12))
print(tabu_list)
# represents the forbidden transitions, known as the short term memory
# each row represents a facility and the collum the position
# if tabu_list[i][j] = l -> facility i can't be placed in position j for the next l moves
# if tabu_list[i][j] = 0 -> transition is legal
print()
diversification_meca = np.zeros((12, 12))
print(diversification_meca)


# represents the transitions we want to prioritise, known as the long term memory
# if diversification_meca[i][j] = n^2 -> facility i must be placed in position j in the next move

# ######################################################  functions

# taken from tp0 -> used for generation of random initial state
def balancedDice(N):
    return math.floor(random.random() * N)


# create a random array with all the facilities placed in random locations
def generate_random_state():
    facilities = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    s = []
    while len(facilities) > 0:
        i = balancedDice(len(facilities))
        s.append(facilities[i])
        facilities.pop(i)
    return s


# simple fitness computation
def compute_fitness(s):
    total_fit = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            distance = D[i][j]
            weight = W[s[i]][s[j]]
            total_fit = total_fit + distance * weight
    return total_fit * 2


# checks forced transitions -> diversication mecanism -> if a forced transition happens to be a forbiden transition:
# it won't be selected as a transition
# for example we have a forced transition to place facility 3 in village 2
# but the facility in villace 2, is forbidden from being placed in the village in which facility 3 is
# -> we can't make the switch -> mast want until the move is legal
def check_forced_transitions(s):
    transitions = []
    u = n * n
    for i in range(diversification_meca.shape[0]):
        for j in range(diversification_meca.shape[1]):
            if diversification_meca[i][j] == u:
                transition = (s.index(i), j)
                if tabu_list[s[j]][transition[0]] == 0:
                    transitions.append(transition)
    return transitions


# for all transitions, we check if they are legal -> according to the tabu list
def check_transitions(s, transitions):
    post_tr = copy.deepcopy(transitions)
    to_delete = []
    i = 0
    while i < len(transitions):
        city_from = transitions[i][0]  # transitions[i][0] -> city from
        city_to = transitions[i][1]  # transitions[i][1] -> city to
        facility_in_city_from = s[transitions[i][0]]  # s[transitions[i][0]] -> facility in city from
        facility_in_city_to = s[transitions[i][1]]  # s[transitions[i][1]] -> facility in city to
        # if either tabu_list[facility_from_to][city_to_from] > 0 -> locked transition -> we delete it
        if tabu_list[facility_in_city_from][city_to] > 0 or tabu_list[facility_in_city_to][city_from] > 0:
            to_delete.append(i)
        i = i + 1
    i = len(to_delete) - 1
    while i > -1:
        post_tr.pop(to_delete[i])
        i = i - 1
    return post_tr


# compute all transitions -> checks if there are forced and forbidden transitions
def compute_transitions(s):
    transitions = check_forced_transitions(s)
    if len(transitions) > 0:
        return transitions
    transitions = []
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            transitions.append((i, j))
    transitions = check_transitions(s, transitions)
    return transitions


# execute all the transitions in the array transitions from the state s
def execute_transitions(s, transitions):
    neighborhood = []
    for transition in transitions:
        s_nei = copy.copy(s)
        s_nei[transition[0]], s_nei[transition[1]] = s_nei[transition[1]], s_nei[transition[0]]
        neighborhood.append(s_nei)
    return neighborhood


# update tabu list as well as diversification mechanism list
def update_tabu_diversification_meca(s, transition):
    for i in range(tabu_list.shape[0]):
        for j in range(tabu_list.shape[1]):
            if tabu_list[i][j] > 0:
                tabu_list[i][j] = tabu_list[i][j] - 1
            if diversification_meca[i][j] < n * n:
                diversification_meca[i][j] = diversification_meca[i][j] + 1
    tabu_list[s[transition[0]]][transition[0]] = l
    tabu_list[s[transition[1]]][transition[1]] = l
    diversification_meca[s[transition[0]]][transition[0]] = 0
    diversification_meca[s[transition[1]]][transition[1]] = 0


# compute fitness but FASTER -> CODE GO BRRRRR!
def faster_compute_fitness(s, fit, transition):
    c_fit = copy.copy(fit)
    transition_fitness = []
    for i in range(tabu_list.shape[0]):
        c_fit = c_fit - D[transition[0]][i] * W[s[transition[0]]][s[i]]
        c_fit = c_fit - D[transition[1]][i] * W[s[transition[1]]][s[i]]
    s = execute_transitions(s, [transition])[0]
    for i in range(tabu_list.shape[0]):
        c_fit = c_fit + D[transition[1]][i] * W[s[transition[1]]][s[i]]
        c_fit = c_fit + D[transition[0]][i] * W[s[transition[0]]][s[i]]
    return c_fit


# ###################################################### global function

def global_function(initial_state, fitness_initial_state):
    state = initial_state
    fitness = fitness_initial_state

    all_time_fitness = [fitness]

    best_state = initial_state
    best_fitness = fitness_initial_state

    for i in range(t_max):
        transitions_legal = compute_transitions(state)
        executed_transitions = execute_transitions(state, transitions_legal)
        fitness_transitions = [compute_fitness(s) for s in executed_transitions]

        new_state = executed_transitions[np.argmin(fitness_transitions)]
        new_fit = fitness_transitions[np.argmin(fitness_transitions)]

        all_time_fitness.append(new_fit)
        if new_fit < best_fitness:
            best_fitness = new_fit
            best_state = new_state
        update_tabu_diversification_meca(new_state, transitions_legal[np.argmin(fitness_transitions)])
    return best_state, best_fitness, all_time_fitness


states = []
fitness = []
all_time_list = []

for i in range(10):
    initial_state = generate_random_state()
    fitness_initial_state = compute_fitness(initial_state)
    s, fit, all_time = global_function(initial_state, fitness_initial_state)
    states.append(s)
    fitness.append(fit)
    all_time_list.append(all_time)

for i in range(len(states)):
    print("state->", states[i], " || fit -> ", fitness[i], " || avg -> ",
          np.sum(all_time_list[i]) / len(all_time_list[i]), " || np.max/np.min -> ", np.max(all_time_list[i]), " / ",
          np.min(all_time_list[i]))

"""
without diversification

l = 1

state-> [6, 10, 4, 0, 5, 3, 7, 1, 11, 8, 9, 2]  || fit ->  744  || avg ->  746.0030998450078  || np.max/np.min ->  808  /  744
state-> [2, 7, 11, 6, 10, 1, 3, 8, 0, 9, 4, 5]  || fit ->  730  || avg ->  732.0037998100095  || np.max/np.min ->  808  /  730
state-> [5, 9, 7, 6, 1, 4, 8, 10, 0, 11, 2, 3]  || fit ->  740  || avg ->  746.0038998050097  || np.max/np.min ->  824  /  740
state-> [9, 2, 1, 8, 6, 5, 4, 11, 7, 3, 0, 10]  || fit ->  704  || avg ->  705.0021498925054  || np.max/np.min ->  748  /  704
state-> [0, 1, 11, 10, 5, 2, 3, 8, 9, 4, 7, 6]  || fit ->  746  || avg ->  751.0044497775111  || np.max/np.min ->  840  /  746
state-> [11, 0, 1, 2, 8, 10, 7, 9, 6, 3, 5, 4]  || fit ->  664  || avg ->  664.0010999450028  || np.max/np.min ->  686  /  664
state-> [1, 8, 11, 10, 5, 0, 9, 2, 7, 6, 3, 4]  || fit ->  802  || avg ->  802.005599720014  || np.max/np.min ->  914  /  802
state-> [6, 3, 7, 0, 5, 9, 1, 10, 4, 8, 2, 11]  || fit ->  728  || avg ->  739.0055497225138  || np.max/np.min ->  850  /  728
state-> [0, 7, 6, 10, 1, 8, 11, 4, 2, 3, 9, 5]  || fit ->  726  || avg ->  733.0053497325134  || np.max/np.min ->  840  /  726
state-> [3, 4, 7, 6, 10, 1, 2, 0, 11, 8, 9, 5]  || fit ->  786  || avg ->  794.006399680016  || np.max/np.min ->  922  /  786

l = 6

state-> [9, 0, 3, 4, 1, 6, 5, 11, 2, 7, 10, 8]  || fit ->  682  || avg ->  716.0000999950003  || np.max/np.min ->  752  /  682
state-> [0, 7, 2, 1, 9, 11, 8, 3, 5, 4, 6, 10]  || fit ->  786  || avg ->  808.8602569871506  || np.max/np.min ->  894  /  786
state-> [1, 9, 5, 6, 8, 2, 4, 11, 0, 3, 7, 10]  || fit ->  744  || avg ->  764.573171341433  || np.max/np.min ->  820  /  744
state-> [4, 1, 6, 11, 5, 10, 9, 8, 3, 7, 0, 2]  || fit ->  684  || avg ->  694.2876856157192  || np.max/np.min ->  738  /  684
state-> [0, 6, 7, 2, 11, 8, 3, 9, 5, 10, 1, 4]  || fit ->  734  || avg ->  749.1451427428628  || np.max/np.min ->  810  /  734
state-> [1, 3, 5, 10, 2, 0, 9, 11, 4, 7, 6, 8]  || fit ->  778  || avg ->  789.4324283785811  || np.max/np.min ->  878  /  778
state-> [7, 2, 0, 10, 6, 3, 1, 9, 5, 11, 4, 8]  || fit ->  746  || avg ->  763.1444427778611  || np.max/np.min ->  812  /  746
state-> [11, 6, 1, 4, 8, 7, 5, 9, 3, 10, 2, 0]  || fit ->  718  || avg ->  742.5741712914354  || np.max/np.min ->  798  /  718
state-> [10, 7, 3, 2, 6, 9, 8, 11, 5, 1, 0, 4]  || fit ->  726  || avg ->  755.1435428228589  || np.max/np.min ->  798  /  726
state-> [1, 9, 0, 2, 8, 6, 10, 7, 5, 11, 3, 4]  || fit ->  708  || avg ->  732.0009999500026  || np.max/np.min ->  776  /  708

l = 10

state-> [8, 11, 6, 2, 0, 10, 9, 5, 1, 7, 3, 4]  || fit ->  710  || avg ->  777.816809159542  || np.max/np.min ->  846  /  710
state-> [5, 7, 4, 3, 2, 0, 9, 6, 8, 10, 11, 1]  || fit ->  786  || avg ->  826.0029998500075  || np.max/np.min ->  910  /  786
state-> [8, 11, 0, 10, 1, 6, 7, 3, 9, 5, 2, 4]  || fit ->  702  || avg ->  724.9104544772762  || np.max/np.min ->  776  /  702
state-> [3, 0, 11, 6, 7, 10, 1, 9, 8, 2, 5, 4]  || fit ->  786  || avg ->  814.7300634968252  || np.max/np.min ->  900  /  786
state-> [4, 11, 5, 2, 1, 9, 3, 7, 10, 8, 0, 6]  || fit ->  768  || avg ->  802.0022998850058  || np.max/np.min ->  904  /  768
state-> [10, 5, 2, 11, 3, 1, 8, 6, 4, 9, 0, 7]  || fit ->  780  || avg ->  806.1833908304585  || np.max/np.min ->  884  /  780
state-> [10, 9, 5, 4, 6, 8, 7, 1, 2, 11, 3, 0]  || fit ->  684  || avg ->  727.6346182690866  || np.max/np.min ->  758  /  684
state-> [4, 1, 0, 6, 5, 9, 2, 3, 8, 11, 10, 7]  || fit ->  734  || avg ->  747.6371181440928  || np.max/np.min ->  786  /  734
state-> [9, 5, 3, 4, 2, 6, 11, 1, 8, 7, 10, 0]  || fit ->  740  || avg ->  752.1833908304585  || np.max/np.min ->  804  /  740
state-> [11, 8, 5, 4, 3, 6, 0, 9, 7, 10, 1, 2]  || fit ->  686  || avg ->  744.7254637268137  || np.max/np.min ->  786  /  686

"""

"""
with diversification

l = 1

state-> [9, 2, 10, 11, 1, 0, 7, 8, 5, 6, 4, 3]  || fit ->  716  || avg ->  773.4865256737163  || np.max/np.min ->  888  /  716
state-> [8, 0, 10, 9, 11, 7, 2, 1, 3, 6, 5, 4]  || fit ->  680  || avg ->  720.2510874456277  || np.max/np.min ->  866  /  680
state-> [2, 7, 10, 1, 3, 0, 4, 5, 11, 6, 8, 9]  || fit ->  710  || avg ->  765.0842457877106  || np.max/np.min ->  882  /  710
state-> [4, 1, 5, 8, 7, 0, 10, 6, 3, 9, 2, 11]  || fit ->  724  || avg ->  801.6221188940553  || np.max/np.min ->  942  /  724
state-> [5, 6, 2, 7, 8, 11, 9, 0, 4, 10, 3, 1]  || fit ->  756  || avg ->  802.3594820258987  || np.max/np.min ->  908  /  756
state-> [9, 5, 4, 0, 6, 10, 8, 2, 7, 3, 11, 1]  || fit ->  680  || avg ->  728.3289835508225  || np.max/np.min ->  860  /  680
state-> [11, 1, 4, 3, 5, 9, 2, 0, 6, 8, 10, 7]  || fit ->  726  || avg ->  760.5776711164442  || np.max/np.min ->  858  /  726
state-> [9, 11, 1, 4, 6, 3, 8, 10, 7, 2, 0, 5]  || fit ->  754  || avg ->  807.0167491625418  || np.max/np.min ->  926  /  754
state-> [1, 7, 5, 4, 0, 3, 8, 10, 6, 11, 2, 9]  || fit ->  750  || avg ->  796.5556722163892  || np.max/np.min ->  904  /  750
state-> [9, 5, 4, 1, 10, 3, 0, 6, 2, 7, 8, 11]  || fit ->  694  || avg ->  749.1162441877906  || np.max/np.min ->  870  /  694

l = 6

state-> [3, 11, 8, 10, 2, 0, 9, 4, 7, 1, 6, 5]  || fit ->  698  || avg ->  750.2855857207139  || np.max/np.min ->  854  /  698
state-> [7, 0, 6, 4, 3, 2, 9, 5, 11, 10, 1, 8]  || fit ->  726  || avg ->  791.8937053147342  || np.max/np.min ->  978  /  726
state-> [2, 11, 8, 6, 7, 10, 5, 9, 0, 3, 4, 1]  || fit ->  654  || avg ->  704.4896755162242  || np.max/np.min ->  838  /  654
state-> [2, 5, 0, 4, 11, 8, 3, 1, 7, 10, 6, 9]  || fit ->  730  || avg ->  801.1810409479526  || np.max/np.min ->  882  /  730
state-> [9, 2, 7, 11, 3, 10, 6, 8, 5, 4, 0, 1]  || fit ->  720  || avg ->  759.2229388530574  || np.max/np.min ->  886  /  720
state-> [6, 8, 11, 3, 9, 10, 0, 4, 7, 2, 1, 5]  || fit ->  742  || avg ->  797.569621518924  || np.max/np.min ->  938  /  742
state-> [11, 6, 3, 7, 8, 10, 0, 9, 2, 1, 4, 5]  || fit ->  664  || avg ->  723.0792460376981  || np.max/np.min ->  888  /  664
state-> [6, 7, 10, 3, 1, 2, 9, 4, 0, 5, 8, 11]  || fit ->  728  || avg ->  787.3278336083196  || np.max/np.min ->  900  /  728
state-> [2, 9, 7, 3, 6, 10, 4, 5, 1, 8, 0, 11]  || fit ->  728  || avg ->  762.494375281236  || np.max/np.min ->  878  /  728
state-> [9, 0, 11, 8, 5, 10, 2, 7, 4, 3, 1, 6]  || fit ->  728  || avg ->  768.177991100445  || np.max/np.min ->  894  /  728

l = 10

state-> [7, 3, 11, 5, 6, 8, 1, 10, 2, 9, 0, 4]  || fit ->  772  || avg ->  833.9615019249037  || np.max/np.min ->  930  /  772
state-> [6, 0, 7, 3, 8, 11, 5, 4, 1, 2, 10, 9]  || fit ->  678  || avg ->  749.5278236088195  || np.max/np.min ->  890  /  678
state-> [1, 8, 7, 6, 4, 2, 0, 3, 5, 9, 10, 11]  || fit ->  728  || avg ->  781.2840357982101  || np.max/np.min ->  896  /  728
state-> [8, 1, 10, 4, 6, 2, 5, 7, 11, 0, 9, 3]  || fit ->  732  || avg ->  823.9915004249788  || np.max/np.min ->  914  /  732
state-> [1, 10, 2, 9, 6, 0, 4, 7, 11, 8, 5, 3]  || fit ->  772  || avg ->  799.809609519524  || np.max/np.min ->  924  /  772
state-> [4, 7, 3, 11, 0, 2, 6, 8, 9, 1, 5, 10]  || fit ->  690  || avg ->  781.8713064346782  || np.max/np.min ->  898  /  690
state-> [5, 0, 4, 11, 9, 3, 10, 2, 6, 7, 1, 8]  || fit ->  716  || avg ->  760.5629718514074  || np.max/np.min ->  876  /  716
state-> [5, 6, 1, 8, 4, 11, 0, 10, 9, 7, 3, 2]  || fit ->  714  || avg ->  773.7530123493825  || np.max/np.min ->  944  /  714
state-> [11, 6, 8, 0, 7, 1, 3, 2, 10, 5, 9, 4]  || fit ->  780  || avg ->  818.1706914654268  || np.max/np.min ->  930  /  780
state-> [9, 2, 11, 3, 1, 4, 8, 6, 5, 0, 10, 7]  || fit ->  704  || avg ->  759.5157242137893  || np.max/np.min ->  896  /  704
"""
