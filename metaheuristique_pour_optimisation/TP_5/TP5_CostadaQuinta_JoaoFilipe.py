import numpy as np
import random
import math


# gets the X and Y data from X.dat and Y.dat
def extractData():
    data = np.genfromtxt('X.dat', dtype=None, encoding=None, comments='#', delimiter=None)
    images = []
    for d in data:
        vec = np.ones((401, 1))
        i = 1
        line = d
        current = ''
        while len(line) > 0:
            if line[0] == ',':
                vec[i] = float(current)
                current = ''
                i = i + 1
            else:
                current = current + line[0]
            line = line[1:]
        vec[i] = float(current)
        images.append(vec)

    data = np.genfromtxt('Y.dat', dtype=None, encoding=None, comments='#', delimiter=None)
    label = []
    for d in data:
        label.append(int(d))

    return images, label


# computes sigmoid value of x
def sigmoid(x):
    return 1 / (1 + np.exp(- x))


# just a matrix multiplication and application of sigmoid function
def matrix_mul_sigmoid(A, B):
    C = np.dot(A, B)
    for i in range(C.shape[0]):
        C[i] = sigmoid(C[i])
    return C


# rounds the values of the vector
def turn_to_1_or_0(V):
    for i in range(len(V)):
        if V[i] >= 0.5:
            V[i] = 1
        else:
            V[i] = 0
    return V


# computes global error
def computeError(Y_true, Y_pred):
    Y_pred = turn_to_1_or_0(Y_pred)
    err = 0
    for i in range(len(Y_true)):
        err = err + np.power(Y_true[i] - Y_pred[i], 2)
    err = err / len(Y_true)
    return err


def computeNeuralNetwork(sigma_1, sigma_2):
    X, Y = extractData()
    y_pred = []
    for i in range(len(X)):
        c = np.insert(matrix_mul_sigmoid(sigma_1, X[i]), 0, 1, axis=0)
        r = matrix_mul_sigmoid(sigma_2, c)
        y_pred.append(r[0][0])
    err = computeError(Y, y_pred)
    return err


# k = nb of particles
def pso(k, t_max, v_max):
    best_global_score = math.inf
    best_global_m = [np.zeros((25, 401)), np.zeros((1, 26))]

    best_individual_score = []
    best_individual_m = []
    for j in range(k):
        best_individual_score.append(math.inf)
        best_individual_m.append([np.zeros((25, 401)), np.zeros((1, 26))])

    m_1 = []
    m_2 = []
    v = []
    # initialize step
    for i in range(k):
        m_k_1 = np.zeros((25, 401))
        m_k_2 = np.zeros((1, 26))
        for j in range(m_k_1.shape[0]):
            for z in range(m_k_1.shape[1]):
                m_k_1[j][z] = random.random() - 0.5

        for j in range(m_k_2.shape[1]):
            m_k_2[0][j] = random.random() - 0.5
        m_1.append(m_k_1)
        m_2.append(m_k_2)

        v.append([np.zeros((25, 401)), np.zeros((1, 26))])

    for t in range(t_max):
        # compute each initial fitness - and update local best if required
        for i in range(k):
            err_i = computeNeuralNetwork(m_1[i], m_2[i])
            if err_i < best_individual_score[i]:
                best_individual_score[i] = err_i
                best_individual_m[i] = [np.copy(m_1[i]), np.copy(m_2[i])]

        # compute global best fitness - and update it if required
        if best_global_score > np.min(best_individual_score):
            best_global_score = best_individual_score[np.argmin(best_individual_score)]
            best_global_m = [np.copy(best_individual_m[np.argmin(best_individual_score)][0]),
                             np.copy(best_individual_m[np.argmin(best_individual_score)][1])]

        # update speed
        w = 0.9
        c1 = 2
        c2 = 2

        for i in range(k):
            r1 = random.random()
            r2 = random.random()
            v[i][0] = np.add(np.add((v[i][0] * w), (c1 * r1 * (np.subtract(best_individual_m[i][0], m_1[i])))),
                             (c2 * r2 * (np.subtract(best_global_m[0], m_1[i]))))
            v[i][1] = np.add(np.add((v[i][1] * w), (c1 * r1 * (np.subtract(best_individual_m[i][1], m_2[i])))),
                             (c2 * r2 * (np.subtract(best_global_m[1], m_2[i]))))

            # cut off option
            if v_max != 0:
                v[i][0] = np.maximum(np.minimum(v[i][0], np.full((25, 401), v_max)), np.full((25, 401), - v_max))
                v[i][1] = np.maximum(np.minimum(v[i][1], np.full((1, 26), v_max)), np.full((1, 26), - v_max))

            m_1[i] = np.add(m_1[i], v[i][0])
            m_2[i] = np.add(m_2[i], v[i][1])

            # makes particles stay inside the designated search space
            for j in range(m_1[i].shape[0]):
                for z in range(m_1[i].shape[1]):
                    if m_1[i][j][z] > 0.5:
                        m_1[i][j][z] = m_1[i][j][z] - 1
                    elif m_1[i][j][z] < -0.5:
                        m_1[i][j][z] = m_1[i][j][z] + 1

            for j in range(m_2[i].shape[1]):
                if m_2[i][0][j] > 0.5:
                    m_2[i][0][j] = m_2[i][0][j] - 1
                elif m_2[i][0][j] < -0.5:
                    m_2[i][0][j] = m_2[i][0][j] + 1

        print("iteration : ", t, " || best score is : ", best_global_score, " || mean score is : ",
              str(np.sum(best_individual_score) / len(best_individual_score))[:4])


print("#Particles = 20 && Tmax = 10 && Vmax = 2")
pso(20, 10, 2)
