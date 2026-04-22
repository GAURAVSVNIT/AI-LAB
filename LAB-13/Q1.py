# Lab 13 Q1 - Directly solve infix expression and evaluate truth table
# Using Stack class and associativity rules directly on infix

class Stack:
    def __init__(self):
        self.arr = []
    
    def pu(self, x):
        self.arr.append(x)
        
    def po(self):
        return self.arr.pop()
        
    def top(self):
        if len(self.arr) > 0:
            return self.arr[-1]
        return None
        
    def empty(self):
        if len(self.arr) == 0:
            return True
        return False

e = input("Enter expression (e.g., (~P|Q)->R ) : ")

# clean up
e = e.replace(" ", "")
e = e.replace("<->", "=")
e = e.replace("->", ">")
e = e.replace("AND", "&")
e = e.replace("OR", "|")
e = e.replace("NOT", "~")

prec = {'~': 5, '&': 4, '|': 3, '>': 2, '=': 1}
assoc = {'~': 'R', '&': 'L', '|': 'L', '>': 'R', '=': 'L'}

vars_list = []
for c in e:
    if (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z'):
        if c not in prec and c not in ['(', ')']: # symbol found
            if c not in vars_list:
                vars_list.append(c)

# manual generation for combinations
vars_list.sort()
nv = len(vars_list)
seqs = []

def gen_b(count, temp):
    if count == 0:
        seqs.append(list(temp))
        return
    temp.append(False)
    gen_b(count-1, temp)
    temp.pop()
    temp.append(True)
    gen_b(count-1, temp)
    temp.pop()

gen_b(nv, [])

def apply_op(vals, ops):
    op = ops.po()
    if op == '~':
        v = vals.po()
        vals.pu(not v)
    elif op == '&':
        v2 = vals.po()
        v1 = vals.po()
        vals.pu(v1 and v2)
    elif op == '|':
        v2 = vals.po()
        v1 = vals.po()
        vals.pu(v1 or v2)
    elif op == '>':
        v2 = vals.po()
        v1 = vals.po()
        # implication is False only if v1=T and v2=F
        if v1 == True and v2 == False:
            vals.pu(False)
        else:
            vals.pu(True)
    elif op == '=':
        v2 = vals.po()
        v1 = vals.po()
        if v1 == v2:
            vals.pu(True)
        else:
            vals.pu(False)

def eval_infix(exp, vmap):
    vals = Stack()
    ops = Stack()
    
    for c in exp:
        if c in vars_list:
            vals.pu(vmap[c])
        elif c == '(':
            ops.pu(c)
        elif c == ')':
            while not ops.empty() and ops.top() != '(':
                apply_op(vals, ops)
            if not ops.empty():
                ops.po() # pop '('
        elif c in prec:
            while not ops.empty() and ops.top() != '(':
                ch_top = ops.top()
                if (assoc[c] == 'L' and prec[ch_top] >= prec[c]) or (assoc[c] == 'R' and prec[ch_top] > prec[c]):
                    apply_op(vals, ops)
                else:
                    break
            ops.pu(c)
    
    while not ops.empty():
        apply_op(vals, ops)
        
    return vals.po()

# print header
head = ""
for v in vars_list:
    head = head + v + "\t"
head = head + "Res"
print(head)

# print truth table
for sq in seqs:
    vmap = {}
    for i in range(nv):
        vmap[vars_list[i]] = sq[i]
    
    ans = eval_infix(e, vmap)
    row = ""
    for i in range(nv):
        if sq[i]:
            row = row + "T\t"
        else:
            row = row + "F\t"
    if ans:
        row = row + "T"
    else:
        row = row + "F"
    print(row)
