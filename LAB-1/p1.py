class Node:
    def __init__(self,value):
        self.head = None
        self.tail = None
        self.size = 0

class Deque:
    def __init__(self,iterable=None):
        self.head = None
        self.tail = None
        self._size = 0
        if iterable:
            for item in iterable:
                self.append(item)

    def append(self,value):
        new_node = Node(value)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
    
    def popleft(self):
        if self.head is None:
            raise IndexError("popleft from empty deque")
        value = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self._size -= 1
        return value
    
    def pop(self):
        if self.tail is None:
            raise IndexError("pop from empty deque")
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self._size -= 1
        return value
    
    def __len__(self):
        return self._size
    
    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __bool__(self):
        return self._size > 0
        
    def __str__(self):
        items = []
        current = self.head
        while current:
            items.append(str(current.value))
            current = current.next
        return "Deque([" + ", ".join(items) + "])"

adj = {
    'Chicago': {'Detroit': 283, 'Cleveland': 354, 'Indianapolis': 182},
    'Detroit': {'Chicago': 283, 'Buffalo': 256, 'Cleveland': 169},
    'Cleveland': {'Chicago': 345, 'Detroit': 169, 'Buffalo': 189, 'Pittsburgh': 134, 'Columbus': 144},
    'Indianapolis': {'Chicago': 182, 'Columbus': 176},
    'Columbus': {'Indianapolis': 176, 'Cleveland': 144, 'Pittsburgh': 185},
    'Buffalo': {'Detroit': 256, 'Cleveland': 189, 'Syracuse': 150, 'Pittsburgh': 215},
    'Pittsburgh': {'Cleveland': 134, 'Columbus': 185, 'Buffalo': 215, 'Philadelphia': 305, 'Baltimore': 247},
    'Syracuse': {'Buffalo': 150, 'Philadelphia': 253, 'New York': 254, 'Boston': 312},
    'Philadelphia': {'Syracuse': 253, 'Pittsburgh': 305, 'New York': 97, 'Baltimore': 101},
    'Baltimore': {'Pittsburgh': 247, 'Philadelphia': 101},
    'New York': {'Syracuse': 254, 'Philadelphia': 97, 'Providence': 181, 'Boston': 215},
    'Providence': {'New York': 181, 'Boston': 50},
    'Boston': {'Syracuse': 312, 'New York': 215, 'Providence': 50, 'Portland': 107},
    'Portland': {'Boston': 107}
}

def bfs(adj, s, g):
    q = Deque([(s,[s],0)])
    res = []
    while q:
        u, p, c = q.popleft()
        for v, w in adj[u].items():
            if v not in p:
                if v == g:
                    res.append((p + [v], c + w))
                else:
                    q.append((v, p + [v], c + w))
    return res

def dfs(adj, u, g, p=None, c=0):
    if p is None: p = [u]
    if u == g: return [(p, c)]
    res = []
    for v, w in adj[u].items():
        if v not in p:
            paths = dfs(adj, v, g, p + [v], c + w)
            for path in paths: res.append(path)
    return res

st, en = "Syracuse", "Chicago"
print(f"Searching for all paths from {st} to {en}...\n")

print("--- BFS Result ---")
bfs_res = bfs(adj, st, en)
for i, (p, c) in enumerate(bfs_res, 1):
    print(f"Path {i}: {' -> '.join(p)} | Cost: {c}")

print("\n--- DFS Result ---")
dfs_res = dfs(adj, st, en)
for i, (p, c) in enumerate(dfs_res, 1):
    print(f"Path {i}: {' -> '.join(p)} | Cost: {c}")

if bfs_res:
    ans = min(bfs_res, key=lambda x: x[1])
    print(f"\nMin Cost Path: {' -> '.join(ans[0])} | Cost {ans[1]}")
