import matplotlib.pyplot as plt
import numpy as np
from math import pi


def plot_step_matrics(df):
    plt.figure(figsize=(12, 6))
    for algo in df['Algorithm'].unique():
        algo_data = df[df['Algorithm'] == algo]
        avg_time = np.mean([steps for steps in algo_data['Step Time']], axis=0)
        avg_memory = np.mean([steps for steps in algo_data['Step Memory']], axis=0)
        plt.plot(avg_memory, linestyle = ';', marker='o', mfc='none', label=f'{algo} - Memory')
        plt.plot(avg_time, label=f'{algo} - Time')
        
    plt.xlabel('Steps')
    plt.ylabel('Time (s) / Memory (KB)')
    plt.title('Step-by-Step Performance')
    plt.legend()
    plt.show()
    
    
def plot_radar_chart(df):
    categories = ['Time', 'Memory', "Path Length"]
    num_vars = len(categories)
    
    df_normalized = df.groupby('Algorithm')[categories].mean()
    max_values = df_normalized.max().max()
    df_normalized = df_normalized / max_values
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]
    
    for algorithm in df['Algorithm'].unique():
        values = df_normalized.loc[algorithm].values.tolist()
        values += values[:1]
        ax.plot(angles, values, marker='o', label=algorithm)
        ax.fill(angles, values, alpha=0.25)
        
        
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)
    plt.xticks(angles[:-1], categories)
    plt.yticks([0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"])
    
    ax.grid(True)
    plt.title('Comparaison des Performances des Algorithmes (Normalise)')
    plt.legend(loc='upper right', bbox_to_archor=(1.3, 1.1))
    plt.tight_layout()
    plt.show()
    
    
def plot_performance_comparaison(stats):   
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    matrics = ['Time', 'Memory', 'Path Lenght']
    
    for i, metric in enumerate(matrics):
        means = stats[(metric, 'mean')]
        stds = stats[(metric, 'std')]
        
        axes[i].bar(means.index, means, yerr=stds, capsize=5)
        axes[i].set_title(f"{metric} Comparaison")
        axes[i].set_ylabel(metric)
        axes[i].set_xlabel('Algorithm')
        axes[i].grid(True)
        
    plt.tight_layout()
    plt.show()
    
    
    
def plot_boxplots(df):
    import seaborn as sns
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    sns.boxplot(x='Algorithm', y='Time', data=df, ax=axes[0], palette='Set3')
    axes[0].set_title('Boxplot of time', fontsize=14)
    axes[0].set_xlabel('Algorithm')
    axes[0].set_ylabel('Time')
    axes[0].grid(True, linestyle='--', alpha=0.6)
    
    sns.boxplot(x='Algorithm', y='Memory', data=df, ax=axes[1], palette='set3')
    axes[1].set_title('Boxplot of time', fontsize=14)
    # axes[1].set_ylim([0, 40])
    axes[1].set_xlabel('Algorithm')
    axes[1].set_ylabel('Time')
    axes[1].grid(True, linestyle='--', alpha=0.6)
    
    sns.boxplot(x='Algorithm', y='Time', data=df, ax=axes[2], palette='Set3')
    axes[2].set_title('Boxplot of time', fontsize=14)
    axes[2].set_xlabel('Algorithm')
    axes[2].set_ylabel('Time')
    axes[2].grid(True, linestyle='--', alpha=0.6)
    
    plt.show()
    
    
def plot_pie_charts(stats):
    matrics = ['Time', 'Memory', 'Path lenght']
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for i, metric in enumerate(matrics):
        means = stats[(metric, 'mean')]
        axes[i].pie(means, labels=means.index, autopct= '%1.1f%%', startangle=140)
        axes[i].set_title(f'{metric} Distribution')
        
    plt.show()