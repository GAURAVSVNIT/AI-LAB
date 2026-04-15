# Sudoku Hard Puzzle AC-3

grid_rows = [
    "000006000",
    "059000008",
    "200008000",
    "045000000",
    "003000000",
    "006003050",
    "000007000",
    "000000000",
    "000050002"
]
s_grid = "".join(grid_rows)

# vars: 0 to 80
# doms
d = {}
for i in range(81):
    val = int(s_grid[i])
    if val == 0:
        d[i] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:
        d[i] = [val]

# Neighbors
def get_nbrs(i):
    res = set()
    r = i // 9
    c = i % 9
    
    # Row
    for col in range(9):
        if col != c:
            res.add(r * 9 + col)
    # Col
    for row in range(9):
        if row != r:
            res.add(row * 9 + c)
    # Box
    br = (r // 3) * 3
    bc = (c // 3) * 3
    for row in range(br, br + 3):
        for col in range(bc, bc + 3):
            idx = row * 9 + col
            if idx != i:
                res.add(idx)
    return res

# Arcs
arcs = []
for i in range(81):
    nbrs = get_nbrs(i)
    for n in nbrs:
        arcs.append((i, n))

def revised(xi, xj):
    rem = False
    new_di = []
    for v1 in d[xi]:
        # is there a v2 in d[xj] such that v1 != v2
        ok = False
        for v2 in d[xj]:
            if v1 != v2:
                ok = True
                break
        if ok:
            new_di.append(v1)
        else:
            rem = True
    d[xi] = new_di
    return rem

# AC-3
q = []
for a in arcs:
    q.append(a)

removed = 0
while len(q) > 0:
    xi, xj = q.pop(0)
    old_len = len(d[xi])
    if revised(xi, xj):
        removed += (old_len - len(d[xi]))
        if len(d[xi]) == 0:
            print("Failure: Empty Domain at index", xi)
            break
        for xk in get_nbrs(xi):
            if xk != xj:
                q.append((xk, xi))

print("Total values removed:", removed)

# Visualization
print("\nGrid of Domain Sizes:")
for r in range(9):
    row_str = ""
    for c in range(9):
        row_str += str(len(d[r*9 + c])) + " "
    print(row_str)

# Final Conclusion
print("\n" + "="*30)
print("ANSWER TO KEY QUESTION:")
if any(len(d[i]) == 0 for i in range(81)):
    print("- AC-3 detected a failure (domain reached zero).")
elif all(len(d[i]) == 1 for i in range(81)):
    print("- AC-3 solved the puzzle completely.")
else:
    print("- AC-3 reduced the search space but did NOT solve it completely.")
    print("- No domain was reduced to zero (puzzle not proven unsolvable).")

print("\nCONCLUSION:")
print("Standard arc consistency thinned out the search space (removed " + str(removed) + " values),")
print("but for this Hard puzzle, a human or backtracking is still needed.")
print("="*30)
