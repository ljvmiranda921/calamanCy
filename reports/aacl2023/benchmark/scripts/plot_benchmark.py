from pathlib import Path

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import typer
import numpy as np

from .constants import MATPLOTLIB_STYLE

pylab.rcParams.update(MATPLOTLIB_STYLE)


# Better to handwrite it here than keeping it in the VM.
# PER, ORG, LOC, Overall
RESULTS = {
    "Baseline": [87.85, 74.80, 81.03, 84.57],
    "fastText": [91.20, 85.39, 88.38, 88.90],
    "RoBERTa": [92.18, 87.30, 90.01, 90.34],
    "XLM-RoBERTa": [91.95, 84.84, 88.92, 88.03],
    "Multi. BERT": [90.78, 85.08, 88.45, 87.40],
}


def plot_benchmark(outfile: Path):
    labels = ["PER", "ORG", "LOC", "Overall"]

    # Set how the bars will be separated
    width = 0.20  # the width of the bars
    x = np.arange(len(labels))
    coords = np.array([-0.4, -0.2, 0, 0.2, 0.40])

    # Design
    white = "#fffff8"
    red = "#a00000"
    hatches = ["", "/", "", "\\", "-"]
    colors = [white, white, red, white, white]

    fig, ax = plt.subplots(figsize=(8, 6))
    # Data
    rects = []
    for idx, (xy, (model, results)) in enumerate(zip(coords, RESULTS.items())):
        rects.append(ax.bar(1.5*x + xy, results, width, label=model, color=colors[idx], edgecolor="#353935", hatch=hatches[idx]))

    ax.set_ylabel("F1-score")
    ax.set_xticks(np.arange(0,6,1.5))
    ax.set_xticklabels(labels)
    ax.set_ylim(top=100)
    ax.legend(ncol=5, frameon=False, loc=(-0.1, -0.125))
    # Hide the right and top splines
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)


    def _autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                "{:.0f}".format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

    for rect in rects:
        _autolabel(rect)

    fig.tight_layout()
    plt.savefig(outfile, transparent=True, dpi=300)

if __name__ == "__main__":
    typer.run(plot_benchmark)
