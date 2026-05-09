import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

plt.style.use('seaborn-v0_8-paper')
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'legend.fontsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
})

def log_func(k, a, b):
    return a + b * np.log(k)

def plot_epl_f_vs_k(data, outpath):
    fig, ax = plt.subplots(figsize=(7, 5))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    markers = ['o', 's', '^']
    
    for i, m in enumerate([3, 5, 7]):
        key = f'ba_m{m}'
        if key in data:
            k = np.array(data[key]['k'])
            f = np.array(data[key]['f'])
            
            # sort by k
            idx = np.argsort(k)
            k, f = k[idx], f[idx]
            
            # moving average to smooth the noisy f values
            if len(f) > 5:
                window = 5
                f_smooth = np.convolve(f, np.ones(window)/window, mode='valid')
                k_smooth = k[window//2 : -window//2 + 1] if window%2 != 0 else k[window//2 - 1 : -window//2]
            else:
                k_smooth, f_smooth = k, f
                
            ax.plot(k_smooth, f_smooth, marker=markers[i], linestyle='-', markersize=4, alpha=0.7, color=colors[i], label=f'BA (m={m})')
    
    ax.plot(np.linspace(2, 1000, 100), 1/np.linspace(2, 1000, 100), 'k--', label='f = 1/k')
    
    ax.set_xscale('log')
    ax.set_xlabel('Degree $k$')
    ax.set_ylabel('Spread factor $f$')
    ax.set_title('Spread factor vs Degree')
    ax.legend()
    fig.tight_layout()
    fig.savefig(outpath, dpi=300)
    plt.close(fig)

def plot_epl_tau_vs_k(data, outpath):
    fig, ax = plt.subplots(figsize=(7, 5))
    
    colors = ['#1f77b4', '#d62728']
    
    # Plot BA m=7
    if 'ba_m7' in data:
        k = np.array(data['ba_m7']['k'])
        tau = np.array(data['ba_m7']['tau'])
        idx = np.argsort(k)
        k, tau = k[idx], tau[idx]
        
        # Fit A + B log k
        mask = k > 10
        if np.any(mask):
            popt, _ = curve_fit(log_func, k[mask], tau[mask])
            ax.plot(k[mask], log_func(k[mask], *popt), 'k-', linewidth=2, label=f'BA Fit: {popt[0]:.2f} + {popt[1]:.2f}ln(k)')
            
        ax.scatter(k, tau, color=colors[0], alpha=0.6, s=20, label='BA (m=7)')

    # Plot APL gen6
    if 'apl_gen6' in data:
        k = np.array(data['apl_gen6']['k'])
        tau = np.array(data['apl_gen6']['tau'])
        idx = np.argsort(k)
        k, tau = k[idx], tau[idx]
        
        mask = k > 0
        if np.any(mask):
            popt, _ = curve_fit(log_func, k[mask], tau[mask])
            ax.plot(k[mask], log_func(k[mask], *popt), 'k--', linewidth=2, label=f'APL Fit: {popt[0]:.2f} + {popt[1]:.2f}ln(k)')
        
        ax.scatter(k, tau, color=colors[1], marker='^', alpha=0.6, s=30, label='APL (gen=6)')

    ax.set_xscale('log')
    ax.set_xlabel('Degree $k$')
    ax.set_ylabel('Spreading time $\\tau$')
    ax.set_title('Spreading time vs Degree')
    ax.legend()
    fig.tight_layout()
    fig.savefig(outpath, dpi=300)
    plt.close(fig)

def plot_epl_p_tau(data, outpath):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # BA m=7
    if 'ba_m7' in data:
        raw_tau = data['ba_m7']['raw_tau']
        counts = np.bincount(raw_tau)
        t_vals = np.nonzero(counts)[0]
        p_t = counts[t_vals] / len(raw_tau)
        
        ax1.plot(t_vals, p_t, 'bo-', label='BA m=7')
        
        # Fit exp(-tau * (1-gamma)/B) for large tau
        mask = t_vals >= 4
        if np.sum(mask) > 2:
            popt, _ = np.polyfit(t_vals[mask], np.log(p_t[mask]), 1, cov=True)
            ax1.plot(t_vals[mask], np.exp(popt[1]) * np.exp(popt[0] * t_vals[mask]), 'k-', label=f'Fit slope: {popt[0]:.2f}')
        
        ax1.set_yscale('log')
        ax1.set_xlabel('$\\tau$')
        ax1.set_ylabel('$P(\\tau)$')
        ax1.set_title('Distribution of $\\tau$ (BA)')
        ax1.legend()
        
    # APL gen6
    if 'apl_gen6' in data:
        raw_tau = data['apl_gen6']['raw_tau']
        counts = np.bincount(raw_tau)
        t_vals = np.nonzero(counts)[0]
        p_t = counts[t_vals] / len(raw_tau)
        
        ax2.plot(t_vals, p_t, 'r^-', label='APL gen=6')
        
        mask = t_vals >= 2
        if np.sum(mask) > 2:
            popt, _ = np.polyfit(t_vals[mask], np.log(p_t[mask]), 1, cov=True)
            ax2.plot(t_vals[mask], np.exp(popt[1]) * np.exp(popt[0] * t_vals[mask]), 'k-', label=f'Fit slope: {popt[0]:.2f}')
            
        ax2.set_yscale('log')
        ax2.set_xlabel('$\\tau$')
        ax2.set_ylabel('$P(\\tau)$')
        ax2.set_title('Distribution of $\\tau$ (APL)')
        ax2.legend()

    fig.tight_layout()
    fig.savefig(outpath, dpi=300)
    plt.close(fig)

def plot_pre_local_sweep(data, outpath):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    local = data.get('local', {})
    q_vals = []
    f_means = []
    tau_means = []
    
    for q_str in sorted(local.keys(), key=lambda x: float(x.split('_')[1])):
        q = float(q_str.split('_')[1])
        q_vals.append(q)
        f_means.append(local[q_str]['f_mean'])
        tau_means.append(local[q_str]['tau_mean'])
        
    ax1.plot(q_vals, f_means, 's-', color='#d97706', linewidth=2, markersize=8)
    ax1.set_xlabel('Probability $q$')
    ax1.set_ylabel('Spread factor $f$')
    ax1.set_title('Average Spread Factor vs Probability')
    
    ax2.plot(q_vals, tau_means, 'o-', color='#0d9488', linewidth=2, markersize=8)
    ax2.set_xlabel('Probability $q$')
    ax2.set_ylabel('Spreading time $\\tau$')
    ax2.set_title('Average Spreading Time vs Probability')
    
    fig.tight_layout()
    fig.savefig(outpath, dpi=300)
    plt.close(fig)

def plot_pre_entire_network(data, outpath):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    entire = data.get('entire', {})
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for i, q_str in enumerate(sorted(entire.keys())):
        q = float(q_str.split('_')[1])
        k = np.array(entire[q_str]['k'])
        F_N = np.array(entire[q_str]['F_N'])
        tau_max = np.array(entire[q_str]['tau_max'])
        
        idx = np.argsort(k)
        k, F_N, tau_max = k[idx], F_N[idx], tau_max[idx]
        
        ax1.plot(k, F_N, 'o', alpha=0.6, color=colors[i], label=f'q = {q}')
        ax2.plot(k, tau_max, 's', alpha=0.6, color=colors[i], label=f'q = {q}')

    ax1.set_xscale('log')
    ax1.set_xlabel('Degree $k$')
    ax1.set_ylabel('$F_N$')
    ax1.set_title('Global Reach ($F_N$) vs Degree')
    ax1.legend()
    
    ax2.set_xscale('log')
    ax2.set_xlabel('Degree $k$')
    ax2.set_ylabel('Max Spreading Time $\\tau_{max}$')
    ax2.set_title('Global Spreading Time vs Degree')
    ax2.legend()
    
    fig.tight_layout()
    fig.savefig(outpath, dpi=300)
    plt.close(fig)

def main():
    os.makedirs('outputs/figures', exist_ok=True)
    
    # Load EPL results
    if os.path.exists('outputs/epl_results.json'):
        print("Generating EPL figures...")
        with open('outputs/epl_results.json', 'r') as f:
            epl_data = json.load(f)
        plot_epl_f_vs_k(epl_data, 'outputs/figures/epl_f_vs_k.pdf')
        plot_epl_tau_vs_k(epl_data, 'outputs/figures/epl_tau_vs_k.pdf')
        plot_epl_p_tau(epl_data, 'outputs/figures/epl_p_tau.pdf')
    else:
        print("outputs/epl_results.json not found.")

    # Load PRE results
    if os.path.exists('outputs/pre_results.json'):
        print("Generating PRE figures...")
        with open('outputs/pre_results.json', 'r') as f:
            pre_data = json.load(f)
        plot_pre_local_sweep(pre_data, 'outputs/figures/pre_local_sweep.pdf')
        plot_pre_entire_network(pre_data, 'outputs/figures/pre_entire_network.pdf')
    else:
        print("outputs/pre_results.json not found.")
        
    print("All figures generated in outputs/figures/")

if __name__ == '__main__':
    main()
