dist = ["Kuchchh", "Banaskantha", "Patan", "Mehsana", "Sabarkantha", 
        "Gandhinagar", "Ahmedabad", "Kheda", "Panchmahal", "Dahod", 
        "Surendranagar", "Rajkot", "Jamnagar", "Porbandar", "Junagadh", 
        "Amreli", "Bhavnagar", "Anand", "Vadodara", "Narmada", 
        "Bharuch", "Surat", "Navsari", "Valsad", "Dangs"]

# Map city string to its number (index 0 to 24)
city_map = {}
for i in range(len(dist)):
    city_map[dist[i]] = i

# Create empty adjacency matrix (25x25)
n = len(dist)
adj_matrix = []
for i in range(n):
    row = []
    for j in range(n):
        row.append(0)
    adj_matrix.append(row)

# The mapped numeric adjacency list 
adj_list = {
    0: [], 
    1: [2, 3, 4], 
    2: [1, 10, 3], 
    3: [2, 1, 4, 5, 6, 10], 
    4: [1, 3, 5, 7, 8], 
    5: [3, 4, 7, 6],
    6: [10, 3, 5, 7, 17, 16],
    7: [5, 4, 8, 18, 17, 6],
    8: [4, 7, 18, 9], 
    9: [8, 18],
    10: [2, 3, 6, 16, 11], 
    11: [10, 16, 15, 14, 13, 12], 
    12: [11, 13], 
    13: [12, 11, 14], 
    14: [13, 11, 15], 
    15: [14, 11, 16], 
    16: [15, 11, 10, 6], 
    17: [6, 7, 18], 
    18: [17, 7, 8, 9, 19, 20], 
    19: [18, 20, 21], 
    20: [18, 19, 21, 17], 
    21: [20, 19, 22, 24], 
    22: [21, 24, 23], 
    23: [22],
    24: [22, 21]
}

# Fill the matrix using numeric IDs
for u in adj_list:
    for v in adj_list[u]:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1 # undirected graph

# Array to store assigned color for each city index
res = []

# check if assigning color 'c' to city 'node' (index) is safe
def check(node, c):
    # Loop through all 25 cities
    for neighbor in range(n):
        # If they are connected (value is 1 in matrix)
        if adj_matrix[node][neighbor] == 1:
            # If that neighbor already has the color we want to use, fail
            if res[neighbor] == c:
                return False
    return True

# Standard Backtracking (NO Forward Checking)
def run(idx, colors):
    if idx == n:
        return True
    
    for c in colors:
        if check(idx, c):
            res[idx] = c
            if run(idx + 1, colors):
                return True
            # Backtrack
            res[idx] = -1 
    return False

# main loop to find min colors
for i in [1, 2, 3, 4]:
    cols = []
    if i == 1: cols = ["Red"]
    elif i == 2: cols = ["Red", "Blue"]
    elif i == 3: cols = ["Red", "Blue", "Green"]
    else: cols = ["Red", "Blue", "Green", "Yellow"]
    
    # Initialize array with -1 meaning "uncolored"
    res = []
    for _ in range(n):
        res.append(-1)
        
    if run(0, cols):
        print("Minimum colors used:", i)
        print("No. District \t Color")
        for k in range(n):
            print(str(k) + "   " + dist[k], "\t", res[k])
        break
