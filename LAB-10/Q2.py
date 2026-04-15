# Erratic Vacuum Cleaning Agent - AND-OR Graph Search
#
# State: (agent_location, tile_A_state, tile_B_state)
#   agent_location : 'A' or 'B'
#   tile states    : 'Clean' or 'Dirty'
#
# Erratic Suck rules:
#   - Suck on Dirty  -> always cleans current tile,
#                       SOMETIMES also cleans adjacent tile  (two outcomes)
#   - Suck on Clean  -> sometimes deposits dirt on current tile (two outcomes)
#
# AND-OR search:
#   OR  node  = agent chooses an action
#   AND node  = ALL possible world outcomes of that action must be handled

ACTIONS = ['Suck', 'Right', 'Left']

# -------------------------------------------------------
# Goal check
# -------------------------------------------------------
def is_goal(state):
    loc, a, b = state
    return a == 'Clean' and b == 'Clean'

# -------------------------------------------------------
# Erratic transition model
# Returns SET of possible next states for (state, action)
# -------------------------------------------------------
def results(state, action):
    loc, a, b = state

    if action == 'Right':
        return {('B', a, b)}

    if action == 'Left':
        return {('A', a, b)}

    # Suck
    if action == 'Suck':
        outcomes = set()
        if loc == 'A':
            if a == 'Dirty':
                outcomes.add(('A', 'Clean', b))        # only A cleaned
                outcomes.add(('A', 'Clean', 'Clean'))  # A cleaned + adjacent B also cleaned
            else:  # A is Clean
                outcomes.add(('A', 'Clean', b))        # no change
                outcomes.add(('A', 'Dirty', b))        # deposits dirt on A
        else:  # loc == 'B'
            if b == 'Dirty':
                outcomes.add(('B', a, 'Clean'))        # only B cleaned
                outcomes.add(('B', 'Clean', 'Clean'))  # B cleaned + adjacent A also cleaned
            else:  # B is Clean
                outcomes.add(('B', a, 'Clean'))        # no change
                outcomes.add(('B', a, 'Dirty'))        # deposits dirt on B
        return outcomes

# -------------------------------------------------------
# AND-OR search
# Returns a conditional plan (nested dict) or 'failure'
#
# Plan structure:
#   { 'action': <action>,
#     'if': { outcome_state: sub_plan, ... } }
#   or 'Goal' if already at goal
# -------------------------------------------------------
def or_search(state, visited):
    if is_goal(state):
        return 'Goal'
    if state in visited:
        return 'failure'

    visited = visited | {state}   # immutable copy for this branch

    for action in ACTIONS:
        outcomes = results(state, action)
        sub_plan = and_search(outcomes, visited)
        if sub_plan != 'failure':
            return {'action': action, 'branches': sub_plan}

    return 'failure'


def and_search(outcome_states, visited):
    # All outcomes must be solvable
    plans = {}
    for s in outcome_states:
        plan = or_search(s, visited)
        if plan == 'failure':
            return 'failure'
        plans[s] = plan
    return plans

# -------------------------------------------------------
# Pretty-print the conditional plan
# -------------------------------------------------------
def print_plan(plan, indent=0):
    pad = "  " * indent
    if plan == 'Goal':
        print(pad + "[GOAL - tiles are clean]")
        return
    if plan == 'failure':
        print(pad + "[FAILURE]")
        return

    action = plan['action']
    branches = plan['branches']
    print(pad + f"DO: {action}")

    if len(branches) == 1:
        sub = list(branches.values())[0]
        print_plan(sub, indent)
    else:
        for outcome, sub in branches.items():
            print(pad + f"  IF outcome => {outcome}:")
            print_plan(sub, indent + 2)

# -------------------------------------------------------
# Run AND-OR search from all 8 possible initial states
# -------------------------------------------------------
locations = ['A', 'B']
tile_states = ['Clean', 'Dirty']

all_states = [(loc, a, b)
              for loc in locations
              for a in tile_states
              for b in tile_states]

print("=" * 60)
print("   ERRATIC VACUUM AGENT - AND-OR GRAPH SEARCH")
print("=" * 60)

results_table = []
for init in all_states:
    plan = or_search(init, frozenset())
    results_table.append((init, plan))

# Summary table
print(f"\n{'Initial State':<35} {'Plan Found?':>12}")
print("-" * 49)
for init, plan in results_table:
    loc, a, b = init
    label = f"Loc={loc}, A={a}, B={b}"
    found = "YES" if plan != 'failure' else "NO"
    print(f"  {label:<33} {found:>12}")

# Detailed plans
print("\n" + "=" * 60)
print("   DETAILED CONDITIONAL PLANS")
print("=" * 60)
for init, plan in results_table:
    loc, a, b = init
    print(f"\n[Start] Location={loc}  A={a}  B={b}")
    print("-" * 40)
    print_plan(plan)
