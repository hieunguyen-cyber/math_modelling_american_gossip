import sys
import os
import csv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from visualization.static_plots import plot_spread_vs_degree, plot_degree_distribution, plot_probability_sweep
from graphs import generate_ba, generate_er, generate_ws, generate_apollonian
import matplotlib.pyplot as plt

def generate_degree_distributions():
    os.makedirs('outputs/figures', exist_ok=True)
    # BA
    G_ba = generate_ba(5000, 3)
    fig_ba = plot_degree_distribution([d for n, d in G_ba.degree()], title="BA Scale-Free Degree Distribution", outpath='outputs/figures/dist_ba.png')
    plt.close(fig_ba)
    
    # ER
    G_er = generate_er(5000, 0.002)
    fig_er = plot_degree_distribution([d for n, d in G_er.degree()], title="ER Random Degree Distribution", outpath='outputs/figures/dist_er.png')
    plt.close(fig_er)
    
    # WS
    G_ws = generate_ws(5000, 6, 0.1)
    fig_ws = plot_degree_distribution([d for n, d in G_ws.degree()], title="WS Small-World Degree Distribution", outpath='outputs/figures/dist_ws.png')
    plt.close(fig_ws)

    # Apollonian
    G_ap = generate_apollonian(1000) # smaller n due to generation cost
    fig_ap = plot_degree_distribution([d for n, d in G_ap.degree()], title="Apollonian Degree Distribution", outpath='outputs/figures/dist_apollonian.png')
    plt.close(fig_ap)

def plot_probability_results():
    os.makedirs('outputs/figures', exist_ok=True)
    for gtype in ['ba', 'er', 'ws']:
        filepath = f'outputs/processed/probability_sweep_{gtype}.csv'
        if not os.path.exists(filepath):
            continue
        
        qs, f_means, f_stds, tau_means, tau_stds = [], [], [], [], []
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                qs.append(float(row['q']))
                f_means.append(float(row['f_mean']))
                f_stds.append(float(row['f_std']))
                tau_means.append(float(row['tau_mean']))
                tau_stds.append(float(row['tau_std']))
        
        fig = plot_probability_sweep(qs, f_means, f_stds, tau_means, tau_stds, label=gtype.upper(), outpath=f'outputs/figures/prob_sweep_{gtype}.png')
        plt.close(fig)

def demo_save():
    os.makedirs('outputs/figures', exist_ok=True)
    ks = [1,2,3,4,5,10,20,50]
    fs = [0.1,0.15,0.2,0.25,0.28,0.35,0.4,0.45]
    fig = plot_spread_vs_degree(ks, fs, outpath='outputs/figures/spread_vs_k.png')
    plt.close(fig)

if __name__ == '__main__':
    print("Generating figures...")
    demo_save()
    generate_degree_distributions()
    plot_probability_results()
    print("All figures saved to outputs/figures/")
