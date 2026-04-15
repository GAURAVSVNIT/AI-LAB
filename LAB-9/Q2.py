states_mm = 0
states_ab = 0

def print_b(b):
    for r in b:
        print(r[0] + " " + r[1] + " " + r[2])
    print("")

def check_win(b):
    if b[0][0] == b[0][1] and b[0][1] == b[0][2] and b[0][0] != '-': return b[0][0]
    if b[1][0] == b[1][1] and b[1][1] == b[1][2] and b[1][0] != '-': return b[1][0]
    if b[2][0] == b[2][1] and b[2][1] == b[2][2] and b[2][0] != '-': return b[2][0]
    
    if b[0][0] == b[1][0] and b[1][0] == b[2][0] and b[0][0] != '-': return b[0][0]
    if b[0][1] == b[1][1] and b[1][1] == b[2][1] and b[0][1] != '-': return b[0][1]
    if b[0][2] == b[1][2] and b[1][2] == b[2][2] and b[0][2] != '-': return b[0][2]
    
    if b[0][0] == b[1][1] and b[1][1] == b[2][2] and b[0][0] != '-': return b[0][0]
    if b[0][2] == b[1][1] and b[1][1] == b[2][0] and b[0][2] != '-': return b[0][2]
    
    empty = 0
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if b[i][j] == '-':
                empty = empty + 1
    if empty == 0:
        return 'Tie'
    
    return 'None'

def minimax(b, depth, is_max):
    global states_mm
    states_mm = states_mm + 1
    
    res = check_win(b)
    if res == 'X': return 10 - depth
    elif res == 'O': return -10 + depth
    elif res == 'Tie': return 0
        
    if is_max == True:
        best = -1000
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                if b[i][j] == '-':
                    b[i][j] = 'X'
                    val = minimax(b, depth + 1, False)
                    b[i][j] = '-'
                    if val > best: best = val
        return best
    else:
        best = 1000
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                if b[i][j] == '-':
                    b[i][j] = 'O'
                    val = minimax(b, depth + 1, True)
                    b[i][j] = '-'
                    if val < best: best = val
        return best

def alphabeta(b, depth, is_max, a, be):
    global states_ab
    states_ab = states_ab + 1
    
    ind = ""
    for x in range(depth):
        ind = ind + "    "
    ind = ind + "|-- "
    
    res = check_win(b)
    if res == 'X': return 10 - depth
    elif res == 'O': return -10 + depth
    elif res == 'Tie': return 0
        
    if is_max == True:
        best = -1000
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                if b[i][j] == '-':
                    b[i][j] = 'X'
                    print(ind + "X -> " + str(i) + "," + str(j))
                    val = alphabeta(b, depth + 1, False, a, be)
                    b[i][j] = '-'
                    if val > best: best = val
                    if best > a: a = best
                    if be <= a:
                        print(ind + "Pruned!")
                        return best
        return best
    else:
        best = 1000
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                if b[i][j] == '-':
                    b[i][j] = 'O'
                    print(ind + "O -> " + str(i) + "," + str(j))
                    val = alphabeta(b, depth + 1, True, a, be)
                    b[i][j] = '-'
                    if val < best: best = val
                    if best < be: be = best
                    if be <= a:
                        print(ind + "Pruned!")
                        return best
        return best

def test_board(b, name):
    global states_mm
    global states_ab
    states_mm = 0
    states_ab = 0
    
    print("------- " + name + " -------")
    print_b(b)
    
    best_val_mm = -1000
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if b[i][j] == '-':
                b[i][j] = 'X'
                move_val = minimax(b, 0, False)
                b[i][j] = '-'
                if move_val > best_val_mm:
                    best_val_mm = move_val
                    
    print("Tree built by Alpha-Beta:")
    best_val_ab = -1000
    a = -1000
    be = 1000
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if b[i][j] == '-':
                b[i][j] = 'X'
                print("|-- X -> " + str(i) + "," + str(j))
                move_val = alphabeta(b, 1, False, a, be)
                b[i][j] = '-'
                if move_val > best_val_ab:
                    best_val_ab = move_val
                if best_val_ab > a:
                    a = best_val_ab

    print("")
    print("Minimax States   : " + str(states_mm))
    print("AlphaBeta States : " + str(states_ab))
    print("")

board1 = [
    ['X', 'O', 'X'],
    ['O', '-', '-'],
    ['-', '-', '-']
]

board2 = [
    ['-', 'O', '-'],
    ['X', '-', 'X'],
    ['-', '-', 'O']
]

test_board(board1, "Board 1")
test_board(board2, "Board 2")
