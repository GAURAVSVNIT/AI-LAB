
import time

def get_neighbors(state):
    """
    Returns a list of neighbors for the current state.
    state: A tuple representing the 3x3 grid (flattened).
    """
    state_list = list(state)
    neighbors = []
    # Find the index of the empty tile (0)
    zero_idx = state_list.index(0)
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
            new_state = list(state_list)
            new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
            
            neighbors.append(tuple(new_state))
            
    return neighbors


import sys
import os

# Add parent directory to sys.path to import my_deque
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_deque import MyDeque

def bfs(start_state, goal_state):
    """
    BFS algorithm to find the goal state.
    Returns: (explored_count, path_cost)
    """
    # Using MyDeque as a queue (FIFO)
    queue = MyDeque([(start_state, 0)]) # Stores (state, depth)
    visited = set()
    visited.add(start_state)
    
    explored_count = 0
    
    while len(queue) > 0:
        current_state, depth = queue.popleft()
        explored_count += 1
        
        if current_state == goal_state:
            return explored_count, depth
        
        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                # Store depth + 1
                queue.append((neighbor, depth + 1))
                
    return explored_count, -1 # Not reachable

def dfs(start_state, goal_state):
    """
    DFS algorithm to find the goal state.
    Returns: (explored_count, path_cost)
    """
    # Using a list as a stack (LIFO)
    stack = [(start_state, 0)] # Stores (state, depth)
    visited = set()
    visited.add(start_state)
    
    explored_count = 0
    
    while len(stack) > 0:
        current_state, depth = stack.pop()
        explored_count += 1
        
        if current_state == goal_state:
            return explored_count, depth
        
        # Get neighbors
        # Note: In DFS, the order we push determines the order we process.
        # If we want to process in same order as BFS generation (Up, Down, Left, Right),
        # we should push them in Reverse order (Right, Left, Down, Up).
        # But standard DFS doesn't strictly require this. 
        # We'll just push all unvisited neighbors.
        
        neighbors = get_neighbors(current_state)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, depth + 1))
                
    return explored_count, -1 # Not reachable

if __name__ == "__main__":
    # Start State from Q1
    # 7 2 4
    # 5 0 6
    # 8 3 1
    start_state = (
        7, 2, 4,
        5, 0, 6,
        8, 3, 1
    )

    # Goal State from Q1
    # 0 1 2
    # 3 4 5
    # 6 7 8
    goal_state = (
        0, 1, 2,
        3, 4, 5,
        6, 7, 8
    )

    print(f"Start State: {start_state}")
    print(f"Goal State:  {goal_state}")
    print("-" * 50)

    # Run BFS
    print("Running BFS...")
    start_time = time.time()
    bfs_explored, bfs_cost = bfs(start_state, goal_state)
    bfs_time = time.time() - start_time
    
    print(f"BFS Completed.")
    print("-" * 50)

    # Run DFS
    print("Running DFS...")
    start_time = time.time()
    dfs_explored, dfs_cost = dfs(start_state, goal_state)
    dfs_time = time.time() - start_time
    
    print(f"DFS Completed.")
    print("-" * 50)

    # Comparison Output
    print(f"{'Algorithm':<10} | {'States Explored':<20} | {'Path Cost (Depth)':<20} | {'Time (s)':<10}")
    print("-" * 70)
    print(f"{'BFS':<10} | {bfs_explored:<20} | {bfs_cost:<20} | {bfs_time:<10.4f}")
    print(f"{'DFS':<10} | {dfs_explored:<20} | {dfs_cost:<20} | {dfs_time:<10.4f}")
    print("-" * 70)
