# Practice Links | 05 Feb


## Quadrant Queries

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;

public class Solution {
    private static final int[] BC = new int[1<<16];
    public static void main(String[] argv) throws Exception {
        prep();
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line1 = br.readLine();
        int N = Integer.parseInt(line1);
        ArrayList<String> dump = new ArrayList<String>(100000);
        int[] x = new int[N/32+1];
        int[] y = new int[N/32+1];
        long rs = System.currentTimeMillis();
        for(int i=0;i<N;i++){
            String line2 = br.readLine();
            String[] tmp2 = line2.split(" ");
            if(tmp2[0].charAt(0) != '-') x[i/32] |= 1<< i%32;
            if(tmp2[1].charAt(0) != '-') y[i/32] |= 1<< i%32;
        }
        long re = System.currentTimeMillis();
        String line3 = br.readLine();
        int Q = Integer.parseInt(line3);
        boolean wasC = false;
        int[] tmp1 = new int[N/32+1];
        int[] tmp24= new int[N/32+1];
        int[] tmp2 = new int[N/32+1];
        int[] cnt1 = new int[N/32+1];
        int[] cnt24= new int[N/32+1];
        int[] cnt2 = new int[N/32+1];
        long ws = System.currentTimeMillis();
        for(int i=0;i<Q;i++){
            String line4 = br.readLine();
            String[] tmp4 = line4.split(" ");
            int sindex = Integer.parseInt(tmp4[1]);
            int eindex = Integer.parseInt(tmp4[2]);
            int sm = (sindex-1)%32;
            int sn = (sindex-1)/32;
            int em = eindex%32;
            int en = eindex/32;
            int es = eindex-sindex+1;
            if(tmp4[0].equals("X")) {
                if(sn == en){
                    int mask = ((1<<(es))-1)<<(sm);
                    y[en] ^= mask;
                }else{
                    int mask = -1;
                    int fmask = mask<<(sm);
                    int emask = (1<<(em))-1;
                    y[sn] ^= fmask;
                    for(int j=sn+1;j<en;j++) y[j] ^= mask;
                    y[en] ^= emask;
                }
                wasC = false;
            }else if(tmp4[0].equals("Y")) {
                if(sn == en){
                    int mask = ((1<<(es))-1)<<(sm);
                    x[en] ^= mask;
                }else{
                    int mask = -1;
                    int fmask = mask<<(sm);
                    int emask = (1<<(em))-1;
                    x[sn] ^= fmask;
                    for(int j=sn+1;j<en;j++) x[j] ^= mask;
                    x[en] ^= emask;
                }
                wasC = false;
            }else{
                /*
                if(!wasC || wasC){
                    for(int j=0;j<x.length;j++) {
                        tmp1[j]  = x[j] & y[j];
                        tmp24[j] = x[j] ^ y[j];
                        tmp2[j]  = tmp24[j] & y[j];
                        cnt1[j] = bitCount(tmp1[j]);
                        cnt24[j]= bitCount(tmp24[j]);
                        cnt2[j] = bitCount(tmp2[j]);
                    }
                }
                */
                int maskes = ((1<<(es))-1)<<(sm);
                int maskall = -1;
                int fmask = maskall<<(sm);
                int emask = (1<<(em))-1;
                // 1st quadrant x bit: 1, y bit: 1 (x & y)
                int c1 = 0;
                if(sn == en){
                    c1 += bitCount(x[en] & y[en] & maskes);
                }else{
                    c1 += bitCount(x[sn] & y[sn] & fmask);
                    for(int j=sn+1;j<en;j++) c1 += bitCount(x[j] & y[j]);
                    c1 += bitCount(x[en] & y[en] & emask);
                }
                // 2nd quadrant x bit: 0, y bit: 1
                // 4th quadrant x bit: 1, y bit: 0
                // x xor y = c2 + c4
                // (x xor y) & y = c2
                int c24 = 0;
                int c2 = 0;
                if(sn == en){
                    int t2 = (x[en] ^ y[en]) & maskes;
                    c24 += bitCount(t2);
                    c2 += bitCount(t2 & y[en]);
                }else{
                    int t2 = (x[sn] ^ y[sn]) & fmask;
                    c24 += bitCount(t2);
                    c2 += bitCount(t2 & y[sn]);
                    for(int j=sn+1;j<en;j++) {
                        t2 = x[j] ^ y[j];
                        c24 += bitCount(t2);
                        c2 += bitCount(t2 & y[j]);
                    }
                    t2 = (x[en] ^ y[en]) & emask;
                    c24 += bitCount(t2);
                    c2 += bitCount(t2 & y[en]);
                }
                int c4 = c24 - c2;
                // 3rd quadrant x bit: 0, y bit: 0 (total - c1 - c2 - c4)
                int c3 = eindex - sindex + 1 - c1 - c2 - c4;
                dump.add(c1+" "+c2+" "+c3+" "+c4);
                //System.out.println(c1+" "+c2+" "+c3+" "+c4);
                wasC = true;
            }
        }
        long we = System.currentTimeMillis();
        for(int i=0;i<dump.size();i++) System.out.println(dump.get(i));
        br.close();
        //System.out.println("R:"+(re-rs));
        //System.out.println("W:"+(we-ws));
    }
    private static void prep() {
        int max = 1<<16;
        int step1 = 1<<8;
        for(int i=0;i<step1;i++) BC[i] = Integer.bitCount(i);
        for(int i=step1;i<max;i++){
            BC[i] = BC[i&0xFF] + BC[(i>>8)&0xFF];
        }
    }
    
    private static int bitCount(int i){
        return BC[i&0xFFFF] + BC[(i>>16)&0xFFFF];
    }
}
```

## Sparse Arrays

``` py
n = int(input())
hashmap = {}

for i in range(n):
    string = input()
    hashmap[string] = 1 if string not in hashmap else hashmap[string] + 1

q = int(input())

for j in range(q):
    string = input()
    print(0 if string not in hashmap else hashmap[string])
```

## Count Scorecards

```java
import java.io.*;
import java.util.*;

public class Solution {

  static final int MOD = 1_000_000_007;

  static class Solve {
    int[] exceed = new int[55];
    int numErased;
    int sCount;
    int scores;
    int dp[][][] = new int[42][42][42 * 41];
    int[][][] calced = new int[42][42][42 * 41];
    int calcedn;
    int[][] c = new int[55][55];

    void init() {
      for (int i = 0; i < 50; ++i) {
        c[i][0] = 1;
        for (int j = 1; j <= i; ++j) {
          c[i][j] = (c[i - 1][j] + c[i - 1][j - 1]) % MOD;
        }
      }
    }

    int calc(int k, int last, int sum) {
      if (k == numErased) {
        return (scores + sum == sCount * (sCount - 1) / 2) ? 1 : 0;
      }

      if (last >= sCount) {
        return 0;
      }

      int ans = dp[k][last][sum];

      if (calced[k][last][sum] == calcedn) {
        return ans;
      }
      calced[k][last][sum] = calcedn;

      ans = calc(k, last + 1, sum);
      int sumi = sum;
      for (int i = 1; k + i <= numErased; i++) {
        sumi += last;
        if (sumi + exceed[k + i] < (k + i) * (k + i - 1) / 2) {
          break;
        }

        ans = (int) ((ans + 1L * c[numErased - k][i] * calc(k + i, last + 1, sumi)) % MOD);
      }
      dp[k][last][sum] = ans;
      return ans;
    }

    int countScorecards(int[] s, int n, int sCount, int numErased) {
      this.sCount = sCount;
      this.numErased = numErased;

      Arrays.sort(s, 0, n);

      int sum = 0;
      for (int i = 0; i < n; ++i) {
        sum += s[i];
        if (i * (i + 1) / 2 > sum) {
          return 0;
        }
      }
      scores = sum;

      for (int i = 1; i <= numErased; ++i) {
        sum = 0;
        exceed[i] = 0;
        for (int j = 0; j < n; ++j) {
          sum += s[j] - (i + j);
          exceed[i] = Math.min(exceed[i], sum);
        }
      }
      calcedn++;
      return calc(0, 0, 0);
    }

  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    BufferedWriter bw = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

    StringTokenizer st = new StringTokenizer(br.readLine());
    int t = Integer.parseInt(st.nextToken());

    Solve solve = new Solve();
    solve.init();

    int[] s = new int[55];

    for (int it = 0; it < t; it++) {
      st = new StringTokenizer(br.readLine());
      int sCount = Integer.parseInt(st.nextToken());
      int n = 0;
      int numErased = 0;

      st = new StringTokenizer(br.readLine());

      for (int j = 0; j < sCount; j++) {
        int item = Integer.parseInt(st.nextToken());
        if (item == -1) {
          numErased++;
        } else {
          s[n++] = item;
        }
      }

      int result = solve.countScorecards(s, n, sCount, numErased);

      bw.write(String.valueOf(result));
      bw.newLine();
    }

    bw.close();
    br.close();
  }
}
```

## Highest Value Palindrome

```py
import math
import os
import random
import re
import sys

# Complete the highestValuePalindrome function below.
def highestValuePalindrome(s, n, k):
    min_no_of_changes = 0
    for i in range(n//2):
        if s[i] != s[n - i - 1]:
            min_no_of_changes += 1
            
    if min_no_of_changes > k:
        return '-1'
    
    highest_value_palindrome = ''
    for i in range(n//2):
        if k - min_no_of_changes > 1:
            if s[i] != s[n - i - 1]:
                if s[i] != '9' and s[n - i - 1] != '9':
                    highest_value_palindrome += '9'
                    k -= 2
                else:
                    if s[i] > s[n - i - 1]:
                        highest_value_palindrome += s[i]
                    else:
                        highest_value_palindrome += s[n - i - 1]
                    k -= 1
                min_no_of_changes -= 1
            elif s[i] != '9': # s[i] is equal to s[n - i - 1]:
                highest_value_palindrome += '9'
                k -= 2
            else:
                highest_value_palindrome += s[i]
        elif k - min_no_of_changes == 1:
            if s[i] != s[n - i - 1]:
                if s[i] != '9' and s[n - i - 1] != '9':
                    highest_value_palindrome += '9'
                    k -= 2
                else:
                    if s[i] > s[n - i - 1]:
                        highest_value_palindrome += s[i]
                    else:
                        highest_value_palindrome += s[n - i - 1]
                    k -= 1
                min_no_of_changes -= 1
            else:
                highest_value_palindrome += s[i]
        elif s[i] != s[n - i - 1]: # in this case min_no_of_changes must equal to or less than k
            if s[i] > s[n - i - 1]:
                highest_value_palindrome += s[i]
            else:
                highest_value_palindrome += s[n - i - 1]
            k -= 1
            min_no_of_changes -= 1
        else:
            highest_value_palindrome += s[i]

    if n&1:
        if k > 0:
            return highest_value_palindrome + '9' + highest_value_palindrome[::-1]

        return highest_value_palindrome + s[n//2] + highest_value_palindrome[::-1]
    
    return highest_value_palindrome + highest_value_palindrome[::-1]

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    nk = input().split()

    n = int(nk[0])

    k = int(nk[1])

    s = input()

    result = highestValuePalindrome(s, n, k)

    fptr.write(result + '\n')

    fptr.close()
```

## Maximum Palindromes

``` py
import math
import os
import random
import re
import sys
from collections import Counter, defaultdict
from math import factorial

fact = dict()
powr = dict()
dist = defaultdict(lambda : Counter(""))

m = 10 ** 9 + 7

def initialize(s):
    fact[0], powr[0], dist[0] = 1, 1, Counter(s[0])
    for j in range(1, len(s)):
        fact[j] = (j * fact[j - 1]) % m
        dist[j] = dist[j-1] + Counter(s[j])

def power(x, n, m):
    if n == 1:
        return x % m
    elif n % 2 == 0:
        return power(x ** 2 % m, n // 2, m)
    else:
        return (x * power(x ** 2 % m, (n - 1) // 2, m)) % m


def answerQuery(s, l, r):
    # Return the answer for this query modulo 1000000007.
    b = dist[r-1] - dist[l-2]
    p, count, value = 0, 0, 1
    for c in b.values():
        if c >= 2:
            count += c // 2
            value = (value * fact[c // 2]) % m
        if c % 2 == 1:
            p += 1
    return (max(1, p) * fact[count] * power(value, m - 2, m)) % m

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()

    initialize(s)
    
    print(dist)
    q = int(input().strip())

    for q_itr in range(q):
        first_multiple_input = input().rstrip().split()

        l = int(first_multiple_input[0])

        r = int(first_multiple_input[1])

        result = answerQuery(s,l, r)

        fptr.write(str(result) + '\n')

    fptr.close()
```

## Sherlock and Anagrams

```py
cases = int(input())
for caseNo in range(cases):
    s = input()
    n = len(s)
    res = 0
    for l in range(1, n):
        cnt = {}
        for i in range(n - l + 1):
            subs = list(s[i:i + l])
            subs.sort()
            subs = ''.join(subs)
            if subs in cnt:
                cnt[subs] += 1
            else:
                cnt[subs] = 1
            res += cnt[subs] - 1
    print(res)
```


## Common Child

```py
import os

# Complete the commonChild function below.
def commonChild(s1, s2):
  maxAt = {}

  for i1 in range(len(s1)):
    maxForI1 = 0
    for i2 in range(len(s2)):
      potentialSum = maxForI1 + 1

      # You might be tempted to use the max() function to simplify the next three lines,
      # but that makes the solution so much slower that several of the test cases fail.
      other = maxAt.get(i2, 0)
      if other > maxForI1:
        maxForI1 = other

      if s1[i1] == s2[i2]:
        maxAt[i2] = potentialSum

  return max(maxAt.values(), default=0)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s1 = input()

    s2 = input()

    result = commonChild(s1, s2)

    fptr.write(str(result) + '\n')

    fptr.close()
```

## Bear and Steady Gene

```py
from collections import Counter
import sys
import math

n = int(input())
s1 = input()
s = Counter(s1)

if all(e <= n/4 for e in s.values()):
    print(0)
    sys.exit(0)

result = float("inf")
out = 0
for mnum in range(n):
    s[s1[mnum]] -= 1
    while all(e <= n/4 for e in s.values()) and out <= mnum:
        result = min(result, mnum - out + 1)
        s[s1[out]] += 1
        out += 1

print(result)
```