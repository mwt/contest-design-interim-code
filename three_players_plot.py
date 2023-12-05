"""
Make and save plots which show strategies, revenues, and payoffs for three
players with bid costs:
    k_1 = 5/6
    k_2 = 1.0
    k_3 = k (variable)

The plots are saved in the directory: plots/three_players_plot/
"""

import pathlib

import matplotlib.pyplot as plt
import numpy as np

from three_players import analytical_solution

################## Set parameters ###################

# Number of points to plot
n = 10000

# Set bid costs as a matrix with k_1, k_2, k_3 as columns
k = np.linspace(1.0, 3.5, n)
k_grid = np.column_stack(np.broadcast_arrays(5 / 6, 1.0, k))

# Output directory
output_dir = pathlib.Path("plots/three_players_plot")

####################### Setup #######################

# Create directory for plots
output_dir.mkdir(parents=True, exist_ok=True)

scores = []
prizes = []
revenues = []

for ki in k_grid:
    result = analytical_solution(ki)
    scores.append(result["scores"])
    prizes.append(result["prizes"])
    revenues.append(result["revenue"])

np_scores = np.array(scores)
np_prizes = np.array(prizes)
np_revenues = np.array(revenues)


####################### Plots #######################

###################### Revenue

# Create a plot of k vs np_revenues and export to .pdf
fig, ax = plt.subplots()
ax.plot(k, np_revenues, color="black")

# Draw thin, dotted grey lines at switching points
for i in [1.5, 2.0, 2.5, 3.0]:
    ax.axvline(i, linestyle=":", color="grey", linewidth=0.5)

# Set bounds for the axes
ax.set_xlim(1.0, 3.5)
ax.set_ylim(0.0, 2.2)

# Set labels
ax.set_xlabel(r"$k_3$")
ax.set_ylabel("Revenue")

# Make plot 16:9
fig.set_size_inches(16 / 2.54, 9 / 2.54)

# Save the plot
fig.savefig(output_dir / "revenue.pdf", bbox_inches="tight")

###################### Scores

# Create a plot of k vs np_scores and export to .pdf
fig, ax = plt.subplots()

# Hide the spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Control the colors of the lines
ax.plot(k, np_scores[:, 2], label="Player 3", color="red", linestyle="-")
ax.plot(k, np_scores[:, 1], label="Player 2", color="green", linestyle="--")
ax.plot(k, np_scores[:, 0], label="Player 1", color="blue", linestyle=":")

# Draw thin, dotted grey lines at switching points
for i in [1.5, 2.0, 2.5, 3.0]:
    ax.axvline(i, linestyle=":", color="grey", linewidth=0.5)

# Add a legend
ax.legend()

# Set bounds for the axes
ax.set_xlim(1.0, 3.5)
ax.set_ylim(0.0, 1.0)

# Set labels
ax.set_xlabel(r"$k_3$")
ax.set_ylabel("Scores")

# Make plot 16:9
fig.set_size_inches(16 / 2.54, 9 / 2.54)

# Save the plot
fig.savefig(output_dir / "scores.pdf", bbox_inches="tight")


###################### Prizes

# Create a plot of k vs np_prizes and export to .pdf
fig, ax = plt.subplots()

# Hide the spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Control the colors of the lines
ax.plot(k, np_prizes[:, 2], label="Player 3", color="red", linestyle="-", linewidth=1.5)
ax.plot(
    k, np_prizes[:, 1], label="Player 2", color="green", linestyle="--", linewidth=1.5
)
ax.plot(
    k, np_prizes[:, 0], label="Player 1", color="blue", linestyle=":", linewidth=1.5
)

# Draw thin, dotted grey lines at switching points
for i in [1.5, 2.0, 2.5, 3.0]:
    ax.axvline(i, linestyle=":", color="grey", linewidth=0.5)

# Add a legend
ax.legend()

# Set bounds for the axes
ax.set_xlim(1.0, 3.5)
ax.set_ylim(0.0, 1)

# Set labels
ax.set_xlabel(r"$k_3$")
ax.set_ylabel("Prizes")

# Make plot 16:9
fig.set_size_inches(16 / 2.54, 9 / 2.54)

# Save the plot
fig.savefig(output_dir / "prizes.pdf", bbox_inches="tight")
