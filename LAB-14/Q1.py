
# Forward Chaining Program for AI Lab

def solve_a():
    print("Solving Problem (a)...")
    # Facts given
    facts = ['A', 'B', 'M']
    
    # Rules represented as [premises, conclusion]
    # P -> Q, L ^ M -> P, A ^ B -> L
    rules = [
        [['P'], 'Q'],
        [['L', 'M'], 'P'],
        [['A', 'B'], 'L']
    ]
    
    goal = 'Q'
    count = 0
    
    while True:
        added = False
        for r in rules:
            pre = r[0]
            concl = r[1]
            
            if concl in facts:
                continue
                
            # Check if all premises are in facts
            check = True
            for p in pre:
                if p not in facts:
                    check = False
                    break
            
            if check:
                facts.append(concl)
                print("Added:", concl, "Current facts:", facts)
                added = True
                if concl == goal:
                    print("Conclusion Q reached!")
                    return
        
        if not added:
            break
            
    print("Could not reach goal.")

def solve_b():
    print("\nSolving Problem (b)...")
    # A -> B, B -> C, C -> D, A, E, D ^ E -> F
    known = ['A', 'E']
    target = 'F'
    
    # KB rules
    kb = [
        [['A'], 'B'],
        [['B'], 'C'],
        [['C'], 'D'],
        [['D', 'E'], 'F']
    ]
    
    changed = True
    while changed:
        changed = False
        for rule in kb:
            pms = rule[0]
            res = rule[1]
            
            if res in known:
                continue
            
            # brute force check
            all_in = True
            for p in pms:
                if p not in known:
                    all_in = False
            
            if all_in:
                known.append(res)
                print("Inferred:", res)
                changed = True
                if res == target:
                    print("Conclusion F reached!")
                    return

    print("Target not found.")

# Run them
solve_a()
solve_b()
