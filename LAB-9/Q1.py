board = [
    ['-', '-', '-'],
    ['-', '-', '-'],
    ['-', '-', '-']
]

states = 0

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
    global states
    states = states + 1
    
    ind = ""
    for x in range(depth):
        ind = ind + "    "
    ind = ind + "|-- "
    
    res = check_win(b)
    if res == 'X':
        return 10 - depth
    elif res == 'O':
        return -10 + depth
    elif res == 'Tie':
        return 0
        
    if is_max == True:
        best = -1000
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                if b[i][j] == '-':
                    b[i][j] = 'X'
                    print(ind + "X -> " + str(i) + "," + str(j))
                    val = minimax(b, depth + 1, False)
                    b[i][j] = '-'
                    if val > best:
                        best = val
        return best
    else:
        best = 1000
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                if b[i][j] == '-':
                    b[i][j] = 'O'
                    print(ind + "O -> " + str(i) + "," + str(j))
                    val = minimax(b, depth + 1, True)
                    b[i][j] = '-'
                    if val < best:
                        best = val
        return best

def find_best(b):
    global states
    states = 0
    best_val = -1000
    best_r = -1
    best_c = -1
    
    print("Tree:")
    
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if b[i][j] == '-':
                b[i][j] = 'X'
                print("|-- X -> " + str(i) + "," + str(j))
                move_val = minimax(b, 1, False)
                b[i][j] = '-'
                if move_val > best_val:
                    best_r = i
                    best_c = j
                    best_val = move_val
                    
    print("\nStates: " + str(states))
    return [best_r, best_c]

# Check on board
board[0][0] = 'O'
board[0][1] = 'X'
board[0][2] = 'O'
board[1][0] = '-'
board[1][1] = '-'
board[1][2] = '-'
board[2][0] = '-'
board[2][1] = '-'
board[2][2] = '-'

print("Board:")
print_b(board)

ans = find_best(board)
print("Best Move: " + str(ans[0]) + "," + str(ans[1]))
