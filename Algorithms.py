import time 
import tracemalloc
from collections import deque
import heapq

#heuristic ( distance de manhattan )
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

#definer les directions possibles
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#fonction pour obtenir les voisins valides
def get_neighbors(node, Maze):
    x, y = node
    return [(x+dx, y+dy) for dx, dy in directions if (x+dx, y+dy) in Maze and Maze[(x+dx, y+dy)] == 0]


def a_star(start, goal, Maze, heuristic):
    matrics = {'time': [], 'memory': []}
    tracemalloc.start()
    start_time = time.time()
    
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), start))
    came_from = {start: None}
    g_score = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        matrics['time'].append(time.time() - start_time)
        matrics['memory'].append(tracemalloc.get_traced_memory()[1] / 1024)    # en KB
        
        if current == goal:
            break 
        
        for neighbor in get_neighbors(current, Maze):
            tentative_g  = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current 
                g_score[neighbor] = tentative_g 
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))
    
    tracemalloc.stop()
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from.get(current)
    return path[::-1], matrics



def gbfs(start, goal, Maze, heuristic):
    matrics = {'time': [], 'memory': []}
    tracemalloc.start()
    start_time = time.time()
    
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {start: None}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        matrics['time'].append(time.time() - start_time)
        matrics['memory'].append(tracemalloc.get_traced_memory()[1] / 1024)
        
        if current == goal:
            break
        
        for neighbor in get_neighbors(current, Maze):
            if neighbor not in came_from:
                came_from[neighbor] = current
                priority = heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))
    
    tracemalloc.stop()
    path = []
    current = goal 
    while current:
        path.append(current)
        current = came_from.get(current)
    return path[::-1], matrics


def bfs(start, goal, Maze):
    matrics = {'time': [], 'memory': []}
    tracemalloc.start()
    start_time = time.time()
    
    queue = deque([start])
    came_from = {start: None}
    
    while queue:
        current = queue.popleft()
        
        matrics['time'].append(time.time() - start_time)
        matrics['memory'].append(tracemalloc.get_traced_memory()[1] / 1024)
        
        if current == goal:
            break
        
        for neighbor in get_neighbors(current, Maze):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)
                
    tracemalloc.stop()
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from.get(current)
    return path[::-1], matrics


def dfs(start, goal, Maze):
    matrics = {'time': [], 'memory': []}
    tracemalloc.start()
    start_time = time.time()
    
    stack = [start]
    came_from = {start: None}
    
    while stack:
        current = stack.pop()
        
        matrics['time'].append(time.time() - start_time)
        matrics['memory'].append(tracemalloc.get_traced_memory()[1] / 1024)
        
        if current == goal:
            break
        
        for neighbor in get_neighbors(current, Maze):
            if neighbor not in came_from:
                came_from[neighbor] = current
                stack.append(neighbor)
                
    tracemalloc.stop()
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from.get(current)
    return path[::-1], matrics