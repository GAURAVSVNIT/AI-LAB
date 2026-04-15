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

# The original adjacency list 
adj_list = {
"Kuchchh": [],
 "Banaskantha": ["Patan", "Mehsana", "Sabarkantha"],
 "Patan": ["Banaskantha", "Surendranagar", "Mehsana"],
 "Mehsana": ["Patan", "Banaskantha", "Sabarkantha", "Gandhinagar",
             "Ahmedabad", "Surendranagar"],
 "Sabarkantha": ["Banaskantha", "Mehsana", "Gandhinagar", "Kheda",
                 "Panchmahal"],
 "Surendranagar": ["Patan", "Mehsana", "Ahmedabad", "Bhavnagar",
                    "Rajkot"],
 "Rajkot": ["Surendranagar", "Bhavnagar", "Amreli", "Junagadh",
                "Porbandar", "Jamnagar"],
 "Jamnagar": ["Rajkot", "Porbandar"],
 "Porbandar": ["Jamnagar", "Rajkot", "Junagadh"],
 "Junagadh": ["Porbandar", "Rajkot", "Amreli"],
 "Amreli": ["Junagadh", "Rajkot", "Bhavnagar"],
 "Bhavnagar": ["Amreli", "Rajkot", "Surendranagar", "Ahmedabad"],
 "Ahmedabad": ["Surendranagar", "Mehsana", "Gandhinagar", "Kheda", "Anand",
"Bhavnagar"],
 "Gandhinagar": ["Mehsana", "Sabarkantha", "Kheda", "Ahmedabad"],
 "Kheda": ["Gandhinagar", "Sabarkantha", "Panchmahal", "Vadodara", "Anand",
           "Ahmedabad"],
 "Anand": ["Ahmedabad", "Kheda", "Vadodara"],
 "Panchmahal": ["Sabarkantha", "Kheda", "Vadodara", "Dahod"],
 "Dahod": ["Panchmahal", "Vadodara"],
 "Vadodara": ["Anand", "Kheda", "Panchmahal", "Dahod", "Narmada", "Bharuch"],
 "Bharuch": ["Vadodara", "Narmada", "Surat", "Anand"],
 "Narmada": ["Vadodara", "Bharuch", "Surat"],
 "Surat": ["Bharuch", "Narmada", "Navsari", "Dangs"],
 "Navsari": ["Surat", "Dangs", "Valsad"],
 "Dangs": ["Navsari", "Surat"],
 "Valsad": ["Navsari"]
}

# Fill the matrix
for city in adj_list:
    u = city_map[city]
    for neighbor in adj_list[city]:
        v = city_map[neighbor]
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
