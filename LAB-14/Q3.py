
# Resolution and Proof by Contradiction Lab

def negate(lit):
    if lit.startswith('~'):
        return lit[1:]
    else:
        return '~' + lit

def resolve(c1, c2):
    # try to find a literal to cancel out
    for l1 in c1:
        for l2 in c2:
            if l1 == negate(l2):
                # found contradiction between l1 and l2
                new_c = []
                for x in c1:
                    if x != l1: new_c.append(x)
                for y in c2:
                    if y != l2:
                        if y not in new_c: # avoid duplicates
                            new_c.append(y)
                return sorted(new_c)
    return None

def solve_resolution(clauses, goal):
    print("Initial Clauses (KB + Negated Goal):", clauses)
    
    work = list(clauses)
    steps = 0
    
    while True:
        new_clauses = []
        n = len(work)
        
        # brute force nested loops
        for i in range(n):
            for j in range(i + 1, n):
                res = resolve(work[i], work[j])
                
                if res is not None:
                    if res == []:
                        print("Resolved", work[i], "and", work[j], "-> []")
                        print("CONTRADICTION FOUND! Goal is proven.")
                        return True
                    
                    if res not in work and res not in new_clauses:
                        new_clauses.append(res)
                        print("Resolved", work[i], "and", work[j], "->", res)
        
        if not new_clauses:
            break
            
        work.extend(new_clauses)
        steps += 1
        if steps > 50: # safety break
            break
            
    print("No more resolutions possible. Goal could not be proven.")
    return False

def prob_a():
    print("\n--- Solving Problem A ---")
    # P v Q, P->R, Q->S, R->S, Goal S
    # CNF: {P,Q}, {~P,R}, {~Q,S}, {~R,S}
    # Neg Goal: {~S}
    kb = [
        ['P', 'Q'],
        ['~P', 'R'],
        ['~Q', 'S'],
        ['~R', 'S'],
        ['~S']
    ]
    solve_resolution(kb, 'S')

def prob_b():
    print("\n--- Solving Problem B ---")
    # P->Q, Q->R, S->~R, P, Goal S
    # CNF: {~P,Q}, {~Q,R}, {~S,~R}, {P}
    # Neg Goal: {~S}
    kb = [
        ['~P', 'Q'],
        ['~Q', 'R'],
        ['~S', '~R'],
        ['P'],
        ['~S']
    ]
    # Note: If P is true, then R is true. S->~R means S must be false.
    # Trying to prove S by refutation means adding ~S.
    # But ~S is already in the KB basically. We won't find [].
    solve_resolution(kb, 'S')

prob_a()
prob_b()
