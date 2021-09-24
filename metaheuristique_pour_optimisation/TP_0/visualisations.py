import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import random

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


plt.show()