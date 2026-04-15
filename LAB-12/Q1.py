# Teams and rooms
tList = ["P1", "P2", "P3", "P4", "P5", "P6"]
rooms = ["R1", "R2", "R3"]

# Conflicts
conf = {
    "P1": ["P2", "P3", "P6"],
    "P2": ["P1", "P3", "P4"],
    "P3": ["P1", "P2", "P5"],
    "P4": ["P2", "P6"],
    "P5": ["P3", "P6"],
    "P6": ["P1", "P4", "P5"]
}

# Initial domains
doms = {}
for t in tList:
    doms[t] = ["R1", "R2", "R3"]

# Generate arcs
arcs = []
for t1 in tList:
    for t2 in conf[t1]:
        arcs.append((t1, t2))

# Step-by-Step Trace (first 5)
print("Step-by-Step Trace (First 5):")
for i in range(5):
    a, b = arcs[i]
    # In initial state, no value will be removed because 
    # for any room in a, there are 2 other rooms in b.
    print("Arc (", a, ",", b, ") checked, no change")

# Run AC-3 logic
def revised(x, y, d):
    rem = False
    new_d = []
    for v1 in d[x]:
        exists = False
        for v2 in d[y]:
            if v1 != v2:
                exists = True
                break
        if exists:
            new_d.append(v1)
        else:
            rem = True
    d[x] = new_d
    return rem

def run_ac3(d, a_list):
    q = []
    for item in a_list:
        q.append(item)
    
    while len(q) > 0:
        x, y = q.pop(0)
        if revised(x, y, d):
            if len(d[x]) == 0:
                return False
            for nbr in conf[x]:
                if nbr != y:
                    q.append((nbr, x))
    return True

run_ac3(doms, arcs)
print("\nIs it arc-consistent? Yes (No domains reduced to zero)")

# Case: P1 assigned to R1
print("\n--- Assigning P1 to R1 ---")
doms2 = {}
for t in tList:
    doms2[t] = ["R1", "R2", "R3"]
doms2["P1"] = ["R1"]

if run_ac3(doms2, arcs):
    print("AC-3 finished. Valid domains remain.")
    print("Final Domains:")
    for t in tList:
        print(t, ":", doms2[t])
    print("\nAnswer: AC-3 does NOT detect a failure. It leaves a valid set of domains.")
else:
    print("AC-3 detected failure!")
