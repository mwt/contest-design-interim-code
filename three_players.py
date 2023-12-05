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


def analytical_solution(k):
    """Analytical solution to the three-player game.
    Parameters
    ----------
    k : array
        Bid costs of Player 1, Player 2, and Player 3, respectively.

    Returns
    -------
    dict
        Dictionary with the following keys:
        - scores: array
            Scores of Player 1, Player 2, and Player 3, respectively.
        - prizes: array
            Prizes of Player 1, Player 2, and Player 3, respectively.
        - revenue: array
            Revenue of the principal.
        - description: str
            Description of the solution.
    """
    if k[2] / k[1] >= 3:
        return {
            "scores": np.array([1 / (2 * k[0]), 1 / (2 * k[1]), 0]),
            "prizes": np.array([1, 1, 0]),
            "revenue": 1 / (2 * k[0]) + 1 / (2 * k[1]),
            "description": "Case 1: It is not worthwhile for the principal to demand effort from Player 3.",
        }
    if k[2] / k[1] <= 3 <= k[2] / k[0]:
        return {
            "scores": np.array(
                [1 / (2 * k[0]) + 1 / (2 * k[2]), 1 / (2 * k[2]), 1 / (2 * k[2])]
            ),
            "prizes": np.array([1, 0.5, 0.5]),
            "revenue": 1 / (2 * k[0]) + 3 / (2 * k[2]),
            "description": "Case 2: The principal transfers half of Player 2's prize to Player 3.",
        }
    if k[2] / k[0] <= 3 and k[2] / k[1] >= 2:
        return {
            "scores": np.array([1 / k[2], 1 / k[2], 1 / k[2]]),
            "prizes": np.array([0.5, 0.5, 1]),
            "revenue": 3 / k[2],
            "description": "Case 3: The principal transfers half of Player 1's and Player 2's prize to\n        Player 3.",
        }
    if k[2] / k[0] <= 3 <= (k[1] + k[2]) / k[0] and k[2] / k[0] <= 2:
        return {
            "scores": np.array(
                [
                    1 / k[0] - ((k[2] / k[0]) - 1) / (2 * k[1]),
                    1 / (2 * k[1]),
                    1 / (2 * k[1]),
                ]
            ),
            "prizes": np.array([1.5 - (k[2] / (2 * k[1])), 0.5, k[2] / (2 * k[1])]),
            "revenue": 1 / k[0] + (3 - (k[2] / k[0])) / (2 * k[1]),
            "description": "Case 4: The principal transfers half of Player 2's and some of Player 1's to\n        Player 3. Player 2's individual rationality constraint is binding.",
        }
    if (k[1] + k[2]) / k[0] <= 3 and k[2] / k[0] <= 2:
        return {
            "scores": np.array(
                [
                    (4 - ((k[1] + k[2]) / k[0])) / (2 * k[0]),
                    1 / (2 * k[0]),
                    1 / (2 * k[0]),
                ]
            ),
            "prizes": np.array(
                [
                    2 - ((k[1] + k[2]) / (2 * k[0])),
                    k[1] / (2 * k[0]),
                    k[2] / (2 * k[0]),
                ]
            ),
            "revenue": (6 - ((k[1] + k[2]) / k[0])) / (2 * k[0]),
            "description": """Case 5: The principal transfers some of Player 1's and Player 2's prize to\n        Player 3. Every player's individual rationality constraint is binding.""",
        }


solution = analytical_solution(k)

########### Print results

print(" Analytical Results ".center(80, "="))
print("")
print("Analytical scores:  ", solution["scores"])
print("Analytical prizes:  ", solution["prizes"])
print("Analytical revenue: ", np.array([solution["revenue"]]))
print("")
print(solution["description"])
