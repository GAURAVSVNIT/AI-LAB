
# Backward Chaining Lab Exercise

def can_prove(target, known_facts, rules):
    # base case: if it is a fact
    if target in known_facts:
        return True
    
    # search rules
    for r in rules:
        prems = r[0]
        concl = r[1]
        
        if concl == target:
            # try to prove all premises of this rule
            print("To prove", target, "need to prove", prems)
            all_proven = True
            for p in prems:
                if not can_prove(p, known_facts, rules):
                    all_proven = False
                    break
            
            if all_proven:
                print("Proved", target)
                return True
                
    return False

def solve_a():
    print("--- PROBLEM A ---")
    facts = ['A', 'B']
    # P -> Q, R -> Q, A -> P, B -> R
    kb = [
        [['P'], 'Q'],
        [['R'], 'Q'],
        [['A'], 'P'],
        [['B'], 'R']
    ]
    goal = 'Q'
    
    if can_prove(goal, facts, kb):
        print("Final Conclusion: SUCCESS")
    else:
        print("Final Conclusion: FAILED")

def solve_b():
    print("\n--- PROBLEM B ---")
    # A, E are facts
    # A -> B, B ^ C -> D, E -> C
    data = ['A', 'E']
    logic = [
        [['A'], 'B'],
        [['B', 'C'], 'D'],
        [['E'], 'C']
    ]
    target = 'D'
    
    if can_prove(target, data, logic):
        print("Final Conclusion: SUCCESS")
    else:
        print("Final Conclusion: FAILED")

# Start
solve_a()
solve_b()
