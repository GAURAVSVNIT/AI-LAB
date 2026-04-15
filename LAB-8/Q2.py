# Use the following graph for the Traveling Salesperson problem. Find the least cost path in the
# graph for the TSP problem.
# A B C D E F G H
# A [0, 10, 15, 20, 25, 30, 35, 40], # City 0
# B [12, 0, 35, 15, 20, 25, 30, 45], # City 1
# C [25, 30, 0, 10, 40, 20, 15, 35], # City 2
# D [18, 25, 12, 0, 15, 30, 20, 10], # City 3
# E [22, 18, 28, 20, 0, 15, 25, 30], # City 4
# F [35, 22, 18, 28, 12, 0, 40, 20], # City 5
# G [30, 35, 22, 18, 28, 32, 0, 15], # City 6
# H [40, 28, 35, 22, 18, 25, 12, 0 ] # City 7
# 2. Use the genetic algorithm to solve the problem. Use one crossover point and two crossover
# points to generate the offspring. Does the number of crossover points impact the convergence
# rate?

import random

# Matrix (hardcoded as requested)
# A B C D E F G H
d = [
    [0, 10, 15, 20, 25, 30, 35, 40], # A
    [12, 0, 35, 15, 20, 25, 30, 45], # B
    [25, 30, 0, 10, 40, 20, 15, 35], # C
    [18, 25, 12, 0, 15, 30, 20, 10], # D
    [22, 18, 28, 20, 0, 15, 25, 30], # E
    [35, 22, 18, 28, 12, 0, 40, 20], # F
    [30, 35, 22, 18, 28, 32, 0, 15], # G
    [40, 28, 35, 22, 18, 25, 12, 0 ] # H
]

cities = ["A", "B", "C", "D", "E", "F", "G", "H"]

def get_cost(p):
    val = 0
    for i in range(len(p) - 1):
        c1 = p[i]
        c2 = p[i+1]
        val = val + d[c1][c2]
    val = val + d[p[-1]][p[0]]
    return val

def to_ord(p):
    L = [0, 1, 2, 3, 4, 5, 6, 7]
    res = []
    for x in p:
        temp = L.index(x)
        res.append(temp)
        L.remove(x)
    return res

def from_ord(o):
    L = [0, 1, 2, 3, 4, 5, 6, 7]
    res = []
    for x in o:
        val = L[x]
        res.append(val)
        L.remove(val)
    return res

def one_pt_cross(p1, p2):
    o1 = to_ord(p1)
    o2 = to_ord(p2)
    pt = random.randint(1, 6)
    child = []
    for i in range(8):
        if i < pt:
            child.append(o1[i])
        else:
            child.append(o2[i])
    return from_ord(child)

def two_pt_cross(p1, p2):
    o1 = to_ord(p1)
    o2 = to_ord(p2)
    pt1 = random.randint(0, 5)
    pt2 = random.randint(pt1 + 1, 7)
    child = []
    for i in range(8):
        if i >= pt1 and i <= pt2:
            child.append(o1[i])
        else:
            child.append(o2[i])
    return from_ord(child)

def mutate(p):
    # swap two random cities
    i, j = random.sample(range(8), 2)
    p[i], p[j] = p[j], p[i]
    return p

def solve(mode):
    # Genetic Algo Params
    pop_size = 50
    generations = 100
    
    # Initial population
    pop = []
    base = [0,1,2,3,4,5,6,7]
    for _ in range(pop_size):
        tmp = base[:]
        random.shuffle(tmp)
        pop.append(tmp)
        
    best_ever = 9999
    gen_found = 0
    
    # Evolution loop
    for gen in range(generations):
        # find costs
        costs = []
        for p in pop:
            c = get_cost(p)
            costs.append((c, p))
        
        costs.sort() # elitism: keep best ones
        
        if costs[0][0] < best_ever:
            best_ever = costs[0][0]
            gen_found = gen
            
        new_pop = []
        # Keep top 2 (elites)
        new_pop.append(costs[0][1])
        new_pop.append(costs[1][1])
        
        while len(new_pop) < pop_size:
            # tournament selection
            t1 = random.sample(pop, 3)
            # find best in t1
            b1 = sorted([(get_cost(x), x) for x in t1])[0][1]
            
            t2 = random.sample(pop, 3)
            b2 = sorted([(get_cost(x), x) for x in t2])[0][1]
            
            # Crossover
            if mode == 1:
                child = one_pt_cross(b1, b2)
            else:
                child = two_pt_cross(b1, b2)
                
            # Mutation (small chance)
            if random.random() < 0.2:
                child = mutate(child)
                
            new_pop.append(child)
            
        pop = new_pop
        
    return best_ever, gen_found

# Main execution
print("Crossover Point Comparison")
print("-" * 25)

# Run 5 trials each to see average convergence
for m in [1, 2]:
    header = "Single-Point" if m == 1 else "Two-Point"
    print(header + " Crossover:")
    
    avg_gen = 0
    avg_cost = 0
    trials = 5
    for i in range(trials):
        c, g = solve(m)
        avg_cost += c
        avg_gen += g
        print(f"Trial {i+1}: Best Cost = {c}, Found at Gen = {g}")
        
    print(f"AVERAGE Cost: {avg_cost/trials}")
    print(f"AVERAGE Generation: {avg_gen/trials}")
    print("-" * 25)