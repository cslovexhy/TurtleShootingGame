from MazeGenerator import MazeGenerator
import random

# Set seed for reproducible maze
random.seed(123)

# Create maze generator (70x38 to match your level dimensions)
maze_gen = MazeGenerator(70, 38, wall_char='s', empty_char='.')

# Generate maze with 3-wide paths
maze_gen.generate_recursive_backtracking()

# Add fewer openings since paths are already wider
maze_gen.add_openings(opening_density=0.02)

# Place fewer entities for simpler gameplay
entities = {
    'p': 1,  # player
    '0': 2,  # bikers
    '1': 1,  # enforcer
    'F': 1,  # fire ball item
    'I': 1,  # ice ball item
}

maze_gen.place_entities(entities)

# Generate level string
level_string = maze_gen.to_level_string()

print('all_levels[9] = """')
print(level_string)
print('"""')
