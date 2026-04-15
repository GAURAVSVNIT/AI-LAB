for s in range(1, 10):
    for e in range(10):
        if e == s: continue
        for n in range(10):
            if n == s or n == e: continue
            for d in range(10):
                if d == s or d == e or d == n: continue
                # m can't be zero
                for m in range(1, 10):
                    if m == s or m == e or m == n or m == d: continue
                    for o in range(10):
                        if o == s or o == e or o == n or o == d or o == m: continue
                        for r in range(10):
                            if r ==s or r == e or r == n or r == d or r == m or r == o: continue
                            for y in range(10):
                                if y == s or y == e or y == n or y == d or y == m or y == o or y == r: continue
                                
                                send = s*1000 + e*100 + n*10 + d
                                more = m*1000 + o*100 + r*10 + e
                                money = m*10000 + o*1000 + n*100 + e*10 + y
                                
                                if send + more == money:
                                    print("S E N D M O R Y")
                                    print(s, e, n, d, m, o, r, y)
                                    print("----------------")
                                    print("SEND:", send)
                                    print("MORE:", more)
                                    print("MONEY:", money)
