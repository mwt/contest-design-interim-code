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

# Output directories
plot_dir = pathlib.Path("plots/three_players_plot")
data_dir = pathlib.Path("data/three_players_plot")

# Plot size
plot_width = 5.5
plot_height = 2.3

# Set matplotlib parameters
plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "sans-serif",
    }
)

####################### Setup #######################

# Create directory for plots
plot_dir.mkdir(parents=True, exist_ok=True)
data_dir.mkdir(parents=True, exist_ok=True)

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

# Save to tsv
np.savetxt(
    data_dir / "3p-scores.tsv",
    np.column_stack((k, np_scores)),
    delimiter="\t",
    header="k\ts1\ts2\ts3",
    comments="",
)
np.savetxt(
    data_dir / "3p-prizes.tsv",
    np.column_stack((k, np_prizes)),
    delimiter="\t",
    header="k\tp1\tp2\tp3",
    comments="",
)
np.savetxt(
    data_dir / "3p-revenue.tsv",
    np.column_stack((k, np_revenues)),
    delimiter="\t",
    header="k\tR",
    comments="",
)


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
fig.set_size_inches(plot_width, plot_height)

# Save the plot
fig.savefig(plot_dir / "3p-revenue.pdf", bbox_inches="tight", transparent=True)

###################### Scores

# Create a plot of k vs np_scores and export to .pdf
fig, ax = plt.subplots()

# Hide the spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Control the colors of the lines
ax.plot(k, np_scores[:, 2], label=r"Player $3$", color="red", linestyle="-")
ax.plot(k, np_scores[:, 1], label=r"Player $2$", color="green", linestyle="--")
ax.plot(k, np_scores[:, 0], label=r"Player $1$", color="blue", linestyle=":")

# Draw thin, dotted grey lines at switching points
for i in [1.5, 2.0, 2.5, 3.0]:
    ax.axvline(i, linestyle=":", color="grey", linewidth=0.5)

# Style the legend
ax.legend(fancybox=False, edgecolor="black", framealpha=1.0)

# Set bounds for the axes
ax.set_xlim(1.0, 3.5)
ax.set_ylim(0.0, 1.0)

# Set labels
ax.set_xlabel(r"$k_3$")
ax.set_ylabel(r"Scores")

# Make plot 16:9
fig.set_size_inches(plot_width, plot_height)

# Save the plot
fig.savefig(plot_dir / "3p-scores.pdf", bbox_inches="tight", transparent=True)


###################### Prizes

# Create a plot of k vs np_prizes and export to .pdf
fig, ax = plt.subplots()

# Hide the spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Control the colors of the lines
ax.plot(
    k, np_prizes[:, 2], label=r"Player $3$", color="red", linestyle="-", linewidth=1.5
)
ax.plot(
    k,
    np_prizes[:, 1],
    label=r"Player $2$",
    color="green",
    linestyle="--",
    linewidth=1.5,
)
ax.plot(
    k, np_prizes[:, 0], label=r"Player $1$", color="blue", linestyle=":", linewidth=1.5
)

# Draw thin, dotted grey lines at switching points
for i in [1.5, 2.0, 2.5, 3.0]:
    ax.axvline(i, linestyle=":", color="grey", linewidth=0.5)

# Style the legend
ax.legend(fancybox=False, edgecolor="black", framealpha=1.0)

# Set bounds for the axes
ax.set_xlim(1.0, 3.5)
ax.set_ylim(0.0, 1)

# Set labels
ax.set_xlabel(r"$k_3$")
ax.set_ylabel(r"Prizes")

# Make plot 16:9
fig.set_size_inches(plot_width, plot_height)

# Save the plot
fig.savefig(plot_dir / "3p-prizes.pdf", bbox_inches="tight", transparent=True)
