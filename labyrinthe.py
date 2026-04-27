#Definir le labyrithe 
# 0 = libre, 1 = mur 
from collections import deque

maze = {
    (0, 0): 0, (0, 1): 1, (0, 2): 0, (0, 3): 0,
    (1, 0): 0, (1, 1): 1, (1, 2): 0, (1, 3): 1,
    (2, 0): 0, (2, 1): 0, (2, 2): 0, (2, 3): 1,
    (3, 0): 0, (3, 1): 1, (3, 2): 0, (3, 3): 0,
}

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_neighbors(node):
    x, y = node
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (nx, ny) in maze and maze[(nx, ny)] == 0:
            neighbors.append((nx, ny))
    return neighbors

#affichage
def print_maze(maze, path=None):
    for x in range(4):
        for y in range(4):
            if path and (x, y) in path:
                print("P", end=" ")  #chemin
            elif maze[(x,y)] == 1:
                print("#", end=" ")  # Mur
            else:
                print(".", end=" ")  #libre
        print()


#BFS
def bfs(start, goal):
    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break 
        for neighbor in get_neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    return path[::-1]




#DFS
def dfs(start, goal):
    stack = [start]
    came_from = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            break
        for neighbor in get_neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                stack.append(neighbor)

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    return path[::-1]


#Execution
start = (0, 0)
goal = (3, 3)

print("labyrithe initial: ")
print_maze(maze)

print("\nChemin BFS:")
bfs_path = bfs(start, goal)
print_maze(maze, bfs_path)

print("\nChemin DFS:")
dfs_path = dfs(start, goal)
print_maze(maze, dfs_path)

#test empirique
import time
import tracemalloc
import matplotlib.pyplot as plt 

def measure_performance(algorithm, start, goal):
    start_time = time.time()
    tracemalloc.start()

    path = algorithm(start, goal)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    elapsed_time = time.time() - start_time

    return path, elapsed_time, peak / 1024  #convertion en KB

algorithms = [
    (bfs, "BFS"),
    (dfs, "DFS"), 
]


results = []
paths = {}
for algo, name in algorithms:
    path, time_taken, mem_used = measure_performance(algo, start, goal)
    paths[name] = path
    results.append((name, len(path), time_taken, mem_used))


#affichage des resultats
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
#donnees pour les graphiques
names = [res[0] for res in results]
times = [res[2] * 1000 for res in results]

memory = [res[3] for res in results]
lenghts = [res[1] for res in results]

#Graphique du temps d'execution
ax1.bar(names, times, color='skyblue')
ax1.set_title("Temps d'exécution")
ax1.set_ylabel('Millisecondes')
ax1.grid(axis='y', linestyle='--')

#Graphique de la memorie utilisee
ax2.bar(names, memory, color='lightgreen')
ax2.set_title('Mémoire utilisée')
ax2.set_ylabel('Kilobytes')
ax2.grid(axis='y', linestyle='--')

#Graphique de la longueur du chemin
ax3.bar(names, lenghts, color='salmon')
ax3.set_title('Longueur du chemin')
ax3.set_ylabel('Nombre de noeuds')
ax3.grid(axis='y', linestyle='--')

plt.tight_layout()
plt.show()