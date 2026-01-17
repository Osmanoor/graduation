import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from analysis.load_exp001_data import load_experiment_data
from analysis.analyze_exp001_quantitative import run_quantitative_analysis

print("="*60)
print("ERROR ANALYSIS - EXPERIMENT 001 (Dense Baseline)")
print("="*60)

# Load data
print("\nLoading data...")
topics, qrels, results = load_experiment_data()

# Run analysis
print("\nRunning quantitative analysis...")
analysis = run_quantitative_analysis(topics, qrels, results)

print("\nDONE!")
