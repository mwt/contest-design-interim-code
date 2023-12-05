"""
Library to house common functions for the three-player game.
"""

import numpy as np


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
    if k[2] / k[0] >= 3:
        return {
            "scores": np.array(
                [1 / (2 * k[0]) + 1 / (2 * k[2]), 1 / (2 * k[2]), 1 / (2 * k[2])]
            ),
            "prizes": np.array([1, 0.5, 0.5]),
            "revenue": 1 / (2 * k[0]) + 3 / (2 * k[2]),
            "description": "Case 2: The principal transfers half of Player 2's prize to Player 3.",
        }
    if k[2] / k[1] >= 2:
        return {
            "scores": np.array([1 / k[2], 1 / k[2], 1 / k[2]]),
            "prizes": np.array([0.5, 0.5, 1]),
            "revenue": 3 / k[2],
            "description": "Case 3: The principal transfers half of Player 1's and Player 2's prize to\n        Player 3.",
        }
    if (k[1] + k[2]) / k[0] >= 3:
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
    if (k[1] + k[2]) / k[0] <= 3:
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
