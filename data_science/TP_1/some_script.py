# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:41:20 2020

@author: Denis
"""
from datetime import datetime
import numpy as np

print('START - %s' % datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

# parameters
N = 2  # the dimension chosen

# functions
def scalar_product(u, v):
    """
    takes a pair of vectors (u, v) as input and returns their scalar product
    such that s = sum_{i=1..N}(u_i * v_i)
    """

    return np.dot(u, v)


def deviate_vector(u, v):
    """
    takes a pair of vectors (u, v) as input and returns a vector w defined by
    w = v - projection of v on u.
    """

    return v - project_on_first(u, v)


def project_on_first(u, v):
    """
    takes a pair of vectors (u, v) as input and returns the vector w which is
    the projection of v on u : w and u are colinear. All vectors are column!
    subspace is a build-in function of matlab which returns the angle between
    2 column vectors.
    (au)^2 + (v-au)^2 = v^2
    a^2u^2 + v^2 -2a(v,u) + a^2u^2 = v^2
    a^2u^2 -a(u,v) = 0
    a = (u,v)/u^2
    """
    return np.dot(u, v) / np.dot(u, u) * u


def orthogonal_norm_on_first(u, v):
    w_1 = np.dot(u, v) / np.dot(u, u) * u  # computes the projection of v onto u = w_1
    w_2 = v - w_1  # computes a vector orthogonal to w_1, such that : v = w_1 + w_2

    norm_u = np.linalg.norm(u)  # compute norm of u
    norm_w_2 = np.linalg.norm(w_2)  # compute norm of w_2

    # the goal is to compute a collinear vector to w_2 of same norm as u

    alpha = norm_u / norm_w_2  # this value tells us by how much we multiply w_2 by to make it the same norm as u

    w_2_norm = alpha * w_2  # w_2_norm is collinear to w_2, but of different norm !
    norm_w_2_alpha = np.linalg.norm(w_2_norm)  # compute the norm of the computed vector to verify if it was done right

    return w_2_norm


u = np.zeros(N)
u[np.random.randint(N)] = 1  # random canonic vector of dimension N
v = np.random.randn(N)  # random vector of dimension N

w = deviate_vector(u, v)  # w is a vector, function of u and v based on some geometrics

print('Result = %.1f' % scalar_product(u, w))

print('END - %s\n' % datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

u1 = np.random.randn(5)
v1 = np.random.randn(5)

w_2_norm = orthogonal_norm_on_first(u1, v1)

# print("norm of u        -> ", np.linalg.norm(u1))
# print("norm of w_2_norm -> ", np.linalg.norm(w_2_norm))
# print("scalar product of u and w_2_norm", np.dot(u1, w_2_norm))
