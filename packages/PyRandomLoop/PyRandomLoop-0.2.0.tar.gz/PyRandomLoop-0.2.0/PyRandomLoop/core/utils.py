import numpy as np
import json
from collections import deque
import colorsys
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

__all__ = ['generate_rgb_colors', 'create_cmap', 'infer_style', 'NumpyEncoder', 'bfs']

#################### global variables ########################

GAMMA = 1.5   # changes the gradient of the colormap, high GAMMA means similar colors, big gap with the background, GAMMA = 1 means the gradient is linear which cause low visibility sometimes
plt.style.use("dark_background")  # set dark background as default style
plt.rcParams['animation.embed_limit'] = 128 # Set the limit to 100 MB (default is 21 MB)


def generate_rgb_colors(n):
    """
    Generates n RGB colors in the form of (r, g, b) with r, g, b values in [0, 1],
    maximizing the perceptual difference between the colors, ensuring they are bright and vivid.
    """
    colors = []
    
    for i in range(n):
        hue = i / n
        saturation = 1  # Max saturation for vivid colors
        lightness = 0.5  # Lightness set to 0.5 for bright colors
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append(rgb)
    
    return colors

def create_cmap(num_colors, color, n_bins):  # create a color map to show how many links are in a edge   ############## Gamma and cmap norm to fine tune 
    
    # get current style
    current_style = infer_style()
    if current_style == 'dark_background':
        background_color = (0,0,0)
        gamma = 1 / GAMMA
    else:
        background_color = (1,1,1)
        gamma = GAMMA
    
    target_color = generate_rgb_colors(num_colors)[color]
    '''
    if color == 0:
        target_color = (1, 0, 0)  # Red
    elif color == 1:
        target_color = (0, 1, 0)  # Green
    elif color == 2:
        target_color = (0, 0, 1)  # Blue
    else:
        target_color = (0.8, 0, 1)  # Magenta-like for any color > 2
    '''
    # Generate interpolated colors with gamma correction
    colors = np.array([np.linspace(background_color[i], target_color[i], n_bins) for i in range(3)])
    colors = np.power(colors, gamma).T  # Apply gamma correction and transpose to get the correct shape  gamma = 0.5 to brighten the cmap
    
    # Create the colormap
    cmap = ListedColormap(colors, name = 'my_cmap')
    return cmap


def infer_style():
    for style_name, style_params in plt.style.library.items():
        if all(key in plt.rcParams and plt.rcParams[key] == val for key, val in style_params.items()):
            return style_name
    return 'Default'

class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert ndarray to list
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
        

def bfs(perc_conf, x):
    """
    Perform a BFS from the given vertex x, marking all visited vertices. If vertex y is found, return 1
    Vertex x should be on the left/bottom of the grid
    """
    grid_size = perc_conf.shape[0]
    visited = np.zeros(shape=(grid_size, grid_size))
    queue = deque()
    
    # Set current vertex as visited, add it to the queue
    visited[x[0], x[1]] = 1 
    queue.append(x) 
    
    if x[0] == 0: # x is on the left border
        horiz = True 
    elif x[1] == 0:
        horiz = False 
    else:
        print(x) 
        
    # Iterate over the queue
    while queue:
        # Dequeue 
        currentVertex = queue.popleft()
        
        # check here
        if horiz:
            if currentVertex[0] == grid_size - 2:
                #print(f'Reached vertex {currentVertex}')
                return 1, None
        else:
            if currentVertex[1] == grid_size - 2:
                #print(f'Reached vertex {currentVertex}')
                return 1, None
            
        # Get all neighbours of currentVertex        
        # If an adjacent has not been visited, then mark it visited and enqueue it
        if perc_conf[currentVertex[0], currentVertex[1], 0] == 1 and not visited[currentVertex[0]-1, currentVertex[1]]:
            # left neighbour
            visited[currentVertex[0]-1, currentVertex[1]] = 1
            queue.append((currentVertex[0]-1, currentVertex[1]))
            
        if perc_conf[currentVertex[0], currentVertex[1], 1] == 1 and not visited[currentVertex[0], currentVertex[1]-1]:
            # bottom neighbour
            visited[currentVertex[0], currentVertex[1]-1] = 1
            queue.append((currentVertex[0], currentVertex[1]-1))
            
        if perc_conf[currentVertex[0]+1, currentVertex[1], 0] == 1 and not visited[currentVertex[0]+1, currentVertex[1]]:
            # right neighbour
            visited[currentVertex[0]+1, currentVertex[1]] = 1
            queue.append((currentVertex[0]+1, currentVertex[1]))
            
        if perc_conf[currentVertex[0], currentVertex[1]+1, 1] == 1 and not visited[currentVertex[0], currentVertex[1]+1]:
            # top neighbour
            visited[currentVertex[0], currentVertex[1]+1] = 1
            queue.append((currentVertex[0], currentVertex[1]+1))
              
    return 0, visited