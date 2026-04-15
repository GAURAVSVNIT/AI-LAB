
# Q1: Greedy Best First Search & A* Search

# Heuristic values (h) to Boston
# Chicago 860, Detroit 610, Cleveland 550, Indianapolis 780, Columbus 640
# Pittsburgh 470, Buffalo 400, Syracuse 260, New York 215, Philadelphia 270
# Baltimore 360, Boston 0, Providence 50, Portland 107

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

h = {
    0: 860, 1: 610, 2: 550, 3: 780, 4: 640,
    5: 470, 6: 400, 7: 260, 8: 215, 9: 270,
    10: 360, 11: 0, 12: 50, 13: 107
}

n = 14
adj = [[0 for _ in range(n)] for _ in range(n)]

edges = [
    (0,1,283), (0,2,354), (0,3,182),
    (1,6,256), (1,2,169),
    (2,6,189), (2,5,134), (2,4,144),
    (3,4,176),
    (4,5,185),
    (5,6,215), (5,9,305), (5,10,247),
    (6,7,150),
    (7,8,254), (7,11,312),
    (8,9,97), (8,12,181), (8,11,215),
    (9,10,101),
    (11,12,50), (11,13,107)
]

for u, v, w in edges:
    adj[u][v] = w
    adj[v][u] = w

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, heuristic_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost

class PriorityQueue:
    def __init__(self, f):
        self.data = []
        self.f = f

    def add(self, node):
        self.data.append(node)
        self.data.sort(key=self.f)

    def pop(self):
        return self.data.pop(0)

    def is_empty(self):
        return len(self.data) == 0

class Problem:
    def __init__(self, initial, goal):
        self.INITIAL = initial
        self.goal = goal

    def is_goal(self, state):
        return state == self.goal

    def ACTIONS(self, state):
        actions = []
        for i in range(n):
            if adj[state][i] != 0:
                actions.append(i)
        return actions

    def ACTION_COST(self, s, s_prime):
        return adj[s][s_prime]

def EXPAND(problem, node):
    s = node.state
    for action in problem.ACTIONS(s):
        s_prime = action
        cost = node.path_cost + problem.ACTION_COST(s, s_prime)
        yield Node(state=s_prime, parent=node, action=action, path_cost=cost, heuristic_cost=h[s_prime])

def SEARCH(problem, f):
    node = Node(problem.INITIAL, heuristic_cost=h[problem.INITIAL])
    frontier = PriorityQueue(f)
    frontier.add(node)
    
    reached = {} # Using a simple dict for reached
    reached[problem.INITIAL] = node
    
    explored = 0
    
    while not frontier.is_empty():
        node = frontier.pop()
        explored += 1
        
        if problem.is_goal(node.state):
            return node, explored
        
        for child in EXPAND(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
                
    return None, explored

def get_path(node):
    path = []
    cost = node.path_cost
    while node:
        path.append(cities[node.state])
        node = node.parent
    return path[::-1], cost

# GBFS: f(n) = h(n)
def f_gbfs(node):
    return node.heuristic_cost

# A*: f(n) = g(n) + h(n)
def f_astar(node):
    return node.path_cost + node.heuristic_cost

if __name__ == "__main__":
    start = 0   # Chicago
    goal = 11   # Boston
    
    problem = Problem(start, goal)
    
    print("--- Greedy Best First Search ---")
    sol_gbfs, exp_gbfs = SEARCH(problem, f_gbfs)
    if sol_gbfs:
        p, c = get_path(sol_gbfs)
        print("Path:", " -> ".join(p))
        print("Cost:", c)
        print("Explored:", exp_gbfs)
    else:
        print("No path found")

    print("\n--- A* Search ---")
    sol_astar, exp_astar = SEARCH(problem, f_astar)
    if sol_astar:
        p, c = get_path(sol_astar)
        print("Path:", " -> ".join(p))
        print("Cost:", c)
        print("Explored:", exp_astar)
    else:
        print("No path found")
        
    print("\n--- Comparison ---")
    print("Algo\tPath Cost\tExplored")
    if sol_gbfs: print(f"GBFS\t{sol_gbfs.path_cost}\t\t{exp_gbfs}")
    if sol_astar: print(f"A*\t{sol_astar.path_cost}\t\t{exp_astar}")

