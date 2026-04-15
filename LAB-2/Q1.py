
# 8-Puzzle Problem using BFS

def get_neighbors(state):
    """
    Returns a list of neighbors for the current state.
    state: A list representing the 3x3 grid (flattened).
    """
    neighbors = []
    # Find the index of the empty tile (0)
    zero_idx = state.index(0)
    row, col = divmod(zero_idx, 3)

    # Possible moves: Up, Down, Left, Right
    # (row_change, col_change)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc

        # Check boundaries
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            
            # Create a new state by swapping
            new_state = list(state)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            
            
            neighbors.append(tuple(new_state))
            
    return neighbors

def get_neighbors_2d(state_2d):
    """
    Returns neighbors using a 2D list structure.
    state_2d: A tuple of tuples ((1, 2, 3), (4, 0, 5), (6, 7, 8))
    """
    # Convert tuple of tuples to list of lists for mutability
    grid = [list(row) for row in state_2d]
    neighbors = []
    
    # 1. Find zero (0)
    zero_row, zero_col = -1, -1
    for r in range(3):
        for c in range(3):
            if grid[r][c] == 0:
                zero_row, zero_col = r, c
                break
    
    # 2. Define Moves
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # U, D, L, R
    
    for dr, dc in moves:
        new_row, new_col = zero_row + dr, zero_col + dc
        
        # 3. Check Boundaries
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            
            # 4. Create new state (Deep Copy manually)
            new_grid = [row[:] for row in grid]
            
            # 5. Swap
            new_grid[zero_row][zero_col], new_grid[new_row][new_col] = \
                new_grid[new_row][new_col], new_grid[zero_row][zero_col]
            
            # 6. Convert back to tuple of tuples for hashing
            new_state = tuple(tuple(row) for row in new_grid)
            neighbors.append(new_state)
            
    return neighbors


import sys
import os

# Add parent directory to sys.path to import my_deque
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_deque import MyDeque

def bfs(start_state, goal_state):
    """
    BFS algorithm to find the goal state and count explored nodes.
    """
    # Using MyDeque as a queue (FIFO)
    # Storing (state, path_to_state)
    queue = MyDeque([(tuple(start_state), [])])
    
    # Using a set for visited states for O(1) lookup
    visited = set()
    visited.add(tuple(start_state))
    
    explored_count = 0
    
    print("BFS Search Started...")
    
    while len(queue) > 0:
        current_state, path = queue.popleft()
        explored_count += 1
        
        # Check if goal is reached
        if current_state == tuple(goal_state):
            return explored_count, path + [list(current_state)]
        
        # Get neighbors
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [list(current_state)]))
                
    return explored_count, None # Goal not reachable

if __name__ == "__main__":
    # 0 represents the empty tile
    
    # Start State from the image
    # 7 2 4
    # 5 0 6
    # 8 3 1
    start_state = [
        7, 2, 4,
        5, 0, 6,
        8, 3, 1
    ]

    # Goal State from the image
    # 0 1 2
    # 3 4 5
    # 6 7 8
    goal_state = [
        0, 1, 2,
        3, 4, 5,
        6, 7, 8
    ]

    print(f"Start State: {start_state}")
    print(f"Goal State:  {goal_state}")
    print("-" * 30)

    explored_nodes, path = bfs(start_state, goal_state)

    if path:
        print("\nGoal Reached!")
        print(f"Number of states explored: {explored_nodes}")
        print(f"Path Length (Moves): {len(path) - 1}") # -1 because path includes start state
        
        print("\nPath:")
        for i, state in enumerate(path):
            # Format as grid for display
            grid = [state[j:j+3] for j in range(0, 9, 3)]
            print(f"Step {i}: {grid[0]} {grid[1]} {grid[2]}")
    else:
        print("Goal not reachable.")
        print(f"Number of states explored: {explored_nodes}")
