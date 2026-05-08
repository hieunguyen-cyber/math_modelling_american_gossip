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

def plot_tau_distribution_violin(data_dict: dict, outpath: str | None = None):
    """Plot violin plots comparing the distribution of tau across different network models."""
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except OSError:
        plt.style.use('ggplot')
        
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = list(data_dict.keys())
    data = [data_dict[k] for k in labels]
    
    parts = ax.violinplot(data, showmeans=True, showmedians=False)
    
    # Customize colors
    for pc in parts['bodies']:
        pc.set_facecolor('#8b5cf6')
        pc.set_edgecolor('black')
        pc.set_alpha(0.7)
        
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels([l.upper() for l in labels])
    ax.set_ylabel('Spreading Time $\\tau$')
    ax.set_title('Distribution of Spreading Time by Network Model')
    
    fig.tight_layout()
    if outpath:
        fig.savefig(outpath, dpi=300)
    return fig

def plot_tau_vs_k_hexbin(k_vals: Sequence[int], tau_vals: Sequence[int], title: str, outpath: str | None = None):
    """Plot a 2D hexbin density plot for Spreading Time vs Degree."""
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except OSError:
        plt.style.use('ggplot')
        
    fig, ax = plt.subplots(figsize=(7, 5))
    hb = ax.hexbin(k_vals, tau_vals, gridsize=30, cmap='inferno', bins='log', mincnt=1)
    ax.set_xscale('log')
    ax.set_xlabel('Degree $k$ (log scale)')
    ax.set_ylabel('Spreading Time $\\tau$')
    ax.set_title(title)
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label('log10(count)')
    
    fig.tight_layout()
    if outpath:
        fig.savefig(outpath, dpi=300)
    return fig

def plot_model_comparison_bar(models: Sequence[str], means: Sequence[float], stds: Sequence[float], metric_name: str, outpath: str | None = None):
    """Bar chart comparing a metric across models with error bars."""
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except OSError:
        plt.style.use('ggplot')
        
    fig, ax = plt.subplots(figsize=(6, 4))
    x_pos = np.arange(len(models))
    
    ax.bar(x_pos, means, yerr=stds, align='center', alpha=0.8, ecolor='black', capsize=10, color=['#3b82f6', '#ef4444', '#10b981', '#f59e0b'])
    ax.set_ylabel(metric_name)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([m.upper() for m in models])
    ax.set_title(f'{metric_name} Comparison')
    
    fig.tight_layout()
    if outpath:
        fig.savefig(outpath, dpi=300)
    return fig
