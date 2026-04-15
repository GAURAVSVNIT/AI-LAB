# City mapping
cities = {
    0: "Chicago",
    1: "Detroit",
    2: "Cleveland",
    3: "Indianapolis",
    4: "Columbus",
    5: "Pittsburgh",
    6: "Buffalo",
    7: "Syracuse",
    8: "New York",
    9: "Philadelphia",
    10: "Baltimore",
    11: "Boston",
    12: "Providence",
    13: "Portland"
}

n = 14

# adjacency matrix
adj = [[0 for _ in range(n)] for _ in range(n)]

edges = [
    (0,1,283),(0,2,354),(0,3,182), # Chicago: Det 283, Cle 354 (corrected from 345 in snippet to match prompt data), Ind 182
    (1,2,169),(1,6,256),           # Detroit: Cle 169, Buf 256
    (2,6,189),(2,5,134),(2,4,144), # Cleveland: Buf 189, Pit 134, Col 144
    (3,4,176),                     # Indy: Col 176
    (4,5,185),                     # Col: Pit 185
    (5,6,215),(5,9,305),(5,10,247),# Pit: Buf 215, Phi 305, Bal 247
    (6,7,150),                     # Buf: Syr 150
    (7,8,254),(7,11,312),          # Syr: NY 254, Bos 312
    (8,9,97),(8,12,181),(8,11,215),# NY: Phi 97, Pro 181, Bos 215 (Added Bos connection)
    (9,10,101),                    # Phi: Bal 101 (Removed NY double)
    (11,12,50),(11,13,107),        # Bos: Pro 50, Por 107
    (12,8,181)                     # Pro: NY 181 (Already covered)
]

edges_clean = [
    (0,1,283), (0,2,354), (0,3,182),     # Chi: Det 283, Cle 354, Ind 182
    (1,6,256), (1,2,169),                # Det: Buf 256, Cle 169
    (2,6,189), (2,5,134), (2,4,144),     # Cle: Buf 189, Pit 134, Col 144 (Chi 345 mismatch? Q1.py says Cle-Chi 345, Chi-Cle 354? Asymmetric? Map is usually symmetric. I'll use 354 as in snippet or check LAB-1 dict 354)
    (3,4,176),                           # Ind: Col 176
    (4,5,185),                           # Col: Pit 185
    (5,6,215), (5,9,305), (5,10,247),    # Pit: Buf 215, Phi 305, Bal 247
    (6,7,150),                           # Buf: Syr 150
    (7,8,254), (7,11,312),               # Syr: NY 254, Bos 312
    (8,9,97), (8,12,181), (8,11,215),    # NY: Phi 97, Pro 181, Bos 215
    (9,10,101),                          # Phi: Bal 101
    (11,12,50), (11,13,107)              # Bos: Pro 50, Por 107
]

# Clear adj
adj = [[0 for _ in range(n)] for _ in range(n)]

for u, v, w in edges_clean:
    adj[u][v] = w
    adj[v][u] = w

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state # Current City Index
        self.parent = parent # Parent Node
        self.action = action  # Next City Index
        self.path_cost = path_cost  # Total Distance from start node to current node

class PriorityQueue:
    def __init__(self, f):
        self.data = []
        self.f = f

    def add(self, node):
        self.data.append(node)
        self.data.sort(key=self.f) # Sort by f(node) = path_cost

    def pop(self):
        return self.data.pop(0)

    def top(self):
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

class Problem:
    def __init__(self, initial, goal):
        self.INITIAL = initial # Start City Index
        self.goal = goal # Goal City Index

    def is_goal(self, state):
        return state == self.goal

    def ACTIONS(self, state):
        actions = []
        for i in range(n):
            if adj[state][i] != 0:
                actions.append(i)
        return actions  # List of next city indices

    def RESULT(self, state, action):
        return action # In this graph, action is the next state index

    def ACTION_COST(self, s, action, s_prime):
        return adj[s][s_prime]

def EXPAND(problem, node):
    s = node.state
    for action in problem.ACTIONS(s):
        s_prime = problem.RESULT(s, action)
        cost = node.path_cost + problem.ACTION_COST(s, action, s_prime)
        yield Node(state=s_prime, parent=node, action=action, path_cost=cost)

def BEST_FIRST_SEARCH(problem, f):
    node = Node(problem.INITIAL) # Start Node
    
    frontier = PriorityQueue(f)
    frontier.add(node)
    
    # reach dict stores state -> node
    reached = [None] * n
    reached[problem.INITIAL] = node
    explored = 0
    
    while not frontier.is_empty():
        node = frontier.pop()
        explored += 1
        
        if problem.is_goal(node.state):
            return node, explored, reached
        
        for child in EXPAND(problem, node):
            s = child.state
            if reached[s] is None or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
                
    return None, explored, reached

# Path Cost (UCS)
# Using path cost as per the snippet's logic f(node) => node.path_cost (Uniform Cost Search)
def f(node):
    return node.path_cost

def get_path(node):
    path = []
    while node:
        path.append(cities[node.state])
        node = node.parent
    return path[::-1]

if __name__ == "__main__":
    # Driver code
    start = 7   # Syracuse
    goal = 0    # Chicago
    
    problem = Problem(start, goal)
    solution, explored_count, reached_table = BEST_FIRST_SEARCH(problem, f)
    
    if solution:
        print("Uniform Cost Search Path:")
        print(" -> ".join(get_path(solution)))
        print("Total cost:", solution.path_cost)
        print("Number of paths explored:", explored_count)
        
        print("\nLookup Table (Reached States):")
        print(f"{'City Index':<12} | {'City Name':<15} | {'Cost':<6} | {'Parent'}")
        print("-" * 55)
        for i in range(len(reached_table)):
            node = reached_table[i]
            city_name = cities[i]
            if node:
                parent_name = cities[node.parent.state] if node.parent else "None"
                print(f"{i:<12} | {city_name:<15} | {node.path_cost:<6} | {parent_name}")
            else:
                print(f"{i:<12} | {city_name:<15} | {'None':<6} | -")
    else:
        print("No path found.")
