# src/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns

def save_visualization(data, title, filename):
    """Save a visualization to a file."""
    plt.figure(figsize=(10, 6))
    sns.barplot(x=data.index, y=data.values)
    plt.title(title)
    plt.xlabel('Categories')
    plt.ylabel('Counts')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()



def save_visualization_mutli_dim(data, title, filename):
    """Save a visualization to a file."""
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, x='VEH_BODY_STYL_ID', y='counts', hue='PRSN_ETHNICITY_ID')
    plt.title(title)
    plt.xlabel('Vehicle Body Style')
    plt.ylabel('Counts')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()