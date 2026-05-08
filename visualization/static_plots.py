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

def plot_probability_sweep(q_vals, f_means, f_stds, tau_means, tau_stds, label: str, outpath: str | None = None):
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except OSError:
        plt.style.use('ggplot')
        
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Plot f vs q
    ax1.errorbar(q_vals, f_means, yerr=f_stds, fmt='-o', capsize=4, label=label, color='#d97706')
    ax1.set_xlabel('Probability $q$')
    ax1.set_ylabel('Spread factor $f$')
    ax1.set_title('Spread Factor vs Probability')
    ax1.legend()
    
    # Plot tau vs q
    ax2.errorbar(q_vals, tau_means, yerr=tau_stds, fmt='-s', capsize=4, label=label, color='#0d9488')
    ax2.set_xlabel('Probability $q$')
    ax2.set_ylabel('Spreading time $\\tau$')
    ax2.set_title('Spreading Time vs Probability')
    ax2.legend()
    
    fig.tight_layout()
    if outpath:
        fig.savefig(outpath, dpi=300)
    return fig

def plot_scaling_laws(n_vals, metric_means, metric_stds, metric_name: str, label: str, outpath: str | None = None):
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except OSError:
        plt.style.use('ggplot')
        
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.errorbar(n_vals, metric_means, yerr=metric_stds, fmt='-^', capsize=4, label=label, color='#7e22ce')
    ax.set_xlabel('Network Size $N$')
    ax.set_ylabel(metric_name)
    ax.set_xscale('log')
    if 'time' in metric_name.lower():
        ax.set_yscale('log')
    ax.set_title(f'{metric_name} vs Network Size')
    ax.legend()
    
    fig.tight_layout()
    if outpath:
        fig.savefig(outpath, dpi=300)
    return fig

def plot_degree_distribution(degrees: Sequence[int], title: str = "Degree Distribution", outpath: str | None = None):
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except OSError:
        plt.style.use('ggplot')
        
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = np.bincount(degrees)
    k_vals = np.nonzero(counts)[0]
    p_k = counts[k_vals] / len(degrees)
    
    ax.scatter(k_vals, p_k, s=30, alpha=0.8, color='#2563eb')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Degree $k$')
    ax.set_ylabel('$P(k)$')
    ax.set_title(title)
    
    fig.tight_layout()
    if outpath:
        fig.savefig(outpath, dpi=300)
    return fig
