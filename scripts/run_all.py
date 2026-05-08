"""Top-level CLI to run a sequence of reproduction steps."""
import argparse
from experiments import reproduce_epl, reproduce_pre

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--step', type=str, default='epl', choices=['epl','pre'])
    args = parser.parse_args()
    if args.step == 'epl':
        reproduce_epl.run_basic()
    else:
        reproduce_pre.run_probability_experiment()

if __name__ == '__main__':
    main()
