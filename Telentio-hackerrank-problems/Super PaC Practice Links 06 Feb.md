# Super PaCC | Practice Links | 06 Feb

## Insert a node at a specific position in a linked list
```py
class Node(object):
 
    def __init__(self, data=None, next_node=None):
       self.data = data
       self.next = next_node

def insertNodeAtPosition(head, data, position):
    if position==0:
        head = Node(data,head)
        return head
    else:
        temp_head = head
        while position>1:
            temp_head = temp_head.next
            position = position -1
        temp_head.next = Node(data,temp_head.next)
        return head
```
## Reverse a doubly linked list
```py 
def reverse(head):
    if head == None or head.next == None:
        return head
    
    while True:
        temp = head.next
        head.next = head.prev
        head.prev = temp
        head = head.prev
        
        if head.next == None:
            break
    temp = head.next
    head.next = head.prev
    head.prev = temp
    return head
```
## Inserting a Node Into a Sorted Doubly Linked List
```py
def sortedInsert(head, data):
    cur=head
    node=DoublyLinkedListNode(data)
    if cur.data>data or cur.data==data:
        node.next=cur
        cur.prev=node
        head=node
        return head
    while cur.next:
        if (cur.data<data and cur.next.data>data) or cur.data==data:
            node.next=cur.next
            cur.next.prev=node
            node.prev=cur
            cur.next=node
            return head
        cur=cur.next
    if cur.data<data or cur.data==data:
        node.prev=cur
        cur.next=node
        return head
```
## Balanced Brackets
```py
def check():
    stack = []
    s = input()
    for c in s:
        #print(c)
        if c == '(':
            stack.append(0);
        elif c == ')':
            if len(stack) > 0 and stack[-1] == 0:
                stack.pop()
            else:
                return -1
        elif c == '[':
            stack.append(2)
        elif c == ']':
            if len(stack) > 0 and stack[-1] == 2:
                stack.pop()
            else:
                return -1
        if c == '{':
            stack.append(4)
        elif c == '}':
            if len(stack) > 0 and stack[-1] == 4:
                stack.pop()
            else:
                return -1
    
    if len(stack) == 0:
        return 0
    else:
        return -1

def solve():
    t = int(input())
    for i in range(0,t):
        if check() == 0:
            print("YES")
        else:
            print("NO")
solve()          
```
## Maximum Element
```py
n = int(input())
stack = []
most = []

for i in range(n):
    data = input().split(' ')
    x = int(data[0])
    v = 0
    if len(data) > 1: v = int(data[1])
    if x == 1:
        stack.append(v)
        if not most or most[-1] <= v: most.append(v)
    elif x == 2:
        v = stack.pop()
        if most[-1] == v: most.pop()
    else:
        print(most[-1])
```
## Next Greater Element 11
```py
n=input()
arr = [int(i) for i in input().split()]
def printNGE(arr):
 
    for i in range(0, len(arr), 1):
 
        next = -1
        for j in range(i+1, len(arr), 1):
            if arr[i] < arr[j]:
                next = arr[j]
                break
 
        print(str(next),end=" ")
printNGE(arr)
```
## Queue using Two Stacks
```py
old, new = [], []
for _ in range(int(input())):
    val = list(map(int,input().split()))
    if val[0] == 1:
        new.append(val[1])
    elif val[0] == 2:
        if not old :
            while new : old.append(new.pop())
        old.pop()
    else:
        print(old[-1] if old else new[0])
```
# Castle on the Grid
```py
import numbers
import math
from collections import namedtuple,deque
class point(namedtuple("point", "i j")):
    def __eq__(self,o):
        return self.i == o.i and self.j == o.j
    def __ne__(self, o):
        return self.i != o.i or self.j != o.j
    def __lt__(self, o):
        return self.i < o.i or self.j < o.j
    def __gt__(self, o):
        return self.i > o.i or self.j > o.j
    def __le__(self, o):
        return self.i <= o.i or self.j <= o.j
    def __ge__(self, o):
        return self.i >= o.i or self.j >= o.j
    def __rshift__(self,o):
        return self.i >= o.i and self.j >= o.j
    def __lshift__(self,o):
        return self.i <= o.i and self.j <= o.j
    def __hash__(self):
        return hash((self.i, self.j))
    def __repr__(self):
        return 'p(%r, %r)' % self
    def __add__(self,o):
        if isinstance(o, point):
            return point.__new__(point,self.i+o.i,self.j+o.j)
        if isinstance(o, numbers.Number):
            return point.__new__(point,self.i+o,self.j+o)
        return NotImplemented
    def __iadd__(self,o):
        return self.__add__(o)
    def __sub__(self,o):
        if isinstance(o, point):
            return point.__new__(point,self.i-o.i,self.j-o.j)
        if isinstance(o, numbers.Number):
            return point.__new__(point,self.i-o,self.j-o)
        return NotImplemented
    def inbound(self,a,b=None):
        if b is None:
            a,b = point(0,0),a
        im,ix = sorted([a.i,b.i])
        jm,jx = sorted([a.j,b.j])
        return im <= self.i and self.i < ix and jm <= self.j and self.j < jx
    def distance(self,o):
        return abs(self.i-o.i)+abs(self.j-o.j)
        #return math.sqrt((self.i-o.i)**2+(self.j-o.j)**2)
    def __isub__(self,o):
        return self.__sub__(o)
    def __neg__(self):
        return point.__new__(point,-self.i,-self.j)
    def I():
        return point.__new__(point,1,0)
    def J():
        return point.__new__(point,0,1)

class grid(list):
    def __getitem__(self, *args, **kwargs):
        if isinstance(args[0], point):
            return self[args[0].i][args[0].j]
        else:
            return list.__getitem__(self, *args, **kwargs)
    def __setitem__(self, *args, **kwargs):
        if isinstance(args[0], point):
            self[args[0].i][args[0].j] = args[1]
        else:
            return list.__setitem__(self, *args, **kwargs)
    def __repr__(self):
        return "\n".join(["".join(map(lambda x:str(x)[-1],a)) for a in self])

around = (-point.I(),-point.J(),point.J(),point.I())
n = int(input())
b = grid([list(input()) for _ in range(n)])
_ = list(map(int,input().split()))
p = point(_[0],_[1])
f = point(_[2],_[3])
b[p] = "#"
b[f] = "E"
q = deque([(p,0)])



vg = grid([[False for _ in range(len(b[0]))] for _ in range(len(b))])
while len(q):
    
    c,d = q.popleft()

    vg[c] = True
    #print(c,b[c.i][c.j])
    if c == f:
        break
    if b[c] == ".":
        b[c] = "="

    for di in around:
        pt = c
        while True:
            pt += di
            if pt.inbound(point(0,0) ,point(len(b),len(b[0]))) and (b[pt] == "." or b[pt] == "E") :
                q.append((pt,d+1))
                vg[pt] = True
                if b[pt] == ".":
                    b[pt] = d+1
            else:
                break
    
    #print(c,ar)
    #print(q)

#print(b)    
print(d)
```
