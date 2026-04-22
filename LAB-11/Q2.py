
# SEND + MORE = MONEY solver
# Using Backtracking (CSP approach) instead of nested loops

letters = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']
assigned = {}
used_digits = [False] * 10

def solve(idx):
    # base case: all letters assigned
    if idx == len(letters):
        s = assigned['S']
        e = assigned['E']
        n = assigned['N']
        d = assigned['D']
        m = assigned['M']
        o = assigned['O']
        r = assigned['R']
        y = assigned['Y']
        
        send = s*1000 + e*100 + n*10 + d
        more = m*1000 + o*100 + r*10 + e
        money = m*10000 + o*1000 + n*100 + e*10 + y
        
        if send + more == money:
            print("Found Solution with Backtracking:")
            print("SEND:", send)
            print("MORE:", more)
            print("MONEY:", money)
            print("Mapping:", assigned)
            return True
        return False

    char = letters[idx]
    
    # Try digits 0-9
    for val in range(10):
        # S and M cannot be 0
        if val == 0 and (char == 'S' or char == 'M'):
            continue
            
        if not used_digits[val]:
            # Assign
            assigned[char] = val
            used_digits[val] = True
            
            # Recurse
            if solve(idx + 1):
                return True
            
            # Backtrack
            used_digits[val] = False
            del assigned[char]
            
    return False

# Run it
if not solve(0):
    print("No solution found.")
