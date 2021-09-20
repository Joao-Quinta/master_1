import numpy as np
import math
import random


# N -> number of faces, n -> number of rolls
def balancedDice(N, n):
    arr = [random.randint(1, N) for _ in range(n)]
    arr2 = [math.floor(random.random() * N) for _ in range(n)]

    print(arr)
    print(arr2)


balancedDice(6, 10)
