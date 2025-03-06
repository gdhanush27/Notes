# Super PaCC | Practice Links | 07 Feb

## Tree: Level Order Traversal

```py
from collections import deque

def levelOrder(root):
    #Write your code here
    if not root: return 
    
    queue = deque()
    queue.append(root)
    while queue:
        el = queue.popleft()
        print(el.info, end = ' ')
        if el.left: 
            queue.append(el.left)
        if el.right: 
            queue.append(el.right)
```

## Binary Search Tree : Insertion

```py 
#self.info (the value of the node)

    def insert(self, val):
        if self.root is None:
            self.root=Node(val)
        else:
            current = self.root
            while True:
                if val < current.info:
                    if current.left is None:
                        current.left=Node(val)
                        break
                    else:
                        current=current.left
                else:
                    if current.right is None:
                        current.right=Node(val)
                        break
                    else:
                        current=current.right
```

# Tree: Huffman Decoding

```py
def decodeHuff(root, s):
    #Enter Your Code Here
    cur = root
    chararray = []
    #For each character, 
    #If at an internal node, move left if 0, right if 1
    #If at a leaf (no children), record data and jump back to root AFTER processing character
    for c in s:
        if c == '0' and cur.left:
            cur = cur.left
        elif cur.right:
            cur = cur.right
        
        if cur.left is None and cur.right is None:
            chararray.append(cur.data)
            cur = root
    
    #Print final array
    print("".join(chararray))
```

# Binary Search Tree : Lowest Common Ancestor

```py
def lca(root, v1, v2):
    if (root.info < v1 and root.info > v2) or (root.info > v1 and root.info < v2):
        return root
    elif root.info < v1 and root.info < v2:
        return lca(root.right, v1, v2)
    elif root.info > v1 and root.info > v2:
        return lca(root.left, v1, v2)
    elif root.info == v1 or root.info == v2:
        return root
```

# Tree: Height of a Binary Tree

```py
def height(root):
    leftHeight = 0
    rightHeight = 0
    
    if(root.left):
        leftHeight = height(root.left) + 1
    
    if(root.right):
        rightHeight = height(root.right) + 1
    
    if(leftHeight > rightHeight):
        return leftHeight
    else:
        return rightHeight
```

# Frog in Maze

```py
import sys

from collections import deque

def ismine(char):
  return char == '*'

def isexit(char):
  return char == '%'

def isopen(char):
  return char == 'A' or char == 'O'

def isobstacle(char):
  return char == '#'

def probability(node):
  if ismine(node): # mine
    return 0.0
  if isexit(node): # exit
    return 1.0
  # if tunnel(node) != None: # tunnel

def getneighbs(node):
  # print("Getting neighbs for",node)
  global n,m,tunnels
  i0,j0 = node
  dirs = [(0,1),(1,0),(-1,0),(0,-1)]
  out = []
  for di, dj in dirs:
    i,j = i0+di, j0+dj
    if i < 0 or i >= n:
      continue
    if j < 0 or j >= m:
      continue
    if (i,j) in tunnels:
      i,j = tunnels[(i,j)]
    ch = mat[i][j]
    if isobstacle(ch):
      continue
    out.append(mapping[(i,j)])
  return out

def matmult(m, times): # m is square
  if times == 0:
    return m
  n = len(m)
  newm = [[sum(a*b for a,b in zip(X_row,Y_col) if a != 0 and b!= 0) for Y_col in zip(*m)] for X_row in m]
  return matmult(newm, times - 1)

n, m, k = map(int,input().strip().split(' '))
mat = [[None for _ in range(m)] for _ in range(n)]
mapping = {} # maps (i,j) to a row/col in our move matrix
reversemapping = {} # maps a node to (i,j)
MAP_MINE = -2
MAP_EXIT = -1
MAP_START = 0
next_open = 1

def pmat(m):
  return True
  print("---")
  for r in m:
    print(" ".join(["%0.2f"%v for v in r]))

def mygauss(m):
    #eliminate columns
    for col in range(len(m[0])):
        for row in range(col+1, len(m)):
            r = [(rowValue * (-(m[row][col] / m[col][col]))) for rowValue in m[col]]
            m[row] = [sum(pair) for pair in zip(m[row], r)]
    #now backsolve by substitution
    ans = []
    m.reverse() #makes it easier to backsolve
    for sol in range(len(m)):
            if sol == 0:
                ans.append(m[sol][-1] / m[sol][-2])
            else:
                inner = 0
                #substitute in all known coefficients
                for x in range(sol):
                    inner += (ans[x]*m[sol][-2-x])
                #the equation is now reduced to ax + b = c form
                #solve with (c - b) / a
                ans.append((m[sol][-1]-inner)/m[sol][-sol-2])
    ans.reverse()
    return ans
  
for i in range(n):
    row = input().strip()
    for j, char in enumerate(row):
      mat[i][j] = char
      if isobstacle(char):
        continue
      if char == 'A':
        node = MAP_START
        reversemapping[node] = (i,j)
      elif ismine(char):
        node = MAP_MINE
      elif isexit(char):
        node = MAP_EXIT
      else: # open
        node = next_open
        reversemapping[node] = (i,j)
        next_open += 1
      mapping[(i,j)] = node
#print(mapping)
tunnels = {}
for a0 in range(k):
    i1, j1, i2, j2 = map(lambda x: int(x) - 1, input().strip().split(' '))
    tunnels[(i1,j1)] = (i2,j2)
    tunnels[(i2,j2)] = (i1,j1)
nodes = next_open + 2
transitions = [[0 for _ in range(nodes)] for _ in range(nodes)] # transitions[i][j] is probability of ending up at j from i
transitions[MAP_MINE][MAP_MINE] = 1 # try zero to make it disappear from probailities
transitions[MAP_EXIT][MAP_EXIT] = 1
for i in range(nodes - 2):
  neighbs = getneighbs(reversemapping[i])
  opts = len(neighbs)
  if opts == 0:
    # leave at zero to make it disappear from the probabilities
    # transitions[i][i] = 1
    continue
  for j in neighbs:
    transitions[i][j] += 1 / opts
# make the transitions matrix all in upper-right quadrant (drive to the end)
for i in range(nodes):
  for j in range(nodes):
    if j < i: # back-transition, substitute that row here
      p = transitions[i][j]
      if p > 0:
        # print(i,j)
        transitions[i][j] = 0
        transitions[i] = [transitions[i][k] + p*transitions[j][k] for k in range(nodes)]
    if j == i and i < nodes-2: # move on, except end goals
      p = transitions[i][j]
      if p > 0: # if we get back to here, distribute that among the other probs
        transitions[i][j] = 0
        for k in range(j+1,nodes):
          if transitions[i][k] > 0:
            transitions[i][k] /= (1-p)
pmat(transitions)
# now fully cancel out row 0 except for endpoints
for i in range(1,nodes-2):
  p = transitions[0][i]
  if p > 0:
        transitions[0][i] = 0
        for k in range(i+1,nodes):
          transitions[0][k] += p*transitions[i][k]
    
# transitions = mygauss(transitions)
pmat(transitions)
print(transitions[0][MAP_EXIT])
```

# Roads and Libraries

```py
from collections import defaultdict
from collections import deque

from math import pi,cos,sin

class graph:
    def __init__(self):
        self.nodes = []
        self.edges = defaultdict(set)
    def clone(self):
        g = graph()
        g.nodes = self.nodes[:]
        for n in self.nodes:
            for e in self.edges[n]:
                g.edges[n].add(e)
        return g

def count_clusters(g):
    nclust = 0
    used = set()
    n = len(g.nodes)

    csize = []
    
    for node in g.nodes:
        if node in used: continue
        used.add(node)

        size = 1
        Q = deque()
        Q.appendleft(node)
        while Q:
            cur = Q.pop()
            for neigh in g.edges[cur]:
                if neigh in used: continue
                used.add(neigh)
                Q.appendleft(neigh)
                size += 1
        nclust += 1
        csize.append(size)

    return nclust,csize

q = int(input())


for _ in range(q):
    n,m,clib,croad = [int(x) for x in input().split()]
    edges = [[int(x) for x in input().split()] for _ in range(m)]

    if clib < croad:
        print(clib*n)
        continue
    
    g = graph()
    g.nodes = range(1,n+1)
    for a,b in edges:
        g.edges[a].add(b)
        g.edges[b].add(a)

    nc,cs = count_clusters(g)
    print(nc*clib + sum((x-1)*croad for x in cs))
```

# Journey to the Moon

```py
import sys

def findPrt(a):
  if prt[a] < 0:
    return a
  prt[a] = findPrt(prt[a])
  return prt[a]

def join(a, b):
  a = findPrt(a)
  b = findPrt(b)
  if a != b:
    prt[a] = b

n, i = sys.stdin.readline().split()
n, i = int(n), int(i)
prt = [-1 for k in range(n)]
for k in range(i):
  a, b = sys.stdin.readline().split()
  a, b = int(a), int(b)
  join(a, b)

count = [0 for k in range(n)]
for k in range(n):
  pk = findPrt(k)
  count[pk] = count[pk] + 1
print(sum([a * (n - a) for a in count]) // 2)
```

# Synchronous Shopping

```py
from collections import deque

import heapq


def shop(n, k, centers, roads):

    # Write your code here
    fish_masks = [0]
    all_fishes_mask = 2 ** k - 1
    f = 1
    for _ in range(k):
        fish_masks.append(f)
        f <<= 1

    cities = [0] * (n + 1)
    for idx, c_str in enumerate(centers):
        c_data = list(map(int, c_str.split()))
        if c_data[0] > 0:
            cities[idx + 1] = sum([fish_masks[i] for i in c_data[1:]])

    neighbours = [[] for _ in range(n+1)]
    times = [[0] * (n+1) for _ in range(n+1)]
    for c1, c2, t in roads:
        neighbours[c1].append(c2)
        neighbours[c2].append(c1)
        times[c1][c2] = t
        times[c2][c1] = t

    q = [(1 << 10) + cities[1]]
    seen = [[False] * (all_fishes_mask + 1) for _ in range(n + 1)]
    trip_time = [[None] * (all_fishes_mask + 1) for _ in range(n + 1)]

    fish_mask = 2 ** 10 - 1
    node_mask = fish_mask << 10
    
    while q:
        data = heapq.heappop(q)
        time = data >> 20
        node = (data & node_mask) >> 10
        f_mask = data & fish_mask
        if seen[node][f_mask]:
            continue
        seen[node][f_mask] = True
        if (node == n) and (f_mask == all_fishes_mask):
            continue
        for nxt in neighbours[node]:
            nxt_mew_mask = cities[nxt] | f_mask
            if seen[nxt][nxt_mew_mask]:
                continue
            nxt_cur_time = trip_time[nxt][nxt_mew_mask]
            nxt_new_time = time + times[node][nxt]
            if (nxt_cur_time is not None) and (nxt_new_time >= nxt_cur_time):
                continue
            trip_time[nxt][nxt_mew_mask] = nxt_new_time
            heapq.heappush(q, (nxt_new_time << 20) + (nxt << 10) + nxt_mew_mask)
            
    rv = 0
    trip_times = trip_time[n]
    for mask_i, time_i in enumerate(trip_times):
        if not time_i:
            continue
        for data_j, time_j in enumerate(trip_times[mask_i:]):
            if not time_j:
                continue
            mask_j = mask_i + data_j
            mask = mask_i | mask_j
            t_time = max(time_i, time_j)
            if mask != all_fishes_mask:
                continue
            if rv and t_time >= rv:
                continue
            rv = t_time
    return rv


```