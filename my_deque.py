import time

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class MyDeque:
    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        self._size = 0
        
        if iterable:
            for item in iterable:
                self.append(item)

    def append(self, value):
        """Add an element to the right side of the deque. O(1)"""
        new_node = Node(value)
        
        if self.tail is None:
            # Empty list
            self.head = new_node
            self.tail = new_node
        else:
            # Connect new node to current tail
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            
        self._size += 1

    def popleft(self):
        """Remove and return an element from the left side of the deque. O(1)"""
        if self.head is None:
            raise IndexError("pop from an empty deque")
        
        value = self.head.value
        
        if self.head == self.tail:
            # Only one element was present
            self.head = None
            self.tail = None
        else:
            # Move head pointer to next
            self.head = self.head.next
            self.head.prev = None # Remove reference to old head
            
        self._size -= 1
        return value

    def pop(self):
        """Remove and return an element from the right side of the deque. O(1)"""
        if self.tail is None:
            raise IndexError("pop from an empty deque")
        
        value = self.tail.value
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            
        self._size -= 1
        return value

    def __len__(self):
        return self._size

    def __bool__(self):
        return self._size > 0
        
    def __str__(self):
        items = []
        current = self.head
        while current:
            items.append(str(current.value))
            current = current.next
        return "MyDeque([" + ", ".join(items) + "])"

if __name__ == "__main__":
    # Correctness Test
    q = MyDeque()
    q.append(1)
    q.append(2)
    q.append(3)
    
    print(f"Queue after appends: {q}")
    print(f"Popped: {q.popleft()}")
    print(f"Popped: {q.popleft()}")
    print(f"Queue after pops: {q}")
    
    # Performance Benchmark vs List
    N = 100000
    
    print(f"\nBenchmarking with {N} elements...")
    
    # List Benchmark
    list_q = []
    start_time = time.time()
    for i in range(N):
        list_q.append(i)
    while list_q:
        list_q.pop(0) # O(N) operation
    list_time = time.time() - start_time
    print(f"Python List Time: {list_time:.6f} seconds")
    
    # MyDeque Benchmark
    my_q = MyDeque()
    start_time = time.time()
    for i in range(N):
        my_q.append(i)
    while my_q:
        my_q.popleft() # O(1) operation
    deque_time = time.time() - start_time
    print(f"MyDeque Time:    {deque_time:.6f} seconds")
    
    if deque_time < list_time:
         print(f"Speedup: {list_time / deque_time:.2f}x faster!")
