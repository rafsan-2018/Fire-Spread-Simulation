import numpy as np
import random
import time
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation

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

# Function to spread fire using a von Neumann neighbourhood algorithm
def spread_fire(forest, grid_size, immune_probability, lightning_probability):
    for i in range(grid_size):
        for j in range(grid_size):
            if forest[i][j] == TREE:
                neighbors = forest[(i-1):(i+2) % grid_size, (j-1):(j+2) % grid_size]
                burning_neighbors = np.count_nonzero(neighbors == BURNING)
                if random.random() < lightning_probability or random.random() < immune_probability * burning_neighbors:
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

# Function to simulate forest fire sequentially with animation
def simulate_animated_forest_fire_sequential(grid_size, tree_probability, burning_probability, immune_probability, lightning_probability, iterations):
    forest = generate_forest(grid_size, tree_probability, burning_probability)
    forest_evolution = [np.copy(forest)]
    for _ in range(iterations):
        forest = spread_moore(forest, grid_size, immune_probability, lightning_probability)
        forest_evolution.append(np.copy(forest))
    return forest_evolution

# Function to simulate forest fire sequentially without animation
def simulate_forest_fire_sequential(grid_size, tree_probability, burning_probability, immune_probability, lightning_probability, iterations):
    forest = generate_forest(grid_size, tree_probability, burning_probability)
    for _ in range(iterations):
        forest = spread_moore(forest, grid_size, immune_probability, lightning_probability)
    return forest

# Function to update the plot for each animation frame
def update(frame, forest_evolution, cmap, img):
    img.set_data(forest_evolution[frame])
    return img,

def visualize_simulation(forest):
    cmap = ListedColormap(['white', 'green', 'orange'])
    plt.imshow(forest, cmap=cmap, interpolation='nearest')
    plt.colorbar()
    plt.title("Forest Fire Simulation")
    plt.show()

def visualize_animation(forest_evolution):
    cmap = ListedColormap(['white', 'green', 'orange'])
    fig, ax = plt.subplots()
    ax.set_title("Sequential Forest Fire Simulation")
    ax.set_axis_off()
    img = ax.imshow(forest_evolution[0], cmap=cmap, interpolation='nearest')
    ani = FuncAnimation(fig, update, frames=len(forest_evolution), fargs=(forest_evolution, cmap, img), interval=500, blit=True)
    plt.show()


def generate_forest_fire(grid_sizes, tree_probability, burning_probability, immune_probability, lightning_probability, iterations):
    # Generate forest evolution frames final result using Sequential implementation
    for size in grid_sizes:
        start_time = time.time()
        forest_seq = simulate_forest_fire_sequential(size, tree_probability, burning_probability, immune_probability, lightning_probability, iterations)
        end_time = time.time()
        print(f"Grid size: {size}x{size}, Time: {(end_time - start_time) } seconds")
        visualize_simulation(forest_seq)


def generate_animated_forest_fire(grid_size, tree_probability, burning_probability, immune_probability, lightning_probability, iterations):
    # Generate forest evolution frames animation using Sequential implementation
    print("Sequential implementation:")
    start_time = time.time()
    forest_evolution = simulate_animated_forest_fire_sequential(grid_size, tree_probability, burning_probability, immune_probability, lightning_probability, iterations)
    end_time = time.time()
    print(f"Grid size: {grid_size}x{grid_size}, Time: {(end_time - start_time) } seconds")
    visualize_animation(forest_evolution)
    

# Main function
def main():
    # grid_sizes = [100,400,800,1000,1200,2000]
    grid_sizes = [100]
    grid_size = 100
    tree_probability = 0.8
    burning_probability = 0.01
    immune_probability = 0.3
    lightning_probability = 0.001
    iterations = 10

    # generate_forest_fire(grid_sizes, tree_probability, burning_probability, immune_probability, lightning_probability, iterations)
    generate_animated_forest_fire(grid_size, tree_probability, burning_probability, immune_probability, lightning_probability, iterations)

if __name__ == "__main__":
    main()

