import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import random


def function_plot1(y1, y2, y3, y4, y5):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_ylabel('fitness')
    ax1.set_xlabel('iteration')

    ax1.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ax1.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    """
    ax1.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y1, 'bo', label='best value at iteration 0')
    ax1.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y2, 'ro', label='best value at final iteration')
    ax1.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y1, 'b--')
    ax1.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y2, 'r--')
    """
    ax1.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y1, label='Vmax = False')
    ax1.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y2, label='Vmax = 0.5')
    ax1.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y3, label='Vmax = 1')
    ax1.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y4, label='Vmax = 1.5')
    ax1.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], y5, label='Vmax = 2')
    ax1.legend()
    plt.show()


y1 = [0.375, 0.35, 0.35, 0.32, 0.22, 0.205, 0.155, 0.155, 0.155, 0.155]
y2 = [0.32, 0.32, 0.32, 0.27, 0.27, 0.22, 0.22, 0.22, 0.22, 0.22]
y3 = [0.385, 0.255, 0.19, 0.19, 0.19, 0.13, 0.13, 0.13, 0.13, 0.13]
y4 = [0.3, 0.3, 0.3, 0.22, 0.22, 0.205, 0.15, 0.15, 0.1, 0.1]
y5 = [0.37, 0.25, 0.25, 0.2, 0.2, 0.185, 0.18, 0.175, 0.14, 0.14]
function_plot1(y1, y2, y3, y4, y5)
