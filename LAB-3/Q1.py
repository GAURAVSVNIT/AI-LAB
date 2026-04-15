import random

def check_rules(room, status):
    if status == 'Dirty':
        return 'Suck'
    if room == 'A':
        return 'Right'
    if room == 'B':
        return 'Right'
    if room == 'C':
        return 'Left'

def solve():
    print("Room A status (c/d): ")
    s1 = input()
    print("Room B status (c/d): ")
    s2 = input()
    print("Room C status (c/d): ")
    s3 = input()
    
    # store in list
    rooms = [s1, s2, s3]
    for i in range(3):
        if rooms[i] == 'd': rooms[i] = 'Dirty'
        else: rooms[i] = 'Clean'

    locs = ['A', 'B', 'C']
    print("Start loc (0 for A, 1 for B, 2 for C): ")
    idx = int(input())
    
    score = 0
    print("Step | Percept | Action | Score")
    
    for step in range(1, 11):
        curr_room = locs[idx]
        curr_status = rooms[idx]
        
        act = check_rules(curr_room, curr_status)
        
        if act == 'Suck':
            rooms[idx] = 'Clean'
            score = score + 10
        elif act == 'Right':
            score = score - 1
            if idx < 2: idx = idx + 1
        elif act == 'Left':
            score = score - 1
            if idx > 0: idx = idx - 1
            
        print(step, " | ", curr_room, curr_status, " | ", act, " | ", score)
        
        # check if all clean
        if rooms[0] == 'Clean' and rooms[1] == 'Clean' and rooms[2] == 'Clean':
            print("all cleaned")
            break

    print("Final Score: ", score)

if __name__ == "__main__":
    solve()
