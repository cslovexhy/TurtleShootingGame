import random
from copy import deepcopy

class MazeGenerator:
    def __init__(self, width, height, wall_char='s', empty_char='.'):
        self.width = width
        self.height = height
        self.wall_char = wall_char
        self.empty_char = empty_char
        self.maze = []
        
    def generate_recursive_backtracking(self):
        """Generate maze using recursive backtracking algorithm with 3-wide paths"""
        # Initialize maze filled with walls
        self.maze = [[self.wall_char for _ in range(self.width)] for _ in range(self.height)]
        
        # Start from position (2,2) to ensure border walls and room for 3-wide paths
        start_x, start_y = 2, 2
        self._carve_3wide_space(start_x, start_y)
        
        # Stack for backtracking
        stack = [(start_x, start_y)]
        
        while stack:
            current_x, current_y = stack[-1]
            
            # Get unvisited neighbors (4 cells away to maintain 3-wide paths + walls)
            neighbors = []
            directions = [(0, -4), (4, 0), (0, 4), (-4, 0)]  # up, right, down, left
            
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if (2 <= nx < self.width - 2 and 2 <= ny < self.height - 2 and 
                    self.maze[ny][nx] == self.wall_char):
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                # Choose random neighbor
                nx, ny, dx, dy = random.choice(neighbors)
                
                # Carve 3-wide path to neighbor
                self._carve_3wide_space(nx, ny)
                self._carve_3wide_corridor(current_x, current_y, nx, ny)
                
                stack.append((nx, ny))
            else:
                # Backtrack
                stack.pop()
        
        return self.maze
    
    def _carve_3wide_space(self, center_x, center_y):
        """Carve a 3x3 empty space centered at given position"""
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                x, y = center_x + dx, center_y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.maze[y][x] = self.empty_char
    
    def _carve_3wide_corridor(self, x1, y1, x2, y2):
        """Carve a 3-wide corridor between two points"""
        # Determine direction
        if x1 == x2:  # vertical corridor
            start_y, end_y = min(y1, y2), max(y1, y2)
            for y in range(start_y, end_y + 1):
                for dx in range(-1, 2):
                    x = x1 + dx
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.maze[y][x] = self.empty_char
        else:  # horizontal corridor
            start_x, end_x = min(x1, x2), max(x1, x2)
            for x in range(start_x, end_x + 1):
                for dy in range(-1, 2):
                    y = y1 + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.maze[y][x] = self.empty_char
    
    def add_openings(self, opening_density=0.05):
        """Add random openings to make maze less dense"""
        for y in range(3, self.height - 3):
            for x in range(3, self.width - 3):
                if self.maze[y][x] == self.wall_char and random.random() < opening_density:
                    # Create 3-wide opening
                    self._carve_3wide_space(x, y)
    
    def place_entities(self, entities):
        """Place entities (player, enemies, items) in empty spaces"""
        empty_spaces = []
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                if self.maze[y][x] == self.empty_char:
                    # Only use center positions of 3-wide areas for cleaner placement
                    if (x % 2 == 0 and y % 2 == 0):
                        empty_spaces.append((x, y))
        
        # Shuffle to get random placement
        random.shuffle(empty_spaces)
        
        placed = 0
        for entity_char, count in entities.items():
            for _ in range(count):
                if placed < len(empty_spaces):
                    x, y = empty_spaces[placed]
                    self.maze[y][x] = entity_char
                    placed += 1
    
    def to_level_string(self):
        """Convert maze to level string format"""
        lines = []
        for row in self.maze:
            lines.append(' '.join(row))
        return '\n'.join(lines)
