# Configuration du lybiranthe 

# definir le lybiranthe aleatoire

import random 

def generate_Maze(width, height, path, start, goal):
    Maze = {}
    
    for y in range(height):
        for x in range(width):
            Maze[(x, y)] = 1
            
    for coord in path:
        Maze[coord] = 0
        
    Maze[start] = 0
    Maze[goal] = 0
    
    return Maze 

# Exemple d'utilisation
width = 100
height = 10 
start = (0, 0)
goal = (9, 9)

def initialize_path(path, width, height):
    i, j = 0, 0
    for i in range(0, height//2 ):
        path.append((i, j))
    
    for j in range(0, int(width/2)):
        path.append((i, j))
        
    for i in range(0, height//2 ):
        path.append((i, j))
        
    for j in range(width//2, width -1):
        path.append((0, j))
        
    for i in range(0, height):
        path.append((i, width-1))
        
    return path 

path = []
path = initialize_path(path, width, height)
Maze = generate_Maze(width, height, path, start, goal)
        
    