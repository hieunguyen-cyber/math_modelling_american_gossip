from typing import Sequence
import matplotlib.pyplot as plt
import numpy as np

def plot_spread_vs_degree(degrees: Sequence[int], spreads: Sequence[float], outpath: str | None = None):
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except OSError:
        plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(6,4))
    ax.scatter(degrees, spreads, s=20, alpha=0.7)
    ax.set_xlabel('Degree k')
    ax.set_ylabel('Spread factor f')
    ax.set_xscale('log')
    ax.set_title('Spread factor vs degree')
    fig.tight_layout()
    if outpath:
        fig.savefig(outpath, dpi=300)
    return fig
