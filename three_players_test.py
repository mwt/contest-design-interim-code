#!/usr/bin/env python3
"""
Command line script to solve the three-player game both analytically and numerically.

The script takes three arguments, k_1, k_2, and k_3, which are the bid costs of
Player 1, Player 2, and Player 3, respectively. The script then solves the
three-player game both analytically and numerically, and prints the results.
"""

import sys

import numpy as np
from scipy.optimize import linprog

from three_players import analytical_solution

###################### Set up #######################

# Set up numpy printing options
np.set_printoptions(precision=4, floatmode="fixed", suppress=True)

###################### Inputs #######################

############## Define constants

# extract k (bid cost) from command line
k = np.array(sys.argv[1:4], dtype=float)

############## Print inputs

print(" Inputs ".center(80, "="))
print("")
print("Bid costs:          ", k)
print("")


################ Linear optimization ################

############## Define constants
# We will order the values of the vector, x, as follows:
# x = [s_1, s_2, s_3, p_1, p_2, p_3]

# Optimization matrix, c, three ones and three zeros
c = -np.append(np.ones(3), np.zeros(3))

# Inequality constraint matrix, Aub and b_ub
# Aub = [[ IC 1,2 ],
#        [ IC 1,3 ],
#        [ IC 2,1 ],
#        [ IC 2,3 ],
#        [ IC 3,1 ],
#        [ IC 3,2 ],
#        [ IR 1 ],
#        [ IR 2 ],
#        [ IR 3 ]]
# IC i,j: k_i * s_i - k_i * s_j - p_i <= -1/2
# IR i  : k_i * s_i - p_i <= 0
Aub = np.array(
    [
        [k[0], -k[0], 0, -1, 0, 0],
        [k[0], 0, -k[0], -1, 0, 0],
        [-k[1], k[1], 0, 0, -1, 0],
        [0, k[1], -k[1], 0, -1, 0],
        [-k[2], 0, k[2], 0, 0, -1],
        [0, -k[2], k[2], 0, 0, -1],
        [k[0], 0, 0, -1, 0, 0],
        [0, k[1], 0, 0, -1, 0],
        [0, 0, k[2], 0, 0, -1],
    ]
)

b_ub = np.array([-0.5] * 6 + [0] * 3)


# Equality constraint matrix, Aeq and beq
# Aeq = [[ p_1 + p_2 + p_3 = 2 ]]
Aeq = np.array([[0, 0, 0, 1, 1, 1]])
beq = np.array([2])

# Specify bounds for each variable
bounds = np.array([(0, 1 / ki) for ki in k] + [(0, 1)] * 3)


############## Solve optimization
optimization_result = linprog(c, Aub, b_ub, Aeq, beq, bounds)

############## Print results

print(" Numerical Results ".center(80, "="))
print("")
print("Numerical scores:   ", optimization_result.x[0:3])
print("Numerical prizes:   ", optimization_result.x[3:6])
print("Numerical revenue:  ", np.array([-optimization_result.fun]))
print("")


############ Analytic results from paper ############

solution = analytical_solution(k)

########### Print results

print(" Analytical Results ".center(80, "="))
print("")
print("Analytical scores:  ", solution["scores"])
print("Analytical prizes:  ", solution["prizes"])
print("Analytical revenue: ", np.array([solution["revenue"]]))
print("")
print(solution["description"])
