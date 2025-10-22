import heapq
import math

def get_dist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def find_path_improved(start, goal, blocks):
    """Improved A* pathfinding implementation"""
    if start == goal:
        return True, [start]
    
    # Priority queue: (f_score, g_score, position, parent)
    open_set = [(get_dist(start, goal), 0, start, None)]
    
    # Track best g_score for each position
    g_scores = {start: 0}
    
    # Track processed nodes
    closed_set = set()
    
    # Track parents for path reconstruction
    parents = {}
    
    # Track closest node to goal (fallback)
    closest = (start, get_dist(start, goal))
    
    while open_set:
        f_score, g_score, current, parent = heapq.heappop(open_set)
        
        # Skip if already processed
        if current in closed_set:
            continue
            
        # Mark as processed
        closed_set.add(current)
        parents[current] = parent
        
        # Check if reached goal
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parents[current]
            return True, path[::-1]
        
        # Update closest node
        dist_to_goal = get_dist(current, goal)
        if dist_to_goal < closest[1]:
            closest = (current, dist_to_goal)
        
        # Explore neighbors
        x, y = current
        for dx in (-20, 0, 20):
            for dy in (-20, 0, 20):
                if dx == 0 and dy == 0:  # Skip current position
                    continue
                    
                neighbor = (x + dx, y + dy)
                
                # Skip if blocked or already processed
                if neighbor in blocks or neighbor in closed_set:
                    continue
                
                # Skip diagonal moves blocked by adjacent walls
                if dx != 0 and dy != 0:
                    if (x + dx, y) in blocks or (x, y + dy) in blocks:
                        continue
                
                # Calculate tentative g_score
                tentative_g = g_score + get_dist(current, neighbor)
                
                # Skip if we've found a better path to this neighbor
                if neighbor in g_scores and tentative_g >= g_scores[neighbor]:
                    continue
                
                # Record best path to neighbor
                g_scores[neighbor] = tentative_g
                h_score = get_dist(neighbor, goal)
                f_score = tentative_g + h_score
                
                heapq.heappush(open_set, (f_score, tentative_g, neighbor, current))
    
    # Goal not reachable, return path to closest point
    path = []
    current = closest[0]
    while current is not None:
        path.append(current)
        current = parents.get(current)
    return False, path[::-1]
