# Practice Contest | 12 Feb

## Candies

```py
N = int(input())
a = []
while N>0:
	a.append(int(input()))
	N -= 1
N = len(a)
left, right, num = [[0 for i in range(N)] for j in range(3)]
p = 1
while p<N:
	if a[p] > a[p-1]:
		left[p] = left[p-1] + 1
	p += 1
p = N-2
while p>=0:
	if a[p] > a[p+1]:
		right[p] = right[p+1] + 1
	p -= 1
p = 0
while p<N:
	num[p] = 1 + max(left[p], right[p])
	p += 1

print(sum(num))
```

## Sherlock and The Beast
```py
def decent_number(N):
    """
    Prints a decent number of N digits. -1 if no such number exists.
    """
    
    for fives in range(N, -1, -1):
        threes = N - fives
        if fives % 3 == 0 and threes % 5 == 0:
            return "5" * fives + "3" * threes
    return "-1"
    
def main():
    
    import sys
    
    count, *Ns = sys.stdin.readlines()
    
    for N in Ns:
        print(decent_number(int(N)))
    
if __name__ == "__main__":
    main()
```

## Priyanka and Toys
```py
import sys

N = int(sys.stdin.readline())

a = list(sys.stdin.readline().split())
for index, item in enumerate(a):
    a[index] = int(item)

a = sorted(a)

count = 0
i = 0
while i < N:
    temp = int(a[i]) + 4
    count+=1
    while i < N and int(a[i]) <= temp:
        i+=1

print (count)
```

## Largest Permutation
```py
import sys


if __name__ == '__main__':
    N, K = list(map(int, sys.stdin.readline().split()))
    A = list(map(int, sys.stdin.readline().split()))
    
    if K >= N - 1:
        print(*sorted(A, reverse = True), sep = ' ')
    
    else:
        X = sorted(A)
        i, swaps = 0, 0
        
        while swaps < K:
            x = X.pop()
            
            if A[i] != x:
                A[A.index(x)] = A[i]
                A[i] = x
                swaps += 1
            
            i += 1
        
        print(*A, sep = ' ')
```

## Mark and Toys
```py
def maximumToys(prices, k):
    items = 0
    prices.sort()
    for p in prices:
        if p <= k:
            items += 1
            k -= p
        else:
            break
    return items
```

## Greedy Florist
```py
N, k = [int(i) for i in input().split(' ')]
ci = [int(i) for i in input().split(' ')] 

ci.sort()

if N<len(ci):
	N = len(ci)

totalCount, perPerson, curRound, totalAmount = 0, 0, 0, 0
pFlower = len(ci) - 1
while totalCount < N:
	totalAmount += ci[pFlower]*(perPerson+1)
	
	curRound += 1
	if curRound == k:
		curRound = 0
		perPerson += 1
	totalCount += 1
	pFlower -= 1

print(totalAmount)
```

## Angry Children 2
```py
def calc_angry_val(arr, start, k):
    angry_val = 0
    for i in range(k):
        angry_val = angry_val + nrs[start + i] * i - nrs[start + i] * (k - 1 - i)
    return angry_val

n = int(input())
k = int(input())

nrs = sorted(int(input()) for _ in range(n))

sums = [0] * (n + 1)
for i in range(n):
    sums[i + 1] = sums[i] + nrs[i]

# Let's select the first block of k candies and compute the angry_val
angry_val = calc_angry_val(nrs, 0, k)
result = angry_val

# Now if we proceed, shifting out the left value x_left removes (k - 1) * x_left
# And shifting in the new value x_right adds (k - 1) * x_right
for i in range(k, n):
    angry_val += (k - 1)  * nrs[i - k]
    angry_val += (k - 1)  * nrs[i]
    angry_val -= 2 * (sums[i] - sums[i - k + 1])
    result = min(result, angry_val)

print(result)
```

## Jim and the Orders
```py
n = int(input())
a = [(tuple(map(int, input().split()))) for _ in range( n )]
print(" ".join(list(map(str, [x[0] for x in sorted([(x[0], x[1] + x[2]) for x in [(i + 1, a[i][0], a[i][1]) for i in range(n)] ] , key=lambda x: x[1]) ] ))))
```

## Permuting Two Arrays
```py
def rl(T=str):
    return list(map(T,input().split()))

T, = rl(int)
for _ in range((T)):
    N,K = rl(int)
    A = rl(int)
    B = rl(int)
    A.sort()
    B.sort(reverse=True)
    bad = len([a+b for a,b in zip(A,B) if a+b<K ])>0
    print("NO" if bad else "YES")
```

## Cutting Boards
```py
import heapq

def cuts_cost(y, x):
    heapq.heapify(y)
    heapq.heapify(x)

    hori_segs = 1
    vert_segs = 1
    total = 0
    while y and x:
        cost_y = heapq.heappop(y)
        cost_x = heapq.heappop(x)

        if (cost_y < cost_x) or (cost_y == cost_x and vert_segs <= hori_segs):
            heapq.heappush(x, cost_x)
            highest = cost_y
            total += hori_segs * highest
            vert_segs += 1
        else:
            heapq.heappush(y, cost_y)
            highest = cost_x
            total += vert_segs * highest
            hori_segs += 1

    total += hori_segs * sum(y)
    total += vert_segs * sum(x)

    return -total % (10**9 + 7)


num_tests = int(input().strip())
for test in range(num_tests):
    m, n = tuple(int(i) for i in input().strip().split(" "))
    costs_y = [-int(i) for i in input().strip().split(" ")]
    costs_x = [-int(i) for i in input().strip().split(" ")]
    print(cuts_cost(costs_y, costs_x))

```