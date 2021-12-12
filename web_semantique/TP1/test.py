import copy

import numpy as np


def etape(x, b):
    b_ = copy.copy(b)
    for i in range(len(b_)):
        if b_[i] >= x:
            b_[i] = b_[i] - x
    return b_


b_etape_ = []
for i in range(1, 2021):
    b_etape_.append(i)

# print(boxes)
x = 1024
i = 1
while x > 0:
    b_etape_ = etape(x, b_etape_)
    if len(np.unique(b_etape_)) == x:
        print("etape ", i, ": bonne -> ", x, " subsets")
        i = i + 1
        x = int(x/2)

print(b_etape_)