
# Q2: A* Search for Maze with Multiple Rewards

# Grid from image analysis
# 0: Empty, 1: Wall, 2: Start, 3: Reward
# A is at (0,0). R at (1,4), (2,1), (4,0), (4,4) based on visual check, but let's stick to the prompt's rules.
# Prompt says "Consider a maze as a 5x5 matrix input...".
# I'll use the matrix derived from the image description I did earlier.
# Row 0: Start(0,0), Wall(0,4)
# Row 1: Wall(1,1), Reward(1,4)
# Row 2: Reward(2,1), Wall(2,3), Wall(2,4)
# Row 3: Wall(3,1), Wall(3,4)
# Row 4: Reward(4,0), Reward(4,4)

grid = [
    [2, 0, 0, 0, 1],
    [0, 1, 0, 0, 3],
    [0, 3, 0, 1, 1],
    [0, 1, 0, 0, 1],
    [3, 0, 0, 0, 3]
]

rows = 5
cols = 5

# Find start and all rewards
start_pos = None
all_rewards = []

for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 2:
            start_pos = (r, c)
        elif grid[r][c] == 3:
            all_rewards.append((r, c))

# Helper to verify standard checking
print(f"Start: {start_pos}")
print(f"Rewards to collect: {all_rewards}")

class Node:
    def __init__(self, r, c, collected, parent=None, action=None, g=0, h=0):
        self.r = r
        self.c = c
        self.collected = collected # Tuple of collected reward coordinates
        self.parent = parent
        self.action = action
        self.g = g # Cost so far
        self.h = h # Heuristic
        self.f = g + h

    # For priority queue comparison
    def __lt__(self, other):
        return self.f < other.f

def get_h(r, c, collected):
    # Heuristic: Max Manhattan distance to any uncollected reward
    # Justification: Admissible because we must travel at least to the farthest reward.
    # Logic: loops through all_rewards, checks if not in collected, finds max dist
    max_d = 0
    uncollected_count = 0
    
    for rw in all_rewards:
        if rw not in collected:
            d = abs(r - rw[0]) + abs(c - rw[1])
            if d > max_d:
                max_d = d
            uncollected_count += 1
            
    # Simple addition: If 0 uncollected, h=0.
    return max_d

def solve():
    # Initial state: Start pos, empty collected tuple
    start_node = Node(start_pos[0], start_pos[1], (), g=0, h=get_h(start_pos[0], start_pos[1], ()))
    
    frontier = [start_node] # List as priority queue
    
    # Visited set to avoid cycles in state space
    # State signature: (r, c, collected_tuple)
    visited = set()
    
    states_explored = 0
    
    while len(frontier) > 0:
        # Sort frontier to simulate priority queue (Bad efficiency, but "messy" compliant)
        frontier.sort() 
        current = frontier.pop(0) # Pop node with lowest f
        
        states_explored += 1
        
        # Check goal: Have we collected all rewards?
        # Note: We can end anywhere after collecting the last reward, or maybe strictly AT the last reward.
        # The problem says "reach all the rewards... If all goals are completed, then one can come out".
        # So typically, the moment we step on the last reward, we are done.
        
        # Update collected set for current node logic check
        # (Already done in child creation, but let's check here for goal)
        if len(current.collected) == len(all_rewards):
            return current, states_explored
            
        r, c = current.r, current.c
        
        state_sig = (r, c, current.collected)
        if state_sig in visited:
            continue
        visited.add(state_sig)
        
        # Actions: U, D, L, R
        moves = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
        
        for dr, dc, act in moves:
            nr, nc = r + dr, c + dc
            
            # Check bounds and walls
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] != 1: # Not a wall
                    # Check new collected status
                    new_collected = list(current.collected)
                    if (nr, nc) in all_rewards and (nr, nc) not in new_collected:
                        new_collected.append((nr, nc))
                        # Sort to make tuple unique for set hashing
                        new_collected.sort()
                    
                    new_collected_tuple = tuple(new_collected)
                    
                    new_g = current.g + 1
                    new_h = get_h(nr, nc, new_collected_tuple)
                    
                    child = Node(nr, nc, new_collected_tuple, current, act, new_g, new_h)
                    
                    # Optimization: Don't add if already visited with lower cost (Skipped here for "messy" simplicity)
                    frontier.append(child)

    return None, states_explored

solution, explored = solve()

if solution:
    print("\n--- Solution Found ---")
    print(f"Total Steps (Cost): {solution.g}")
    print(f"States Explored: {explored}")
    
    # Reconstruct path
    path = []
    curr = solution
    while curr:
        path.append(curr)
        curr = curr.parent
    path = path[::-1]
    
    print("Path taken:")
    for p in path:
        char_at_pos = grid[p.r][p.c]
        desc = "Empty"
        if char_at_pos == 2: desc = "Start"
        if char_at_pos == 3: desc = "Reward"
        
        act = p.action if p.action else "Start"
        print(f"{act} -> ({p.r}, {p.c}) [{desc}] | Collected: {len(p.collected)}/{len(all_rewards)}")
        
    print("\nTiles visited on the way (unique):")
    unique_tiles = set((node.r, node.c) for node in path)
    print(unique_tiles)

else:
    print("No solution found.")

print("\n--- Justification ---")
print("Heuristic used: h(n) = Max Manhattan Distance to any uncollected reward.")
print("Cost function: f(n) = g(n) + h(n), where g(n) is steps taken.")
print("Justification: This is admissible because to visit the set of remaining rewards,")
print("the agent must at least travel to the farthest one from its current position.")
print("It never overestimates the true remaining cost, ensuring optimal A* search.")
