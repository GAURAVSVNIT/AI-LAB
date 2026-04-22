# Adjacency Dictionary (Graph represented with Strings directly)
adj = {
    "Priya":          ["Raj", "Aarav", "Akash", "Neha (Center)"],
    "Raj":            ["Sunil", "Akash"],
    "Aarav":          ["Neha (Right)"],
    "Akash":          [],
    "Neha (Center)":  ["Rahul", "Sneha"],
    "Sunil":          ["Sneha"],
    "Neha (Right)":   ["Arjun (Right)"],
    "Rahul":          ["Maya", "Pooja", "Arjun (Bottom)", "Arjun (Right)"],
    "Sneha":          ["Neha (Center)", "Rahul"],
    "Arjun (Right)":  ["Neha (Right)"],
    "Maya":           ["Arjun (Bottom)"],
    "Pooja":          [],
    "Arjun (Bottom)": ["Pooja"]
}

import sys
import os

# Add parent directory to sys.path to import my_deque
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_deque import MyDeque

def print_tree(u, prefix, is_last, tree_adj):
    """Recursive function to print the tree in ASCII format."""
    print(prefix, end="")
    
    if is_last:
        print("└── " + u)
        prefix += "    "
    else:
        print("├── " + u)
        prefix += "│   "

    # Get children for the current node 'u' from the tree structure
    children = tree_adj.get(u, [])
    
    for i in range(len(children)):
        # Check if this child is the last one in the list
        print_tree(children[i], prefix, i == len(children) - 1, tree_adj)

def bfs(start):
    print("### 1. BFS Tree (Breadth-First Search)")
    vis = set() # Using a set for visited nodes (O(1) lookup)
    tree_adj = {} # Dictionary to store the BFS tree structure
    
    # Using MyDeque as a queue
    q = MyDeque([start])
    vis.add(start)
    
    print(start) # Print root manually

    while len(q) > 0:
        u = q.popleft() # Pop from front
        
        # Ensure the node exists in graph before accessing neighbors
        neighbors = adj.get(u, [])
        
        for v in neighbors:
            if v not in vis:
                vis.add(v)
                
                # Add edge to BFS tree structure
                if u not in tree_adj:
                    tree_adj[u] = []
                tree_adj[u].append(v)
                
                q.append(v)
    
    # Print the tree starting from root's children
    if start in tree_adj:
        children = tree_adj[start]
        for i in range(len(children)):
            print_tree(children[i], "", i == len(children) - 1, tree_adj)
    print()

def dfs_helper(u, vis, tree_adj):
    vis.add(u)
    
    neighbors = adj.get(u, [])
    
    for v in neighbors:
        if v not in vis:
            # Add edge to DFS tree structure
            if u not in tree_adj:
                tree_adj[u] = []
            tree_adj[u].append(v)
            
            dfs_helper(v, vis, tree_adj)

def dfs(start):
    print("### 2. DFS Tree (Depth-First Search)")
    vis = set()
    tree_adj = {}
    
    print(start) # Print root
    dfs_helper(start, vis, tree_adj)

    # Print the tree
    if start in tree_adj:
        children = tree_adj[start]
        for i in range(len(children)):
            print_tree(children[i], "", i == len(children) - 1, tree_adj)

# Driver Code
if __name__ == "__main__":
    bfs("Priya")
    dfs("Priya")