def crossing_logic(tr, obs, e):
    # emergency or obstacle
    if e == 1 or obs == 1:
        print("Signal: Red  Gate: Raise  Siren: On")
    elif tr == 1:
        print("Signal: Green  Gate: Lower  Siren: On")
    else:
        print("Signal: Red  Gate: Raise  Siren: Off")

def run():
    print("1 for simulation, 2 for manual: ")
    choice = input()
    
    if choice == '1':
        print("Tr | Obs | Em | Action")
        # nested loops for truth table
        for t in [0, 1]:
            for o in [0, 1]:
                for e in [0, 1]:
                    print(t, "|", o, "|", e, "|", end=" ")
                    crossing_logic(t, o, e)
    else:
        print("train (0/1): ")
        t_in = int(input())
        print("obstacle (0/1): ")
        o_in = int(input())
        print("emergency (0/1): ")
        e_in = int(input())
        crossing_logic(t_in, o_in, e_in)

    print("\nPriority: Emergency/Obstacle first, then train.")

if __name__ == "__main__":
    run()
