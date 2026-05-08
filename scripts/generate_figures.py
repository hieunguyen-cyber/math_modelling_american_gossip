"""Generate publication-quality figures used by experiments."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from visualization.static_plots import plot_spread_vs_degree
import matplotlib.pyplot as plt

def demo_save():
    ks = [1,2,3,4,5,10,20,50]
    fs = [0.1,0.15,0.2,0.25,0.28,0.35,0.4,0.45]
    fig = plot_spread_vs_degree(ks, fs, outpath='outputs/spread_vs_k.png')
    plt.close(fig)

if __name__ == '__main__':
    demo_save()
