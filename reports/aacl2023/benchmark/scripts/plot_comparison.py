from pathlib import Path

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import typer
import numpy as np

from .constants import MATPLOTLIB_STYLE

pylab.rcParams.update(MATPLOTLIB_STYLE)


# Better to handwrite it here than keeping it in the VM.
RESULTS = {
    "WikiANN": [19.92, 24.41, 23.38, 31.28, 29.20],
    "TLUnified-NER": [30.24, 45.09, 58.90, 57.67, 59.26],
    # "Baseline": [19.92, 30.24],
    # "fastText": [24.41, 45.09],
    # "RoBERTa": [23.38, 58.90],
    # "XLM-RoBERTa": [31.28, 57.67],
    # "Multi. BERT": [29.20, 59.26],
}


def plot_comparison(outfile: Path):
    labels = ["Baseline", "fastText", "RoBERTa", "XLM-RoBERTa", "Multi. BERT"]

    # Set how the bars will be separated
    width = 0.25  # the width of the bars
    x = np.arange(len(labels))
    coords = np.array([-0.125, 0.125])

    # Design
    white = "#fffff8"
    red = "#a00000"
    colors = [white, red]

    fig, ax = plt.subplots(figsize=(8, 4))
    # Data
    rects = []
    for idx, (xy, (model, results)) in enumerate(zip(coords, RESULTS.items())):
        rects.append(ax.bar(x + xy, results, width, label=model, color=colors[idx], edgecolor="#353935"))

    ax.set_ylabel("F1-score")
    ax.set_xticks([0,1,2,3,4])
    ax.set_xticklabels(labels)
    ax.set_ylim(top=100)
    ax.legend(title="Training set", frameon=False, **{"title_fontsize":14})
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
    typer.run(plot_comparison)
