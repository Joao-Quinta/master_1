import numpy as np
import matplotlib as plt
import math
import random


# N -> number of faces, n -> number of rolls
def balancedDice(N, n):
    arr = [math.floor(random.random() * N) for _ in range(n)]


    for i in range(0, N):
        print("val -> ", i, " : ", arr.count(i))

balancedDice(6, 10000)
