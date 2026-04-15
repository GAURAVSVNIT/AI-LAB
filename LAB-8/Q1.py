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
# 1. Use the local beam search to solve the problem. Give a comparative analysis of the algorithm
# when the beam width k=3,5,10. Does the convergence depend on the value of k?

import random

# Graph distance matrix
# A B C D E F G H
d = [
    [0, 10, 15, 20, 25, 30, 35, 40], # city 0 - A
    [12, 0, 35, 15, 20, 25, 30, 45], # city 1 - B
    [25, 30, 0, 10, 40, 20, 15, 35], # city 2 - C
    [18, 25, 12, 0, 15, 30, 20, 10], # city 3 - D
    [22, 18, 28, 20, 0, 15, 25, 30], # city 4 - E
    [35, 22, 18, 28, 12, 0, 40, 20], # city 5 - F
    [30, 35, 22, 18, 28, 32, 0, 15], # city 6 - G
    [40, 28, 35, 22, 18, 25, 12, 0 ] # city 7 - H
]

cities = ["A", "B", "C", "D", "E", "F", "G", "H"]

def get_total_cost(p):
    val = 0
    for i in range(len(p) - 1):
        c1 = p[i]
        c2 = p[i+1]
        val = val + d[c1][c2]
    # cycle back
    v2 = val + d[p[-1]][p[0]]
    return v2

def beam_search(k):
    # random starting points
    pop = []
    base = [0,1,2,3,4,5,6,7]
    for _ in range(k):
        tmp = base[:]
        random.shuffle(tmp)
        pop.append(tmp)
        
    iterations = 0
    # run for 100 times
    while iterations < 100:
        neighbors = []
        for state in pop:
            # 2-opt swap logic
            for i in range(8):
                for j in range(i+1, 8):
                    nn = state[:]
                    # swap
                    temp_v = nn[i]
                    nn[i] = nn[j]
                    nn[j] = temp_v
                    neighbors.append(nn)
        
        # calculate costs
        res = []
        for n in neighbors:
            c = get_total_cost(n)
            res.append((c, n))
            
        # sort to find best k
        res.sort()
        
        # new population
        new_pop = []
        for idx in range(k):
            new_pop.append(res[idx][1])
            
        pop = new_pop
        iterations = iterations + 1
        
    return res[0][0], pop[0]

# Driver code
widths = [3, 5, 10]

for beam_w in widths:
    print("Beam Width k =", beam_w)
    best_c, best_p = beam_search(beam_w)
    
    names = []
    for node in best_p:
        names.append(cities[node])
    
    print("Path Found:", " -> ".join(names), "->", names[0])
    print("Total Cost:", best_c)
    print("--------------------")
