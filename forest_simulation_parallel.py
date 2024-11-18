import numpy as np
import random
import time
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation
from concurrent.futures import ThreadPoolExecutor

# Constants
EMPTY = 0
TREE = 1
BURNING = 2

# Function to initialize the forest grid
def generate_forest(grid_size, tree_probability, burning_probability):
    forest = np.zeros((grid_size, grid_size), dtype=int)
    for i in range(grid_size):
        for j in range(grid_size):
            if random.random() < tree_probability:
                forest[i][j] = TREE
                if random.random() < burning_probability:
                    forest[i][j] = BURNING
    return forest

# Function to spread fire using Moore neighborhood algorithm
def spread_moore(forest, grid_size, immune_probability, lightning_probability):
    new_forest = np.copy(forest)
    for i in range(grid_size):
        for j in range(grid_size):
            if forest[i][j] == TREE:
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        if forest[x % grid_size][y % grid_size] == BURNING:
                            if random.random() < lightning_probability or random.random() < immune_probability:
                                new_forest[i][j] = BURNING
                                break
    return new_forest

# Function to simulate forest fire in parallel using threading
def simulate_forest_fire_parallel(grid_size, tree_probability, burning_probability, immune_probability, lightning_probability, iterations):
    forest = generate_forest(grid_size, tree_probability, burning_probability)
    with ThreadPoolExecutor(max_workers=iterations) as executor:
        for _ in range(iterations):
            forest = executor.submit(spread_moore, forest, grid_size, immune_probability, lightning_probability).result()
    return forest

# Function to simulate forest fire in parallel for animation frames
def simulate_animated_forest_fire_parallel(grid_size, tree_probability, burning_probability, immune_probability, lightning_probability, iterations):
    forest = generate_forest(grid_size, tree_probability, burning_probability)
    forest_states = [np.copy(forest)]
    with ThreadPoolExecutor(max_workers=iterations) as executor:
        for _ in range(iterations):
            forest = executor.submit(spread_moore, forest, grid_size, immune_probability, lightning_probability).result()
            forest_states.append(np.copy(forest))
    return forest_states


# Function to visualize animation
def visualize_animation(forest_evolution):
    cmap = ListedColormap(['white', 'green', 'orange'])
    fig, ax = plt.subplots()
    ax.set_title("Parallel Forest Fire Simulation")
    ax.set_axis_off()
    img = ax.imshow(forest_evolution[0], cmap=cmap, interpolation='nearest')
    
    def update_animation(frame):
        img.set_array(forest_evolution[frame])
        return (img,)
    
    ani = FuncAnimation(fig, update_animation, frames=len(forest_evolution), interval=500, blit=True)
    plt.show()

# Main function
def main():
    grid_size = 100
    tree_probability = 0.8
    burning_probability = 0.01
    immune_probability = 0.3
    lightning_probability = 0.001
    iterations = 10
    
    # Parallel implementation with animation
    print("Parallel implementation:")
    start_time = time.time()
    forest_evolution = simulate_animated_forest_fire_parallel(grid_size, tree_probability, burning_probability, immune_probability, lightning_probability, iterations)
    # forest_evolution = simulate_forest_fire_parallel(grid_size, tree_probability, burning_probability, immune_probability, lightning_probability, iterations)
    end_time = time.time()
    print(f"Grid size: {grid_size}x{grid_size}, Time: {(end_time - start_time) } seconds")
    visualize_animation(forest_evolution)

if __name__ == "__main__":
    main()
