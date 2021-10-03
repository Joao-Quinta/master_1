import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import random


def function_plot(array_vals, type, k):
    print(array_vals)
    n, bins, patches = plt.hist(array_vals, np.unique(array_vals), color="tab:blue", alpha=0.5, histtype='bar',
                                ec='black')

    str_t = type + " hill-climbing, K=" + str(k)
    plt.title(str_t)
    plt.xlabel('Hamming distance')
    plt.ylabel('Number of times')

    plt.show()

    """
        for i in np.unique(array_vals):
        val_i = np.count(array_vals = )
    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title('Histogram of IQ')
    plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    plt.xlim(40, 160)
    plt.ylim(0, 0.03)
    plt.grid(True)
    plt.show()
    """


def function_plot1(x, y1, y2, k):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_ylabel('fitness returned')
    ax1.set_xlabel('call')
    """
    max1 = np.max(y1)
    max2 = np.max(y2)
    max3 = max(max1, max2)
    ax1.set_yticks([0, max3])
    """

    ax1.set_xticks([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    ax1.plot(x, y1, label='deterministic')
    ax1.plot(x, y2, label='probabilistic')
    ax1.legend()
    plt.show()


"""
x = np.arange(0, 1, 1 / 1000)
n1 = 6
n2 = 12
y1 = x*n1
y2 = x*n2
y1 = [math.floor(y1[i]) for i in range(len(y1))]
y2 = [math.floor(y2[i]) for i in range(len(y2))]

fig = plt.figure()
ax1 = fig.add_subplot()
ax1.set_ylabel('result')
ax1.set_xlabel('[ 0 , 1 )')
ax1.set_yticks(range(n2))
ax1.set_xticks([0, 0.5, 1])
ax1.plot(x, y1, label='n = 6')
ax1.plot(x, y2, label='n = 12')
ax1.legend()

x = np.arange(0, 1, 1 / 10)
p1 = 0.3
p2 = 0.7
y1 = []
y2 = []

for i in range(len(x)):
    y1.append(math.floor(x[i] + p1))
    y2.append(math.floor(x[i] + p2))

print(np.unique(y1))


fig = plt.figure()
ax1 = fig.add_subplot()
ax1.set_ylabel('result')
ax1.set_xlabel('[ 0 , 1 )')
ax1.set_yticks([0, 1])
ax1.set_xticks([0, 0.3, 0.7, 1])
ax1.plot(x, y1, label='p = 0.3')
ax1.plot(x, y2, label='p = 0.7')
ax1.legend()
plt.show()"""
