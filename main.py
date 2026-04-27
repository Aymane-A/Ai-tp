import time 
import tracemalloc

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from collections import deque
import heapq

from math import pi 

from visualisation import plot_step_matrics, plot_radar_chart, plot_boxplots, plot_pie_charts, plot_performance_comparaison
from Algorithms import *
from ConfigMaze import width, height, start, goal, Maze


def run_experiments(algorithms, runs=100):
    results = []
    for name, algo in algorithms.items():
        for _ in range(runs):
            path, matrics = algo(start, goal)
            results.append({
                'Algorithm': name, 
                'Time': matrics['time'][-1],
                'Memory': matrics['memory'][-1],
                'Path Length': len(path),
                'Step Time': matrics['time'],
                'Step Memory': matrics['memory']
            })
    return pd.DataFrame(results)

if __name__ == "__main__":
    algorithms = {
        'BFS': lambda s, g: bfs(s, g, Maze),
        'DFS': lambda s, g: dfs(s, g, Maze),
        'A*': lambda s, g: a_star(s, g, Maze, heuristic),
        'GBFS': lambda s, g: gbfs(s, g, Maze, heuristic)
    }
    df = run_experiments(algorithms)
        
    stats = df.groupby('Algorithm').agg({
        'Time': ['mean', 'std'], 
        'Memory': ['mean', 'std'],
        'Path Length': ['mean', 'std']
    })
    print(stats)
    
    plot_step_matrics(df)
    plot_radar_chart(df)
    plot_boxplots(df)
    plot_pie_charts(stats)
    plot_performance_comparaison(stats)