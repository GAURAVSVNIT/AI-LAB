import sys
import collections

# Graph Definitions
# Room Layout:
# Room 1 | Room 2
# Room 3 | Room 4
#
# Adjacency:
# 1: (0,0) -> R:2, D:3
# 2: (0,1) -> L:1, D:4
# 3: (1,0) -> U:1, R:4
# 4: (1,1) -> U:2, L:3

ADJACENCY = {
    1: {'R': 2, 'D': 3},
    2: {'L': 1, 'D': 4},
    3: {'U': 1, 'R': 4},
    4: {'U': 2, 'L': 3}
}

# All possible actions
ACTIONS = ['S', 'N', 'L', 'R', 'U', 'D']

class Node:
    def __init__(self, room, dirt_status, parent=None, action=None):
        self.room = room
        self.dirt_status = tuple(dirt_status) # Tuple for distinct state tracking
        self.parent = parent
        self.action = action

    def get_state(self):
        return (self.room, self.dirt_status)

    def is_goal(self):
        return all(d == 0 for d in self.dirt_status)

    def __repr__(self):
        return f"Node(room={self.room}, dirt={self.dirt_status}, action={self.action})"

def read_input(filepath):
    try:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if len(lines) < 3:
            raise ValueError("Input file must have at least 3 lines")

        # Line 1: Room Number
        start_room = int(lines[0])
        
        # Line 2: Dirt Status (1,0,0,1)
        dirt_parts = lines[1].split(',')
        dirt_status = tuple(int(x.strip()) for x in dirt_parts)
        
        # Line 3: Algorithm
        algorithm = lines[2].lower()
        
        return start_room, dirt_status, algorithm
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

def get_neighbors(node):
    neighbors = []
    
    # Try all actions
    for action in ACTIONS:
        next_room = node.room
        next_dirt = list(node.dirt_status)
        
        is_valid_move = False
        
        if action == 'S':
            # Suck dirt
            # Indices are 0-based, rooms are 1-based
            current_dirt_idx = node.room - 1
            if next_dirt[current_dirt_idx] == 1:
                next_dirt[current_dirt_idx] = 0
                is_valid_move = True
            else:
                # Sucking in a clean room is a valid action but changes nothing?
                # Usually in vacuum world, 'Suck' is always valid. 
                # If clean, state remains same (dirt doesn't change).
                # To prevent useless loops in DFS/BFS without explicit cost, 
                # we usually treat it as valid. Visited set will handle redundancy.
                is_valid_move = True
                
        elif action == 'N':
            # No Op
            is_valid_move = True
            
        else:
            # Move L, R, U, D
            if action in ADJACENCY[node.room]:
                next_room = ADJACENCY[node.room][action]
                is_valid_move = True
        
        if is_valid_move:
            child = Node(next_room, next_dirt, node, action)
            neighbors.append(child)
            
    return neighbors


import sys
import os
# Add parent directory to sys.path to import my_deque
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from my_deque import MyDeque

# ... existing imports ...

def solve():
    if len(sys.argv) < 3:
        print("Usage: python TA_4_5_P1_vacuum_world.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    start_room, start_dirt, algo = read_input(input_file)
    
    start_node = Node(start_room, start_dirt)
    
    # Frontier management
    # MyDeque can act as stack (append/pop) or queue (append/popleft)
    frontier = MyDeque([start_node])
    explored = set()
    
    goal_node = None
    
    while frontier:
        if algo == 'bfs':
            current_node = frontier.popleft()
        elif algo == 'dfs':
            current_node = frontier.pop()
        else:
            print(f"Unknown algorithm: {algo}")
            sys.exit(1)
            
        if current_node.get_state() in explored:
            continue
        
        explored.add(current_node.get_state())
        
        # Check Goal
        if current_node.is_goal():
            goal_node = current_node
            break
        
        # Expand
        neighbors = get_neighbors(current_node)
        for child in neighbors:
            if child.get_state() not in explored:
                # Add to frontier
                frontier.append(child)
    
    # Reconstruct path
    output_lines = []
    if goal_node:
        curr = goal_node
        path = []
        while curr.parent is not None:
            # The action taken to reach 'curr' from 'parent'
            # Format: <current_room_before_action>,<action>
            path.append((curr.parent.room, curr.action))
            curr = curr.parent
        
        # Path is in reverse order (goal -> start)
        path.reverse()
        
        for room, action in path:
            output_lines.append(f"{room},{action}")
    else:
        output_lines.append("No solution found.")

    # Write output
    try:
        with open(output_file, 'w') as f:
            f.write("\n".join(output_lines))
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    solve()
