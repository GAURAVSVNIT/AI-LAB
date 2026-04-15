import sys
import collections

# Graph Representation based on the provided floor plan image
# Nodes: 0, 1, 2, 3, 4, 5 (Outside)
# Connections visible in the diagram:
# 0 -> 4
# 1 -> 2, 3, 5
# 2 -> 1
# 3 -> 1, 4
# 4 -> 0, 3, 5
# 5 -> 1, 4

GRAPH = {
    0: [4],
    1: [2, 3, 5],
    2: [1],
    3: [1, 4],
    4: [0, 3, 5],
    5: [1, 4]
}

GOAL_STATE = 5

def bfs(start_node):
    queue = [(start_node, [start_node])]
    visited = set()
    
    while queue:
        current, path = queue.pop(0)
        
        if current == GOAL_STATE:
            return path
        
        if current in visited:
            continue
        visited.add(current)
        
        for neighbor in GRAPH.get(current, []):
            if neighbor not in visited:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append((neighbor, new_path))
    return None

def dfs(start_node):
    stack = [(start_node, [start_node])]
    visited = set()
    
    while stack:
        current, path = stack.pop()
        
        if current == GOAL_STATE:
            return path
        
        if current in visited:
            continue
        visited.add(current)
        
        # Add neighbors to stack.
        # Note: Order of adding affects traversal order.
        # To match typical DFS behavior (visiting 'first' neighbor first), 
        # we might want to iterate in reverse order or just standard.
        # We'll use standard order.
        for neighbor in GRAPH.get(current, []):
            if neighbor not in visited:
                new_path = list(path)
                new_path.append(neighbor)
                stack.append((neighbor, new_path))
    return None

def solve():
    if len(sys.argv) < 3:
        print("Usage: python TA_4_5_P2_building_path.py <start_node> <algorithm>")
        print("Example: python TA_4_5_P2_building_path.py 2 DFS")
        sys.exit(1)
        
    try:
        start_node = int(sys.argv[1])
        algorithm = sys.argv[2].upper()
    except ValueError:
        print("Error: Start node must be an integer.")
        sys.exit(1)
        
    if start_node not in GRAPH:
        print(f"Error: Start node {start_node} is not valid.")
        sys.exit(1)
        
    path = None
    if algorithm == 'BFS':
        path = bfs(start_node)
    elif algorithm == 'DFS':
        path = dfs(start_node)
    else:
        print(f"Error: Unknown algorithm {algorithm}. Use BFS or DFS.")
        sys.exit(1)
        
    if path:
        print("-".join(map(str, path)))
    else:
        print("No path found.")

if __name__ == "__main__":
    solve()
