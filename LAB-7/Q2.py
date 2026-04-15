# Q2 Repeat the above experiment on first choice, random restart and simulated annealing
# variants of hill climbing and compare your results.

import random
import math

def calc(arr):
    h = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if arr[i] == arr[j]:
                h = h + 1
            if abs(arr[i] - arr[j]) == abs(i - j):
                h = h + 1
    return h

def get_rnd_b():
    b = []
    for k in range(8):
        b.append(random.randint(0, 7))
    return b

def run_fc(b):
    # first choice hc
    cur = b
    h1 = calc(cur)
    st = 0
    
    while 1:
        # get random neighbor
        temp = list(cur)
        c = random.randint(0, 7)
        r = random.randint(0, 7)
        temp[c] = r
        
        n_h = calc(temp)
        if n_h < h1:
            cur = temp
            h1 = n_h
            st = st + 1
        else:
            # stop if stuck for a while (hacky way to check local minimum)
            if st > 1000:
                break
            st = st + 1
            
    return cur, h1, st

def run_rr():
    # random restart
    st_tot = 0
    rst = 0
    
    while 1:
        b = get_rnd_b()
        cur = b
        h1 = calc(cur)
        
        # steepest ascent internal
        while 1:
            best_n = list(cur)
            min_h = h1
            for i in range(8):
                for j in range(8):
                    if cur[i] != j:
                        temp = list(cur)
                        temp[i] = j
                        th = calc(temp)
                        if th < min_h:
                            min_h = th
                            best_n = list(temp)
            
            if min_h >= h1:
                break
                
            cur = best_n
            h1 = min_h
            st_tot = st_tot + 1
            
        rst = rst + 1
        if h1 == 0:
            return cur, h1, st_tot, rst

def run_sa(b):
    # simulated annealing
    cur = b
    h1 = calc(cur)
    st = 0
    t = 100.0
    dr = 0.99
    
    while t > 0.001:
        if h1 == 0:
            break
            
        temp = list(cur)
        c = random.randint(0, 7)
        r = random.randint(0, 7)
        temp[c] = r
        n_h = calc(temp)
        
        de = h1 - n_h
        
        if de > 0:
            cur = list(temp)
            h1 = n_h
        else:
            p = math.exp(de / t)
            if random.random() < p:
                cur = list(temp)
                h1 = n_h
                
        t = t * dr
        st = st + 1
        
    return cur, h1, st

print("First Choice HC 50 Runs")
fc_s = 0
fc_f = 0
fc_st = 0
for x in range(50):
    b = get_rnd_b()
    e, v, s = run_fc(b)
    fc_st = fc_st + s
    if v == 0:
        fc_s = fc_s + 1
    else:
        fc_f = fc_f + 1
print("Solved: " + str(fc_s) + " Fails: " + str(fc_f) + " Avg steps: " + str(fc_st/50.0))

print("\nRandom Restart (runs until solved)")
e2, v2, s2, r_cnt = run_rr()
print("Solved in " + str(r_cnt) + " restarts with " + str(s2) + " total steps")

print("\nSimulated Annealing 50 Runs")
sa_s = 0
sa_f = 0
sa_st = 0
for y in range(50):
    b = get_rnd_b()
    e3, v3, s3 = run_sa(b)
    sa_st = sa_st + s3
    if v3 == 0:
        sa_s = sa_s + 1
    else:
        sa_f = sa_f + 1
print("Solved: " + str(sa_s) + " Fails: " + str(sa_f) + " Avg steps: " + str(sa_st/50.0))
