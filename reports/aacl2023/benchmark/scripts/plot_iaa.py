from pathlib import Path

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import typer

from .constants import MATPLOTLIB_STYLE

pylab.rcParams.update(MATPLOTLIB_STYLE)


# Better to handwrite it here than keeping it in the VM.
RESULTS = {
    "num_samples": [500, 1024, 2113, 3410, 4096, 6000],
    "k_all": [0.42, 0.46, 0.63, 0.70, 0.77, 0.84],
    "k_annotated": [0.25, 0.29, 0.42, 0.53, 0.60, 0.67],
    "f1_score": [0.64, 0.68, 0.80, 0.89, 0.92, 0.96],
}


def plot_iaa(outfile: Path):
    fig, ax = plt.subplots(figsize=(5, 5))

    # Data
    ax.plot(
        RESULTS.get("num_samples"),
        RESULTS.get("f1_score"),
        color="k",
        linestyle="dashed",
        marker="^",
        label="F1-score",
    )
    ax.plot(
        RESULTS.get("num_samples"),
        RESULTS.get("k_all"),
        color="k",
        linestyle="solid",
        marker="o",
        label="Cohen's Kappa (all tokens)",
    )
    ax.plot(
        RESULTS.get("num_samples"),
        RESULTS.get("k_annotated"),
        color="k",
        marker="x",
        linestyle="dotted",
        label="Cohen's Kappa (annotated only)",
    )

    # Labels
    ax.set_xlabel("Number of examples")
    ax.set_ylabel("Inter-annotator agreement")
    ax.legend(loc="lower right", frameon=False)

    # Formatting
    # Hide the right and top splines
    # ax.set_title("Growth of IAA for each annotation round")
    ax.set_ylim([0, 1.0])
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)

    fig.tight_layout()
    plt.savefig(outfile, transparent=True)


if __name__ == "__main__":
    typer.run(plot_iaa)
