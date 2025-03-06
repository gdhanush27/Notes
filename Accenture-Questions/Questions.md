# AbsoluteDifference.java 
 ```java 
/*
You are given a function,
int findCount(int arr[], int length, int num, int diff);

The function accepts an integer array ‘arr’, its length and two integer variables ‘num’ and ‘diff’. Implement this function to find and return the number of elements of ‘arr’ having an absolute difference of less than or equal to ‘diff’ with ‘num’.
Note: In case there is no element in ‘arr’ whose absolute difference with ‘num’ is less than or equal to ‘diff’, return -1.

Example:
Input:

arr: 12 3 14 56 77 13
num: 13
diff: 2
Output:
3

Explanation:
Elements of ‘arr’ having absolute difference of less than or equal to ‘diff’ i.e. 2 with ‘num’ i.e. 13 are 12, 13 and 14.

*/


import java.util.Scanner;
public class AbsoluteDifference {

    public static int AbsDifference(int arr[], int length, int num, int diff){

        int count = 0;
        for(int i = 0; i < length; i++){
            if(Math.abs(num - arr[i]) <= 2){
                count++;
            }
        }

        return count > 0 ? count : -1;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); 

        System.out.println("Enter size of arr: ");
        int n = sc.nextInt ();
        
        int arr[] = new int[n];
        System.out.println("Enter elements: ");
        for (int i = 0; i < n; i++){
            arr[i] = sc.nextInt ();
        }

        System.out.println("Enter num: ");
        int num = sc.nextInt ();

        System.out.println("Enter difference: ");        
        int diff = sc.nextInt ();

        System.out.println ("Absolute Diff count: " + AbsDifference(arr, n, num, diff));
    }
}

 ``` 

# Anagram.java 
 ```java 
/*
You are given two strings, s and t . Your task is to determine if it's 
possible to rearrange the characters of s to form the string t . 
Write a function that returns True it's possible to create t by 
rearranging the characters of s and False otherwise. 

Input 
Two strings, s and t where the length of s and t are between 1 and 
1000 characters. 

Output 
Return True if it's possible to create t by rearranging the characters of 
s and False otherwise 

Example: 
s="listen" 
t="silent" 

Output: 
True

*/

import java.util.*;

public class Anagram{

    public static boolean CheckAnagram(String s, String t){

        s = s.toLowerCase();
        t = t.toLowerCase();

        char []arr1 = s.toCharArray(); 
        char []arr2 = t.toCharArray(); 

        Arrays.sort(arr1); // e,i,l,n,s,t 
        Arrays.sort(arr2); // e,i,l,n,s,t 

        if(Arrays.equals(arr1,arr2)){ 
            return true;
        }else{ 
            return false;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter first string: ");
        String s=sc.nextLine(); // Silent 

        System.out.println("Enter second string: ");
        String t=sc.nextLine(); // listen 

        System.out.println("Output: " + CheckAnagram(s, t));
    }
}

 ``` 

# AutobiographicalNo.cpp 
 ```cpp 
/*

Autobiographical Number

Problem Statement :

An Autobiographical Number is a number N such that the first digit of N represents the count of how many zeroes are there in N, the second digit represents the count of how many ones are there in N and so on.

You are given a function, def FindAutoCount(n):

The function accepts string “n” which is a number and checks whether the number is an autobiographical number or not. If it is, an integer is returned, i.e. the count of distinct numbers in ‘n’. If not, it returns 0.

Assumption:

The input string will not be longer than 10 characters.
Input string will consist of numeric characters.
Note:

If string is None return 0.

Example:

Input:

n: “1210”

Output:

3

Explanation:

0th position in the input contains the number of 0 present in input, i.e. 1, in 1st position the count of number of 1s in input i.e. 2, in 2nd position the count of 2s in input i.e. 1, and in 3rd position the count of 3s i.e. 0, so the number is an autobiographical number.

Now unique numbers in the input are 0, 1, 2, so the count of unique numbers is 3. So 3 is returned.

*/


#include <iostream>
#include<bits/stdc++.h>
using namespace std;
int FinndAutoCount (string n)
{
    int sum = 0;
    set<char> st;
    for (int i = 0; i < n.size (); i++){
        sum += (n[i] - '0');    // converting the string character into integer value and adding it to sum
        st.insert (n[i]);
    }

    if (sum != n.size ())
        return 0;

    return st.size ();
}

int main (){
  string n;

  cout<<"Enter no: "<<endl;
  cin >> n;

  cout <<"Result: "<< FinndAutoCount (n);
  return 0;
}

 ``` 

# BinaryOperations.java 
 ```java 
/*
Problem Description :
The Binary number system only uses two digits, 0 and 1 and number system can be called binary string. You are required to implement the following function:

int OperationsBinaryString(char* str);

The function accepts a string str as its argument. The string str consists of binary digits eparated with an alphabet as follows:

– A denotes AND operation
– B denotes OR operation
– C denotes XOR Operation
You are required to calculate the result of the string str, scanning the string to right taking one opearation at a time, and return the same.

Note:

– No order of priorities of operations is required
– Length of str is odd
– If str is NULL or None (in case of Python), return -1

Input:
str: 1C0C1C1A0B1

Output:
1

Explanation:
The alphabets in str when expanded becomes “1 XOR 0 XOR 1 XOR 1 AND 0 OR 1”, result of the expression becomes 1, hence 1 is returned.

Sample Input:
0C1A1B1C1C1B0A0

Output:
0

*/


import java.util.*;
public class BinaryOperations {

    public static int OperationsBinaryString(String str){
        if(str == null) return 0;

        int result = str.charAt(0) - '0';

        for(int i = 1; i < str.length(); i += 2){
            char operation = str.charAt(i);
            int nextDigit = str.charAt(i+1) - '0';

            switch(operation){
                case 'A':
                    result = result & nextDigit;
                    break;
                case 'B':
                    result = result | nextDigit;
                    break;
                case 'C':
                    result = result ^ nextDigit;
                    break;
                default:
                    return -1;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String str = sc.next();
        System.out.println(OperationsBinaryString(str));
        sc.close();
    }
}
 ``` 

# BinaryToDec.java 
 ```java 
/*
Problem Statement 

Convert binary no to decimal

Input: 1010
Output: 10

*/


import java.util.*;

public class BinaryToDec{
    public static int decTobin(int n) {
        if (n == 0) {
            return 0;
        }

        int ans = 0;
        int base = 1; // This represents the place value (1, 10, 100, ...)

        while (n > 0) {
            int lastBit = n % 10; // Get the last bit (either 0 or 1)
            ans += lastBit * base; // Add it to the current base value
            base *= 2; // Move to the next place value (1 -> 10 -> 100, etc.)
            n /= 10; // Right shift n by 1 (equivalent to n = n / 2)
        }
        
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the the decimal number: ");
        int n = sc.nextInt();

        System.out.println("Output: "+ decTobin(n));
    }
}

 ``` 

# BulbSwitch.java 
 ```java 
/*
Problem Statement :

N light bulbs are connected by a wire. Each bulb has a switch associated with it, however due to faulty wiring, a switch also changes the state of all the bulbs to the right of current bulb. Given an inital state of all bulbs, Find the minimum number of switches you have to press to turn on all the bulbs. You can press the same switch multiple times.

Note: 0 represents the bulb is off and 1 represents the bulb is on.

Note: A[] = [0 1 0 1]
Output: 4

Explanation:
Press switch 0: [1 0 1 0] //1
Press switch 1: [1 1 0 1] //2
Press switch 2: [1 1 1 0] //3
Press switch 3: [1 1 1 1] //4

Input: A[] = [1 0 0 0 0]
Output: 1

*/



import java.util.*;
public class BulbSwitch
{
    public static int BulbSwitch(int arr[], int n)
    {
        int count = 0;
        for(int i = 0; i < n; i++){
            if(arr[i] == 0){
                arr[i] = 1;
                for(int j = i+1; j < n; j++){
                    if(arr[j] == 1){
                        arr[j] = 0;
                    }else{
                        arr[j] = 1;
                    }
                }
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int arr[] = {0,1,0,1};
        int n = arr.length;

        System.out.println("Minimum no of switches to press: " + BulbSwitch(arr, n));
    }
} 

 ``` 

# ChocolateDistribution.java 
 ```java 
/*
Given an array of N integers where each value represents the number of chocolates in a packet. Each packet can have a variable number of chocolates. There are m students, the task is to distribute chocolate packets such that: 

Each student gets one packet.
The difference between the number of chocolates in the packet with maximum chocolates and the packet with minimum chocolates given to the students is minimum.
Examples:

Input : arr[] = {7, 3, 2, 4, 9, 12, 56} , m = 3 
Output: Minimum Difference is 2 
Explanation:
We have seven packets of chocolates and we need to pick three packets for 3 students 
If we pick 2, 3 and 4, we get the minimum difference between maximum and minimum packet sizes.

Input : arr[] = {3, 4, 1, 9, 56, 7, 9, 12} , m = 5 
Output: Minimum Difference is 6 

Input : arr[] = {12, 4, 7, 9, 2, 23, 25, 41, 30, 40, 28, 42, 30, 44, 48, 43, 50} , m = 7 
Output: Minimum Difference is 10 

*/



import java.util.*;
public class ChocolateDistribution {

    public static int chocolateDistribution (int arr[], int m)
    {
        if(arr.length == 0 || m == 0){
            return 0;
        }

        Arrays.sort(arr);

        if(m > arr.length-1){
            return -1;
        }

        int minDiff = Integer.MAX_VALUE;

        for(int i = 0; i < arr.length; i++){
            int j = i + m - 1;

            if(j >= arr.length){
                break;
            }

            int diff = arr[j] - arr[i];
            minDiff = Math.min(minDiff, diff);
        }
        return minDiff;

    }

    public static void main(String[] args) {
        int arr[] = {12, 4, 7, 9, 2, 23, 25, 41, 30, 40, 28, 42, 30, 44, 48, 43, 50};
        int m = 7;
 
        int result = chocolateDistribution(arr, m);
 
        if (result != -1) {
            System.out.println("Minimum difference is " + result);
        } else {
            System.out.println("Invalid input");
        }
    }
}

 ``` 

# CountCarry.cpp 
 ```cpp 
/*

Problem Statement           (Asked in Accenture Offcampus 1 Aug 2021, Slot 2)

A carry is a digit that is transferred to left if sum of digits exceeds 9 while adding two numbers from right-to-left one digit at a time

You are required to implement the following function.

Int NumberOfCarries(int num1 , int num2);

The functions accepts two numbers ‘num1’ and ‘num2’ as its arguments. You are required to calculate and return  the total number of carries generated while adding digits of two numbers ‘num1’ and ‘ num2’.

Assumption: num1, num2>=0

Example:

Input
Num 1: 451
Num 2: 349
Output
2
Explanation:

Adding ‘num 1’ and ‘num 2’ right-to-left results in 2 carries since ( 1+9) is 10. 1 is carried and (5+4=1) is 10, again 1 is carried. Hence 2 is returned.

Sample Input

Num 1: 23

Num 2: 563

Sample Output

0

*/


#include <iostream>
using namespace std;
int CountCarry(int no1, int no2){

    int carry = 0, count = 0, sum = 0;

    while (no1 != 0 || no2 != 0) {
        int val1 = no1 % 10;
        int val2 = no2 % 10;

        sum = carry + val1 + val2;

        if (sum > 9) {
            carry = 1;
            count++;
        } else {
            carry = 0;
        }

        no1 = no1 / 10;
        no2 = no2 / 10;
    }
    return count;
}

int main()
{
	int x, y;
	int result;

    cout<<"Enter first no: "<<endl;
	cin >> x;

    cout<<"Enter second no: "<<endl;
	cin >> y;

	result = CountCarry(x, y);
	cout <<"Result: "<<result;

	return 0;
}


 ``` 

# DecToBinary.java 
 ```java 
/*
Problem Statement 

Convert decimal no to binary

Input: 10
Output: 1010

*/


import java.util.*;

public class DecToBinary{
    public static String decbin(int n){
        if(n == 0){
            return "0";
        }

        String ans = "";
        while (n > 0) {
            if ((n & 1) == 1) {
                ans = "1" + ans;  
            } else {
                ans = "0" + ans;  
            }
            n = n >> 1;  
        }
        
        
        return ans;
    }

    // return type: int
    public static int decTobin(int n) {
        if (n == 0) {
            return 0;
        }

        int ans = 0;
        int place = 1; // This represents the place value (1, 10, 100, ...)

        while (n > 0) {
            int lastBit = n & 1; // Get the last bit (either 0 or 1)
            ans += lastBit * place; // Add it to the current place value
            place *= 10; // Move to the next place value (1 -> 10 -> 100, etc.)
            n = n >> 1; // Right shift n by 1 (equivalent to n = n / 2)
        }
        
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the the decimal number: ");
        int n = sc.nextInt();

        System.out.println("Output: "+ decTobin(n));
    }
}

 ``` 

# DisplayPalindrome.java 
 ```java 
/*
Question: Write a program in C such that it takes a lower limit and upper limit as inputs and print all the intermediate palindrome numbers.

Test Cases:

TestCase 1:
Input :
10 , 80
Expected Result:
11 , 22 , 33 , 44 , 55 , 66 , 77.

Test Case 2:
Input:
100,200
Expected Result:
101 , 111 , 121 , 131 , 141 , 151 , 161 , 171 , 181 , 191.

*/


import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;
public class DisplayPalindrome {

    public static int palindrome (int no1)
    {
        int rem = 0;
        int div = no1;
        while (div != 0)
        {
	        int r = div % 10;
	        rem = (rem * 10) + r;
	        div = div / 10;
        }
        return rem;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner (System.in);

        System.out.println ("Enter Upper and Lower Limit");
        int ul = sc.nextInt ();
        int ll = sc.nextInt ();
        
        for (int i = ul; i <= ll; i++){
	        if (i == palindrome (i))
                System.out.print(i+" ");
        }
    }
}

 ``` 

# Distance.py 
 ```py 
'''

Ques: The program is supposed to calculate the sum of  distance between three points from each other.

For
x1 = 1 y1 = 1
x2 = 2 y2 = 4
x3 = 3 y3 = 6

Distance is calculated as : sqrt(x2-x1)2 + (y2-y1)2

'''


import math

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

def total_distance(x1, y1, x2, y2, x3, y3):
    first_diff = calculate_distance(x1, y1, x2, y2)
    second_diff = calculate_distance(x2, y2, x3, y3)
    third_diff = calculate_distance(x1, y1, x3, y3)
    
    return round(first_diff, 2), round(second_diff, 2), round(third_diff, 2)

def main():
    x1, y1 = map(float, input("Enter coordinates for point 1 (x1 y1): ").split())
    x2, y2 = map(float, input("Enter coordinates for point 2 (x2 y2): ").split())
    x3, y3 = map(float, input("Enter coordinates for point 3 (x3 y3): ").split())
    
    first_diff, second_diff, third_diff = total_distance(x1, y1, x2, y2, x3, y3)
    print("Distances:")
    print(f"Between point 1 and point 2: {first_diff}")
    print(f"Between point 2 and point 3: {second_diff}")
    print(f"Between point 1 and point 3: {third_diff}")

if __name__ == "__main__":
    main()

 ``` 

# ElementOccurences.java 
 ```java 
/*

GIven an array, find the number of occurences of each element in the array.

Sample Test Case 2:
Input:
arr[] = {10,5,10,15,10,5}

Output:
10 - 3
5 - 2
15 - 1

*/

import java.util.HashMap;

public class ElementOccurences {
    public static HashMap<Integer, Integer> Occurence(int[] array) {
        HashMap<Integer, Integer> occu = new HashMap<>();

        for(int elem : array){
            if(occu.containsKey(elem)){
                occu.put(elem, occu.get(elem) + 1);
            }
            else{
                occu.put(elem, 1);
            }
        }
        return occu;
    }

    public static void main(String[] args) {
        int arr[] = {10, 5, 10, 15, 10, 5};
        HashMap<Integer, Integer> result = Occurence(arr);

        for (int key : result.keySet()) {
            System.out.println(key + " - " + result.get(key));
        }
    }
}

 ``` 

# ElevationPoint.java 
 ```java 
/*
Problem Statement :

Input : N = 7, arr = [1,2,3,4,3,2,1]
Output: 4   

Explanation: 4 is the elevation point

Input: N = 2, arr = [5,3]
Output: 5

*/



import java.util.*;
public class ElevationPoint
{
    public static int elevation(int arr[], int n) {
        if(n == 1) return arr[0];

        if(arr[0] > arr[1]){
            return arr[0];
        }
        if(arr[n-1] > arr[n-2]){
            return arr[n-1];
        }

        int low = 1, high = n-2;
        while(low <= high){
            int mid = low + (high - low) / 2;
            if((arr[mid] > arr[mid-1]) && (arr[mid] > arr[mid+1])){
                return arr[mid];
            }
            else if(arr[mid-1] < arr[mid]){
                low = mid + 1;
            }
            else{
                high = mid - 1;
            }
        }
        return -1;
    }



    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter no of elements in array: ");
        int n = sc.nextInt();
        
        System.out.println("Enter the elements of array: ");
        int arr[] = new int[n];
        for(int i = 0; i < n; i++){
            arr[i] = sc.nextInt();
        }

        System.out.println("Elevation point is: " + elevation(arr, n));
        
    }
} 

 ``` 

# EncodeNumber.java 
 ```java 
/*

Encode the Number: 
You work in the message encoding department of a national security 
message agency. Every message that is sent from or received in your 
office is encoded. You have an integer N and each digit of N is squared 
and the squares are concatenated  together to encode the original 
number. Your task is to find and return an integer value representing 
the encoded value of the number. 

Input Specification: 
input1: An integer value N representing the number to be encoded. 

Explanation: 
Output Specification: 
Return an integer value representing the encoded value of the number.

Example 1: 
input1: 34 
Output: 916 

Here, the given integer is 34, and the square its digit are: 
3^2= 9 
4²=16 

*/



import java.util.Scanner;

public class EncodeNumber {

    public static int Encode(int n) {
        String ans = "";

        while(n != 0){
            int last = n % 10;
            ans = (last*last) + ans;
            n = n / 10; 
        }

        return Integer.parseInt(ans);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Input the number of terms
        System.out.println("Enter number:");
        int n = sc.nextInt();

        System.out.println("Encoded number is: " + Encode(n));
    }
}

 ``` 

# EquilibriumSum.java 
 ```java 
/*
Problem Statement :

Given the function accepts an integer arr of size n as its argument. The function needs to return the index of equiibrium point int ht array, where the sum of elements on the left of the index is equal to the sum of elements on the right of the index. If no equilibrium point exists, the function should return -1.

Input arr: {3,4,3,1,6}
Output: 2   

Explanation: 3+4 = 7 and 1+6 = 7 so 3 is the equilibrium point having index 2.

*/



import java.util.*;
public class EquilibriumSum
{
    public static int equilibrium(int arr[]) 
    {
        int n = arr.length;
        int leftsum = 0, rightsum = 0;
        int total = 0;

        for(int i = 0; i < n; i++) {
            total += arr[i];
        }
        for(int i = 0; i < n; i++){
            rightsum = total - arr[i] - leftsum;
            if(leftsum == rightsum){
                return i;
            }
            leftsum += arr[i];
        }
        return -1;
    }



    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter no of elements in array: ");
        int n = sc.nextInt();
        
        System.out.println("Enter the elements of array: ");
        int arr[] = new int[n];
        for(int i = 0; i < n; i++){
            arr[i] = sc.nextInt();
        }

        System.out.println("Equilibrium Index is: " + equilibrium1(arr));
        
    }
} 

 ``` 

# fibonacciSeries.java 
 ```java 
/*
Problem Statement :

Print the fibonacci series.

*/



import java.util.Scanner;

public class fibonacciSeries {

    // Function to print the Fibonacci series up to n terms
    public static void printFibonacciSeries(int n) {
        int num1 = 0, num2 = 1;

        System.out.print("Fibonacci Series: " + num1 + ", " + num2);

        for (int i = 2; i < n; i++) {
            int num3 = num1 + num2;
            System.out.print(", " + num3);
            num1 = num2;
            num2 = num3;
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Input the number of terms
        System.out.println("Enter the number of terms:");
        int n = sc.nextInt();

        // Print the Fibonacci series
        printFibonacciSeries(n);
    }
}

 ``` 

# FindMissingElemArray.py 
 ```py 
# Given an array of integers, write a function that finds the missing number.
# Input: [1,2,4,5,6]
# Output: 3

def FindMissing(arr):
    n = len(arr) + 1        # Total number of elements including the missing one
    TotalSum = n * (n+1) // 2       # Sum of the first n natural numbers
    
    ActualSum = 0
    for i in range(len(arr)):
        ActualSum += arr[i]
        
    return TotalSum - ActualSum


def main():
    arr = [1,2,4,5,6]
    print("Missing number in array is: ", FindMissing(arr))
    

if __name__ == "__main__":
    main()
 ``` 

# FirstKWords.java 
 ```java 
/*
Problem Statement :

Print the first K words of the string.

Input: Hello I am a passionate developer
       k = 4

Output: Hello I am a

*/



import java.util.Scanner;

public class FirstKWords {

    public static String firstKWords(String str,int k) {
        String words[] = str.split("\\s+");

        if(k > words.length){
            return str;
        }

        StringBuilder result = new StringBuilder();

        for(int i = 0; i < k; i++){
            result.append(words[i]);
            if(i < k-1){
                result.append(" ");
            }
        }
        return result.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter String: ");
        String str = sc.nextLine();

        // Input the number of terms
        System.out.println("Enter value of K:");
        int k = sc.nextInt();

        // Print the Fibonacci series
        System.out.println("The first K words are: "+ firstKWords(str,k));
    }
}

 ``` 

# FloydsTriangle.java 
 ```java 
/*
You have been given an integer N as input . your task is to write a 
program to print N rows of Floyad’s Triangle. Floyd's pattern is a right- 
angled triangular array of natural numbers , used for the numbering of 
lines In a printout 
. 
For N=4, 
1 
23 
456 
78910 

*/



import java.util.Scanner;

public class FloydsTriangle {

    public static void Floyd(int n) {
        int k = 0;
        for(int i = 1; i <= n; i++){
            for(int j = 1; j <= i; j++){
                k++;
                System.out.print(k + " ");
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Input the number of terms
        System.out.println("Enter N:");
        int n = sc.nextInt();

        // Print the Fibonacci series
        Floyd(n);
    }
}

 ``` 

# GooglyPrimeNo.java 
 ```java 
/*
Problem Statement 

A number whose sum of digits is prime. 

Input: 43
Output: YES (4+3 = 7)

Input: 123
Output: NO (1+2+3 = 6)

*/


import java.util.*;

public class GooglyPrimeNo{

    public static boolean isPrime(int n){
        if(n <= 1)
            return false;
        
        for(int i = 2; i <= n/2; i++){
            if(n % i == 0){
                return false;
            }
        }
        return true;
    }

    public static String googlyPrime(int n) {
        int sum = 0;
        while (n > 0) {
            int lastDigit = n % 10; 
            sum += lastDigit; 
            n /= 10; 
        }
        if (isPrime(sum)) {
            return "YES";
        }
        return "NO";
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the the decimal number: ");
        int n = sc.nextInt();

        System.out.println("Output: "+ googlyPrime(n));
    }
}

 ``` 

# IntersectionOfArray.java 
 ```java 
import java.util.*;
public class IntersectionOfArray {

    public static List<Integer> Intersection(int arr1[], int arr2[]){
        int i = 0, j = 0;
        List<Integer> ans = new ArrayList<>();

        while(i < arr1.length && j < arr2.length){
            if(arr1[i] == arr2[j]){
                ans.add(arr1[i]);
                i++;
                j++;
            }
            else if(arr1[i] < arr2[j]){
                i++;
            }
            else{
                j++;
            }
        }
        return ans;
    }


    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); 
        int[] arr1 = {1, 2, 2, 3, 4};
        int[] arr2 = {2, 2, 3, 5};
        List<Integer> result = Intersection(arr1, arr2);
        
        for (int num : result) {
            System.out.print(num + " ");
        }
    }
}
 ``` 

# LargeSmallSum.java 
 ```java 
/*
You are required to implement the following Function 

def LargeSmallSum(arr)

The function accepts an integers arr of size ’length’ as its arguments you are required to return the sum of second largest  element from the even positions and second smallest from the odd position of given ‘arr’

Assumption:
All array elements are unique
Treat the 0th position as even

NOTE
Return 0 if array is empty
Return 0, if array length is 3 or less than 3

Example

Input
arr:3 2 1 7 5 4

Output
7

Explanation

Second largest among even position elements(1 3 5) is 3
Second smallest among odd position element is 4
Thus output is 3+4 = 7
Sample Input

arr:1 8 0 2 3 5 6

Sample Output

8

*/


import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;
public class LargeSmallSum {

    public static int largeSmallSum(int[]arr, int n){
        if (arr == null || n <= 3) {
            return 0;
        }

        ArrayList<Integer> even = new ArrayList<Integer>();
        ArrayList<Integer> odd = new ArrayList<Integer>();

        for (int i = 0; i < n; i++) {
            if (i % 2 == 0)
                even.add(arr[i]);
            else
                odd.add(arr[i]);
        }

        Collections.sort(even);
        Collections.sort(odd);

        return even.get(even.size() - 2) + odd.get(1);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); 

        System.out.println("Enter size of arr: ");
        int n = sc.nextInt ();

        int arr[] = new int[n];
        System.out.println("Enter elements: ");

        for (int i = 0; i < n; i++)
            arr[i] = sc.nextInt ();

        System.out.println ("Sum: " + largeSmallSum(arr, n));
    }
}

 ``` 

# LengthLastWord.java 
 ```java 
/*
Problem Statement 

Given a string S consisting of words and spaces, return the lenght of the last word in the string.

Input: "  I am  a passionate   Developer  "
Output: 9

*/


import java.util.*;

public class LengthLastWord{
    public static int LengthLast(String s){
        String arr[] = s.split(" ");
        
        int n = arr.length;
        String s1 = arr[n-1];

        return s1.length();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter string : ");
        String s = sc.nextLine();

        System.out.println("Output: "+ LengthLast(s));
    }
}

 ``` 

# LinkedListPalindrome.java 
 ```java 
/*
Problem Statement 

Given the head of a singly linked lsit, retun true if it is a plaindrome or false otherwise.

Input: head = [1, 2, 2, 1]
Output: true

*/

import java.util.*;

public class LinkedListPalindrome {

    public static Node head;
    public static Node tail;

    public static class Node {
        int data;
        Node next;

        Node(int data) {
            this.data = data;
            this.next = null;
        }
    }

    // Method to reverse the linked list
    public static Node reverse(Node head) {
        Node curr = head;
        Node prev = null;
        Node next = null;

        while (curr != null) {
            next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }

    // Method to check if the linked list is a palindrome
    public static boolean isPalindrome(Node head) {
        if (head == null || head.next == null) {
            return true; // Single node or empty list is always a palindrome
        }

        Node slow = head;
        Node fast = head;

        // To find the middle of the linked list
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        // Reverse the second half of the linked list
        Node revHead = reverse(slow); // Reverse the second half from the middle
        Node curr = head;

        // Compare the first half with the reversed second half
        while (revHead != null) {
            if (curr.data != revHead.data) {
                return false;
            }
            curr = curr.next;
            revHead = revHead.next;
        }
        return true;
    }

    // Method to add nodes to the linked list
    public static void addNode(int data) {
        Node newNode = new Node(data);
        if (head == null) {
            head = newNode;
            tail = newNode;
        } else {
            tail.next = newNode;
            tail = newNode;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter the number of elements in the linked list: ");
        int n = sc.nextInt();

        System.out.println("Enter the elements of the linked list:");
        for (int i = 0; i < n; i++) {
            int element = sc.nextInt();
            addNode(element);
        }

        if (isPalindrome(head)) {
            System.out.println("The linked list is a palindrome.");
        } else {
            System.out.println("The linked list is not a palindrome.");
        }

        sc.close();
    }
}

 ``` 

# LongestSubstring.java 
 ```java 
/*

Given a string s, find the length of the longest 
substring without repeating characters.

Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.


*/


import java.util.*;
public class LongestSubstring {

    public static int Longest(String s){
        Set<Character> set = new HashSet<>();

        int maxLength = 0;
        int start = 0, end = 0;

        while (start < s.length()) {
            if (!set.contains(s.charAt(start))) {
                set.add(s.charAt(start));
                maxLength = Math.max(maxLength, start - end + 1);
                start++;
            } else {
                set.remove(s.charAt(end));
                end++;
            }
        }
        return maxLength;
    }


    public static void main(String[] args) {
    Scanner sc = new Scanner(System.in); 
        
        System.out.println("Enter string: ");
        String str = sc.nextLine();

        System.out.println("Output: " + Longest(str));

    }
}
 ``` 

# LongestWord.java 
 ```java 
/*

Rohan is a kid who has just learned about creating words from 
alphabets. He has written some words in the notepad of his Father 
laptop. Now his father wants to find the longest word written by Rohan 
using a computer program. Write a program to find the longest string 
in a given list of strings. 

Example: 
Input: yes no number 
Output: The longest string is: number

*/



import java.util.Scanner;

public class LongestWord {

    public static String longestWord(String s) {
        s = s.trim();
        s = s.replaceAll("\\s+", " ");
        String arr[] = s.split(" ");

        int max = 0;
        String longest = "";
        for(int i = 0; i < arr.length; i++){
            if(arr[i].length() > max){
                max = arr[i].length();
                longest = arr[i];
            }
        }
        return longest;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Input the number of terms
        System.out.println("Enter string:");
        String s = sc.nextLine();

        System.out.println("The longest string is: " + longestWord(s));
    }
}

 ``` 

# MagicalNo.java 
 ```java 
/*

Find count of magical numbers from 1 to N
A number is magical if:
    Convert to binary.
    Replace 0 with 1 and 1 with 2 in binary string.
    Claculate sum of all diits in binary string.
    Resultant must be an odd number

Eg:
    Input: N = 5
    Output: 2

Explanation:
    1 -> Binary = 1  -> convert to = 2   sum = 2 (even)
    2 -> Binary = 10 -> convert to = 21  sum = 3 (odd)
    3 -> Binary = 11 -> convert to = 22  sum = 4 (even)
    4 -> Binary = 100 -> convert to = 211 sum = 4 (even)
    5 -> Binary = 101 -> convert to = 212 sum = 5 (odd)

*/



import java.util.Scanner;

public class MagicalNo {

    public static int Magical(int n) {
        int count = 0;
        for (int i = 1; i <= n; i++) {
            int num = i;
            int zero = 0;

            while (num != 0) {
                if(num % 2 == 0){
                    zero++;
                }
                num = num/2;
            }
            if(zero % 2 == 1){
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Input the number of terms
        System.out.println("Enter number:");
        int n = sc.nextInt();

        System.out.println("Output: " + Magical(n));
    }
}

 ``` 

# Matrix.java 
 ```java 
/*
Problem Statement 

You are required to input the size of the matrix then the elements of matrix, then you have to divide the main matrix in two sub matrices (even and odd) in such a way that element at 0 index will be considered as even and element at 1st index will be considered as odd and so on. then you have sort the even and odd matrices in ascending order then print the sum of second largest number from both the matrices

Example

enter the size of array : 5
enter element at 0 index : 3
enter element at 1 index : 4
enter element at 2 index : 1
enter element at 3 index : 7
enter element at 4 index : 9
Sorted even array : 1 3 9
Sorted odd array : 4 7

7

*/


import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;
public class Matrix {

    public static void divideArray(int[] main, ArrayList<Integer> even, ArrayList<Integer> odd) {
        for (int i = 0; i < main.length; i++) {
            if (i % 2 == 0) {
                even.add(main[i]);
            } else {
                odd.add(main[i]);
            }
        }
    }

    public static int secondLargest(ArrayList<Integer> list) {
        if (list.size() < 2) {
            throw new IllegalArgumentException("List must have at least two elements to find the second largest");
        }
        return list.get(list.size() - 2);
    }

    public static int sumOfSecondLargestElements(ArrayList<Integer> even, ArrayList<Integer> odd) {
        
        Collections.sort(even);
        Collections.sort(odd);

        System.out.println("Sorted even array ");
        for (int e : even) {
            System.out.print(e + " ");
        }
        System.out.println();

        System.out.println("Sorted odd array ");
        for (int e : odd) {
            System.out.print(e + " ");
        }
        System.out.println();

        int evenSec = secondLargest(even);
        int oddSec = secondLargest(odd);

        System.out.println("Second Largest Element in Even List is: " + evenSec);
        System.out.println("Second Largest Element in Odd List is: " + oddSec);

        return evenSec + oddSec;
    }


    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter size of array : ");
        int arrsize = sc.nextInt();

        int[] main = new int[arrsize];
        ArrayList<Integer> even = new ArrayList<>();
        ArrayList<Integer> odd = new ArrayList<>();

        System.out.println("Enter " + arrsize + " Elements");
        for (int i = 0; i < arrsize; i++) {
            main[i] = sc.nextInt();
        }

        divideArray(main, even, odd);

        int sum = sumOfSecondLargestElements(even, odd);
        System.out.println("Sum Of Second Largest Element Of Odd and Even List: " + sum);
    }
}

 ``` 

# maxDiffSuccessiveElements.java 
 ```java 
/*
Problem Statement 

Given an integer array nums, return the maximum difference between two successive elements in its sorted form. If the array contains less than two elements return 0;

Input: arr = [3,6,9,1]
Output: 3

*/


import java.util.*;

public class maxDiffSuccessiveElements{
    public static int maxDiff(int arr[], int n){
        if(n < 2){
            return 0;
        }
        Arrays.sort(arr);
        int maxdiff = Integer.MIN_VALUE;
        for(int i = 1; i < n; i++){
            maxdiff = Math.max(maxdiff, (arr[i]-arr[i-1]));
        }
        return maxdiff;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter size of arr: ");
        int n = sc.nextInt();

        System.out.print("Enter elements : ");
        int arr[] = new int[n];
        
        for(int i = 0; i < n; i++){
            arr[i] = sc.nextInt();
        }

        System.out.println("Output: "+ maxDiff(arr, n));
    }
}

 ``` 

# MaxExponent.cpp 
 ```cpp 
/*

Problem Statement               (Asked in Accenture Offcampus 2 Aug 2021, Slot 2)

You are given a function,

Int MaxExponents (int a , int b);

You have to find and return the number between ‘a’ and ‘b’ ( range inclusive on both ends) which has the maximum exponent of 2.

The algorithm to find the number with maximum exponent of 2 between the given range is

Loop between ‘a’ and ‘b’. Let the looping variable be ‘i’.
Find the exponent (power) of 2 for each ‘i’ and store the number with maximum exponent of 2 so faqrd in a variable , let say ‘max’. Set ‘max’ to ‘i’ only if ‘i’ has more exponent of 2 than ‘max’.
Return ‘max’.
Assumption: a <b

Note: If two or more numbers in the range have the same exponents of  2 , return the small number.

Example

Input:
7
12
Output:
8
Explanation:

Exponents of 2 in:

7-0

8-3

9-0

10-1

11-0

12-2

Hence maximum exponent if two is of 8.

*/


#include <iostream>
using namespace std;

int CountTwos(int n){
    int count = 0;
    while(n % 2 == 0){
        n = n/2;
        count++;
    }
    return count;
}

int MaxExponents(int a, int b){

    int maxExponent = -1;
    int result = a;

    for(int i = a; i <= b; i++){
        int exponent = CountTwos(i);
        if(exponent > maxExponent){
            maxExponent = exponent;
            result = i;
        }
        else if(exponent == maxExponent && i < result){
            result = i;
        }
    }
    return result;
}

int main()
{
	int a, b;
    cout << "Enter the range (a and b): ";
    cin >> a >> b;

    int result = MaxExponents(a, b);
    cout << "Number with maximum exponent of 2 between " << a << " and " << b << " is: " << result << endl;


	return 0;
}


 ``` 

# MaxFavouriteSong.java 
 ```java 
/*
Problem Statement 

Alice has a collection of songs represented as a string S where each character reperesents a song. Aplaylisy is the substring of the given string with exactly K number of songs. She wants to create a playlist that contains maximum number of her favourite song which is 'a'. Your task is to find and return an integer value representing the maximum number of favourite songs that she can get in a single playlist.

Input: S = "acdbaaca"
       K = 3

Output: 2

Explanation: Substring of S of size 3: {"acd", "cdb", "dba", "baa", "aac", "aca"} 

So "a" is coming max 2 times in substring

*/


import java.util.*;

public class MaxFavouriteSong{
    public static int MaxSong(String s, int k){
        int max = 0;
        int count = 0;

        int i = 0;
        int j = -1;

        int n = s.length();
        char arr[] = s.toCharArray();

        for (j = 0; j < k; j++) {
            if (arr[j] == 'a') {
                count++;
            }
        }

        max = count; 

        for (j = k; j < n; j++) {
            if (arr[i] == 'a') {
                count--;
            }
            i++;

            if (arr[j] == 'a') {
                count++;
            }
            max = Math.max(max, count);
        }     

        return count;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter string : ");
        String s = sc.nextLine();

        System.out.println("Enter K: ");
        int k = sc.nextInt();

        System.out.println("Output: "+ MaxSong(s, k));
    }
}

 ``` 

# Maximum.java 
 ```java 
/*
Problem Statement :

You are given a function, void MaxInArray(int arr[], int length); The function accepts an integer array ‘arr’ of size ‘length’ as its argument. Implement the function to find the maximum element of the array and print the maximum element and its index to the standard output 

(STDOUT). The maximum element and its index should be printed in separate lines.

Note: 

Array index starts with 0 
Maximum element and its index should be separated by a line in the output 
Assume there is only 1 maximum element in the array 
Print exactly what is asked, do not print any additional greeting messages 
Example: 

Input: 
23 45 82 27 66 12 78 13 71 86 

Output: 
86 

9 

Explanation: 
86 is the maximum element of the array at index 9. 

*/



import java.util.*;
public class Maximum
{
    public static void MaxIndElement(int arr[], int length) 
    {
        int max = arr[0], index = 0;
        for (int i = 0; i < length; i++){
            if (arr[i] > max) {
                max = arr[i];
                index = i;
            }
        }
        System.out.println (max);
        System.out.println (index);
    }

    public static void main (String[]args) 
    {
        Scanner sc = new Scanner (System.in);

        System.out.println("Enter size of array: ");
        int n = sc.nextInt ();

        int arr[] = new int[n];

        System.out.println("Enter elements: ");
        for (int i = 0; i < n; i++)
            arr[i] = sc.nextInt ();

        System.out.println("Maximum element with its index is: "); 
        MaxIndElement(arr, arr.length);
    } 
} 

 ``` 

# MaximumWithIndex.py 
 ```py 
# Given an array of integers, write a function that finds the maximum element and its index.
# Input: [1,8,4,9,6]
# Output: (9,3)

def MaximumIndex(arr):
    max = arr[0]
    maxIndex = 0
    
    for i in range(1, len(arr)):
        if arr[i] > max:
            max = arr[i]
            maxIndex = i
        
    return (max, maxIndex)


def main():
    arr = [1,8,4,9,6]
    print("Maximum number with its index is: ", MaximumIndex(arr))
    

if __name__ == "__main__":
    main()
 ``` 

# MergeSortedArrays.java 
 ```java 
/*
Problem Statement :

Given two arrays of integers, return merged sorted array.

Input: arr1 = [1, 2, 3, 4, 5],
       arr2 = [2, 4, 6, 8, 10]

Output: [1, 2, 2, 3, 4, 4, 5, 6, 8, 10]

*/



import java.util.*;
public class MergeSortedArrays
{
    public static List<Integer> MergeSortedArray(int arr1[], int arr2[]) 
    {
        List<Integer> merged = new ArrayList<>();
        int i = 0, j = 0;

        while (i < arr1.length && j < arr2.length) {
            if (arr1[i] < arr2[j]) {
                merged.add(arr1[i]);
                i++;
            } else {
                merged.add(arr2[j]);
                j++;
            }
        }
        while(i < arr1.length){
            merged.add(arr1[i]);
            i++;
        }
        while(j < arr2.length){
            merged.add(arr2[j]);
            j++;
        }
        return merged;
    }

    public static void main(String[] args) {
        int[] arr1 = {1, 3, 5, 7};
        int[] arr2 = {2, 4, 6};

        List<Integer> result = MergeSortedArray(arr1, arr2);
        for (int num : result) {
            System.out.print(num + " ");
        }
        System.out.println();  // Output: 1 2 3 4 5 6 7
    }
} 

 ``` 

# MostFrequentVowel.py 
 ```py 
'''

You are a given a string str of length n. You have to find the most frequent vowel in the string str
Note: You may assume that str will always hav a unique most frequent vowel.

Sample Test Case:
Input:
6 -> string length
xyuaab

Output:
a

Explanation: As the vowel 'a' occurs the most in the string str, hence 'a' is printed in the output.

'''

def MostFrequentVowel(str):
    FreqVow = {}
    mostFreqVow = None
    maxVow = 0
    
    for ch in str:
        if ch in 'aeiou':
            FreqVow[ch] = FreqVow.get(ch,0)+1
            
            if FreqVow[ch] > maxVow:
                maxVow = FreqVow[ch]
                mostFreqVow = ch
    
    return mostFreqVow


def main():
    str = "xyuaab"
    print("Most Frequent vowel is: ", MostFrequentVowel(str))
    

if __name__ == "__main__":
    main()
 ``` 

# MoveHyphen.java 
 ```java 
/*
Implement the following functions.a

char*MoveHyphen(char str[],int n);

The function accepts a string “str” of length ‘n’, that contains alphabets and hyphens (-). Implement the function to move all hyphens(-) in the string to the front of the given string.

NOTE:- Return null if str is null.

Example :-

Input:
str.Move-Hyphens-to-Front
Output:
—MoveHyphenstoFront
Explanation:-

The string “Move-Hyphens -to-front” has 3 hyphens (-), which are moved to the front of the string, this output is “— MoveHyphen”

Sample Input

Str: String-Compare
Sample Output-

-StringCompare

*/


import java.util.*;
public class MoveHyphen {

    public static String MHyphen(String str, int n){
        if (str == null) {
            return null;
        }

        StringBuilder hyphens = new StringBuilder();
        StringBuilder nonHyphens = new StringBuilder();

        for (int i = 0; i < n; i++) {
            if (str.charAt(i) == '-') {
                hyphens.append('-');
            } else {
                nonHyphens.append(str.charAt(i));
            }
        }

        return hyphens.toString() + nonHyphens.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); 

        System.out.println("Enter string with hypehn: ");
        String str = sc.next ();

        System.out.println ("Result: " + MHyphen(str, str.length()));
    }
}

 ``` 

# NegativeStockPrice.java 
 ```java 
/*
Problem Statement 

You are working on a financial analysing tool which repersents daily stock price of a company over time Each element in an integer array A of size N reperesnts the closing price of the stock for that particular day. Your task is to find and return an integer value representing the total number of days where the stock marke price decreased indicating negative growth.

Input: N = 6, A[] = {2,3,1,4,5,2}
Output: 2

Input: N = 1, A[] = {6}
Output: 0

*/


import java.util.*;

public class NegativeStockPrice{
    public static int CountNegativePrice(int arr[], int N){
        int count = 0;

        if(N <= 1){
            return 0;
        }

        for(int i = 0; i < N-1; i++){
            if(arr[i+1] < arr[i]){
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter size of array : ");
        int n = sc.nextInt();

        System.out.println("Enter elements: ");
        int arr[] = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        System.out.println("Output: "+ CountNegativePrice(arr, n));
    }
}

 ``` 

# nthFibonacci.java 
 ```java 
/*
Problem Statement 

Given input as n, find nth fibonacci series number.

Fibonacci series example is: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55...

Input: 9
Output: 34 (At 9th index number is 34)

*/


import java.util.*;

public class nthFibonacci{
    public static int nthFib(int n){
        if(n == 0 || n == 1){
            return n;
        }

        int a = 0, b = 1;
        int c = 0;
        for(int i = 2; i <= n; i++){
            c = a + b;
            a = b;
            b = c;
        }
        return c;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter the index to find number of fibonacci series: ");
        int n = sc.nextInt();

        System.out.println("Output: "+ nthFib(n));
    }
}

 ``` 

# OperationChoices.cpp 
 ```cpp 
/*
Problem Statement

You are required to implement the following function.

Int OperationChoices(int c, int n, int a , int b )

The function accepts 3 positive integers ‘a’ , ‘b’ and ‘c ‘ as its arguments. Implement the function to return.

( a+ b ) , if c=1
( a – b ) , if c=2
( a * b ) ,  if c=3
(a / b) ,  if c =4
Assumption : All operations will result in integer output.

Example:

Input
c :1
a:12
b:16

Output:
Since ‘c’=1 , (12+16) is performed which is equal to 28 , hence 28 is returned.

Sample Input:
 c : 2
 a : 16
 b : 20

Sample Output:
-4

*/


#include <iostream>
using namespace std;
int operationChoices(int c, int a, int b)
{
	if (c == 1) {
    	return a + b;
	}
	else if (c == 2) {
    	return a - b;
	}
	else if (c == 3) {
    	return a * b;
	}
	else if (c == 4) {
    	return a / b;
	}
	return 0;
}

int main()
{
	int x, y, z;
	int result;

    cout<<"Enter value of c: "<<endl;
	cin >> x;

    cout<<"Enter value of a: "<<endl;
	cin >> y;

    cout<<"Enter value of b: "<<endl;
	cin >> z;

	result = operationChoices(x, y, z);
	cout <<"Result: "<<result;

	return 0;
}


 ``` 

# PairSumMaxProduct.java 
 ```java 
/*
 
Given Array of size N, We have to return the pair whose sum is equal to target and having maximum product.

Note: First value of pair must be greater than the second value

Input: Target: 18
       N = 8
       arr = [11,1,2,8,10,11,15,7]

Output: [10, 8]  Sum is 18 and product is 80 which is maximum

*/

import java.util.*;

public class PairSumMaxProduct{

    public static void sortDesc(int arr[]){
        Arrays.sort(arr);
        int n = arr.length;

        for(int i = 0; i < n/2; i++){
            int temp = arr[i];
            arr[i] = arr[n-i-1];
            arr[n-i-1] = temp;
        }
    }

    public static int[] PairSum(int n, int arr[], int target){
        int ans[] = new int[2];
        int prod = 0;

        sortDesc(arr);

        int start = 0;
        int end = n-1;


        while(start < end){
            
            int sum = arr[start] + arr[end];

            if(sum == target){
                int currProd = arr[start] * arr[end];
                if(currProd > prod){
                    prod = currProd;
                    ans[0] = arr[start];
                    ans[1] = arr[end];
                }
                start++;
                end--;
            }
            else if(sum < target){
                end--;
            }
            else{
                start++;
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter size of array : ");
        int n = sc.nextInt();

        System.out.println("Enter elements: ");
        int arr[] = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        System.out.println("Enter target: ");
        int target = sc.nextInt();

        int[] result = PairSum(n, arr, target);
        if (result[0] == 0 && result[1] == 0) {
            System.out.println("No valid pair found.");
        } else {
            System.out.println("Output: [" + result[0] + ", " + result[1] + "]");
        }
    }
}

 ``` 

# PasswordChecker.java 
 ```java 
/*
You are given a function.
int CheckPassword(char str[], int n);
The function accepts string str of size n as an argument. Implement the function which returns 1 if given string str is valid password else 0.
str is a valid password if it satisfies the below conditions.

– At least 4 characters
– At least one numeric digit
– At Least one Capital Letter
– Must not have space or slash (/)
– Starting character must not be a number

Assumption:
Input string will not be empty.

Example:

Input 1:
aA1_67
Input 2:
a987 abC012

Output 1:
1
Output 2:
0

*/


import java.util.Scanner;
public class PasswordChecker {

    public static int checkPassword(String str, int n){
        if(n < 4){
            return 0;
        }
        if(str.charAt(0) >= '0' && str.charAt(0) <= '9'){
            return 0;
        }
        int count = 0;
        for(int i = 0; i < n; i++){
            if(str.charAt(i) == ' ' || str.charAt(i) == '/'){
                return 0;
            } 
            if(str.charAt(i) >= '0' && str.charAt(i) <= '9'){
                count++;
            }
            if(str.charAt(i) >= 'A' && str.charAt(i) <= 'Z'){
                count++;
            }
        }
        if(count < 2){
            return 0;
        }
        
        return 1;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); 

        System.out.println("Enter Password: ");
        String str = sc.next ();

        System.out.println (checkPassword (str, str.length ()));
    }
}
 ``` 

# PrintEvenOdd.java 
 ```java 
/*
Problem Statement 

Jack has an array of lenght N. He Wants to label whether the number in the array is even of odd. Your taks is to help find and return a string with labels even or odd in sequence according to which the numbers appear in the array.

Input: N = 6
arr = [1, 2, 3, 4, 5, 6]

Output: "odd even odd even odd even"

*/


import java.util.*;

public class PrintEvenOdd{
    public static String EvenOdd(int arr[], int n){
        if(n == 0){
            return "";
        }
        String result = "";
        for(int i = 0; i < n; i++){
            if(arr[i] % 2 == 0){
                result += "even ";
            }
            else{
                result += "odd ";
            }
        }
        return result;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter size of array : ");
        int n = sc.nextInt();

        System.out.println("Enter elements: ");
        int arr[] = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        System.out.println("Output: "+ EvenOdd(arr, n));
    }
}

 ``` 

# PrintFirstKWords.cpp 
 ```cpp 
/*

Print first K words
Example

Input: "Hello I am a passionate developer"     
    k: 3
Output:Hello I am
*/

#include<iostream>
using namespace std;

void firstKwords(string s, int k){
    for(char ch : s){
        if(ch == ' '){
            k--;
            if(k == 0)  break;
        }
        cout<<ch;
    }
}

int main(){
    string s;
    int k;

    cout<<"Enter string: "<<endl;
    getline(cin,s);

    cout<<"Enter value of k: "<<endl;
    cin>>k;

    firstKwords(s,k);
}
 ``` 

# ProductSmallest.java 
 ```java 
/*
Implement the following Function

def ProductSmallestPair(sum, arr)

The function accepts an integers sum and an integer array arr of size n. Implement the function to find the pair, (arr[j], arr[k]) where j!=k, Such that arr[j] and arr[k] are the least two elements of array (arr[j] + arr[k] <= sum) and return the product of element of this pair

NOTE

Return -1 if array is empty or if n<2
Return 0, if no such pairs found
All computed values lie within integer range
Example

Input

sum:9

size of Arr = 7

Arr:5 2 4 3 9 7 1

Output

2

Explanation

Pair of least two element is (2, 1) 2 + 1 = 3 < 9, Product of (2, 1) 2*1 = 2. Thus, output is 2

Sample Input

sum:4

size of Arr = 6

Arr:9 8 3 -7 3 9

Sample Output

-21 

*/


import java.util.*;
public class ProductSmallest {

    public static int ProductSmallestPair(int[]arr, int n, int sum){
        if (arr == null || n < 2) {
            return 0;
        }

        Arrays.sort(arr);

        int checkSum = arr[0] + arr[1];
        if(checkSum <= sum){
            return arr[0] * arr[1];
        }else{
            return 0;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); 

        System.out.println("Enter sum: ");
        int sum = sc.nextInt ();

        System.out.println("Enter size of arr: ");
        int n = sc.nextInt ();

        int arr[] = new int[n];
        System.out.println("Enter elements: ");

        for (int i = 0; i < n; i++)
            arr[i] = sc.nextInt ();

        System.out.println ("Sum: " + ProductSmallestPair(arr, n, sum));
    }
}

 ``` 

# RatCountHouse.java 
 ```java 
/*
Problem Description :
The function accepts two positive integers ‘r’ and ‘unit’ and a positive integer array ‘arr’ of size ‘n’ as its argument ‘r’ represents the number of rats present in an area, ‘unit’ is the amount of food each rat consumes and each ith element of array ‘arr’ represents the amount of food present in ‘i+1’ house number, where 0 <= i

Note:
- Return -1 if the array is null
- Return 0 if the total amount of food from all houses is not     sufficient for all the rats.
- Computed values lie within the integer range.

Example:

Input:
r: 7
unit: 2
n: 8
arr: 2 8 3 5 7 4 1 2

Output:
4

Explanation:
Total amount of food required for all rats = r * unit
                                           = 7 * 2 = 14.

The amount of food in 1st houses = 2+8+3+5 = 18. Since, amount of food in 1st 4 houses is sufficient for all the rats. Thus, output is 4.

*/


import java.util.*;

public class RatCountHouse {

    public static int Solve(int r, int unit, int arr[], int n){
        if(arr == null){
            return 0;
        }

        int totalFood = r * unit;

        int sum = 0, count = 0;

        for(int i = 0; i < n; i++){
            sum += arr[i];
            count++;
            if(sum >= totalFood){
                break;
            }
        }
        if(sum < totalFood){
            return 0;
        }
        
        return count;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); 
            
        int r = sc.nextInt ();
        int unit = sc.nextInt ();
        int n = sc.nextInt ();
        int arr[] = new int[n];

        for (int i = 0; i < n; i++){
            arr[i] = sc.nextInt ();
        }

        System.out.println(Solve(r, unit, arr, n));
    }
}
 ``` 

# RearrangementsOfBits.cpp 
 ```cpp 
/*
Rearrangement Of Bits

Alex Gives You a positive Number N and wants you to rearrange the
bits of the number in its binary representation such that all set bits are in consecutive order. Your task is to find and return an integer value representing the minimum possible number that can be formed after re-arranging the bits of the number N.

Example

Input1: 10      
Output: 3
Explanation: 10 -> binary: 1010 count the set bits and arrange in consecutive order such as 0011 which in decimal is 3.

Input: 2
Output: 1
*/

#include<iostream>
using namespace std;

int rearrangement(int n){
    int count = 0;
    while(n > 0){
        if(n & 1) {
            count++;
        }
        n = n >> 1;
    }

    return (1 << count)-1;
}

int main(){
    int n;

    cout<<"Enter the number: "<<endl;
    cin>>n;

    cout<<"Output: "<<rearrangement(n)<<endl;

}
 ``` 

# removeDuplicate.py 
 ```py 
# Given an array of integers, write a function to remove duplicate elements.
# Input: [1, 2, 2, 3, 4, 4, 5]
# Output: [1, 2, 3, 4, 5]

def RemoveDuplicate(arr):
    uniqueElem = []
    
    for elem in arr:
        if elem not in uniqueElem:
            uniqueElem.append(elem)
            
    return uniqueElem


def main():
    arr = [1, 2, 2, 3, 4, 4, 5]
    print("Unique elements are: ", RemoveDuplicate(arr))
    

if __name__ == "__main__":
    main()
 ``` 

# RepeateString.java 
 ```java 
/*
    
Given an integer N and string S. your task is to find and return new String which consist of the original string repeated N times.

Input: N = 3, S = "abc"
Output: "abcabcabc"

*/

import java.util.*;
public class RepeateString {

    public static String repeate(String str, int n){
        String repeate = "";
        while(n > 0){
            repeate += str;
            n--;
        }
        return repeate;
    }


    public static void main(String[] args) {
        String str = "abc";
        int n = 3;
        System.out.println(repeate(str, n));
    }
}
 ``` 

# ReplaceCharacter.cpp 
 ```cpp 
/*
You are given a function,

Void *ReplaceCharacter(Char str[], int n, char ch1, char ch2);

The function accepts a string  ‘ str’ of length n and two characters ‘ch1’ and ‘ch2’ as its arguments . Implement the function to modify and return the string ‘ str’ in such a way that all occurrences of ‘ch1’ in original string are replaced by ‘ch2’ and all occurrences of ‘ch2’  in original string are replaced by ‘ch1’.

Assumption: String Contains only lower-case alphabetical letters.

Note:

Return null if string is null.
If both characters are not present in string or both of them are same , then return the string unchanged.
Example:

Input:
Str: apples
ch1:a
ch2:p
Output:
paales
Explanation:

‘A’ in original string is replaced with ‘p’ and ‘p’ in original string is replaced with ‘a’, thus output is paales.

*/


#include<iostream>
#include<cstring>
using namespace std;

void ReplaceCharacter(char str[], int n, char ch1, char ch2){
    for(int i = 0; i < n; i++){
        if(str[i] == ch1){
            str[i] = ch2;
        }
        else if(str[i] == ch2){
            str[i] = ch1;
        }
    }
    cout<<str;
}


int main(){

    char str[100];
    char b, c;
    int len;

    cout<<"Enter string: "<<endl;
    cin >> str;

    cout<<"Enter ch1: "<<endl;
    cin >> b;

    cout<<"Enter ch2: "<<endl;
    cin >> c;

    len = strlen(str);
    ReplaceCharacter(str, len, b, c);

    return 0;
}


 ``` 

# ReplaceFrequentCharacters.java 
 ```java 
import java.util.*;
public class ReplaceFrequentCharacters {

    static String Replace(String str, char c){
        Map<Character, Integer> mp = new HashMap<>();

        for(int i = 0; i < str.length(); i++){
            if(mp.containsKey(str.charAt(i))){
                mp.put(str.charAt(i), mp.get(str.charAt(i))+1);
            }
            else{
                mp.put(str.charAt(i),1);
            }
        }
        int max = 0;
        char maxChar = ' ';

        for(Map.Entry<Character, Integer> entry : mp.entrySet()){
            if(entry.getValue() > max){
                max = entry.getValue();
                maxChar = entry.getKey();
            }
        }

        return str.replace(maxChar, c);

    }


    public static void main(String[] args) {
    Scanner sc = new Scanner(System.in); 
        
        String str = "bbadbbababb";
        String result = Replace(str, 't');
        System.out.println(result);

    }
}
 ``` 

# ReverseString.java 
 ```java 
import java.util.Scanner;
public class ReverseString {

    public static String reverseString(String str){
        String reversed = "";
        for(int i = 0; i < str.length(); i++){
            reversed = str.charAt(i) + reversed;
        }
        return reversed;
    }


    public static void main(String[] args) {
        String str = "hello";
        System.out.println(reverseString(str));
    }
}
 ``` 

# ReverseWords.java 
 ```java 
/*

Input: 
A single line of text containing words separated by spaces. The input string consists of only printable ASCII characters. 

Output: 
The string with words reversed in order. 

Example: 
Input: Hello 
World 

Output: 
World Hello

*/


import java.util.*;

public class ReverseWords{

    public static void reverseWord(String s){

        String[] words = s.split(" ");

        String reversedString = "";

        for (int i = words.length - 1; i >= 0; i--) {
            reversedString += words[i];
            if (i != 0) {
                reversedString += " "; // Add space between words
            }
        }

        System.out.println(reversedString);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter string: ");
        String s=sc.nextLine(); 

        reverseWord(s);
    }
}
 ``` 

# rhymeWords.py 
 ```py 
def rhymeWords(S, D):
    best_word = "No Word"
    max_match_length = 0
    
    for word in D:
        if word == S:
            continue
        
        # Find the longest matching suffix
        min_length = min(len(S), len(word))
        match_length = 0
        
        for i in range(1, min_length + 1):
            if S[-i] == word[-i]:
                match_length += 1
            else:
                break
        
        # Update best_word if this word has a longer matching suffix
        if match_length > max_match_length:
            max_match_length = match_length
            best_word = word
    
    return best_word
            
            
def main():
    S = "thunder"
    D = ["pukle", "thunder", "powder", "blender", "under"]
    output = rhymeWords(S, D)
    print(output) 
    

if __name__ == "__main__":
    main()
 ``` 

# Roots.py 
 ```py 
# Function to find the roots of a quadratic equation ax^2 + bx + c = 0
# Formula:   +X = (-b + underoot b2 - 4ac/2a)
#            -X = (-b - underoot b2 - 4ac/2a)

import math

def RootsofEquation(a, b, c):
    root1 = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    root2 = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
    return root1, root2


# Example usage
a = 1
b = -3
c = 2
result = RootsofEquation(a, b, c)
print("Roots of the equation:", result)
 ``` 

# RotateArrayByK.java 
 ```java 
/*

Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.

Example 1:

Input: nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
rotate 1 steps to the right: [7,1,2,3,4,5,6]
rotate 2 steps to the right: [6,7,1,2,3,4,5]
rotate 3 steps to the right: [5,6,7,1,2,3,4]

*/


import java.util.*;

public class RotateArrayByK{
    public static void rotate(int arr[], int n, int k){
        k = k % n;
        swap(arr, 0, n-1);
        swap(arr, 0, k-1);
        swap(arr, k, n-1);
    }

    public static void swap(int arr[], int s, int e){
        while(s <= e){
            int temp = arr[s];
            arr[s] = arr[e];
            arr[e] = temp;
            s++;
            e--;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter size of arr: ");
        int n = sc.nextInt();

        System.out.print("Enter elements : ");
        int arr[] = new int[n];
        
        for(int i = 0; i < n; i++){
            arr[i] = sc.nextInt();
        }

        System.out.println("Enter K: ");
        int k = sc.nextInt();

        rotate(arr, n, k);

        System.out.println("After rotating array by k steps: ");
        for(int i = 0; i < n; i++){
            System.out.print(arr[i] + " ");
        }

    }
}
 ``` 

# SecondLargest.java 
 ```java 
import java.util.Scanner;
public class SecondLargest {

    public static int secondLargest(int arr[]){
        int first = Integer.MIN_VALUE;
        int second = Integer.MIN_VALUE;

        for (int i = 0; i < arr.length; i++) {
            if(arr[i] > first){
                second = first;
                first = arr[i];
            }
            else if(arr[i] > second && arr[i] != first){
                second = arr[i];
            }
        }
        return second;
    }

    public static void main(String[] args) {
        int[] arr = {1, 3, 5, 2, 4, 6, 8};
        System.out.println(secondLargest(arr));    
    }   
}
 ``` 

# SetZeroMatrix.java 
 ```java 
/*
Problem Statement 

Given an m * n integer matrix , if an element is 0, set its entire row and column to 0.

Input: matrix = [[1,1,1],
                 [1,0,1],
                 [1,1,1]]

Output: matrix = [[1,0,1],
                  [0,0,0],
                  [1,0,1]]

*/


import java.util.*;

public class SetZeroMatrix{
    public static void setZero(int matrix[][]){
        int rowlen = matrix.length;
        int collen = matrix[0].length;

        int rowarr[] = new int[rowlen];
        int colarr[] = new int[collen];

        for(int i = 0; i < rowlen; i++){
            for(int j = 0; j < collen; j++){
                if(matrix[i][j] == 0){
                    rowarr[i] = 1;
                    colarr[j] = 1;
                }
            }
        }

        for(int i = 0; i < rowlen; i++){
            for(int j = 0; j < collen; j++){
                if(rowarr[i] == 1 || colarr[j] == 1){
                    matrix[i][j] = 0;
                }
            }
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter no of row : ");
        int row = sc.nextInt();

        System.out.print("Enter no of col : ");
        int col = sc.nextInt();

        System.out.println("Enter elements: ");
        int matrix[][] = new int[row][col];
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                matrix[i][j] = sc.nextInt();
            }
        }

        setZero(matrix);

        System.out.println("Output matrix: ");
        for (int i = 0; i < row; i++) {
            for (int j = 0; j < col; j++) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println();
        }
    }
}

 ``` 

# SmallLargeSum.java 
 ```java 
/*

Write a function SmallLargeSum(array) which accepts the array as an argument or parameter, that performs the addition of the second largest element from the even location with the second largest element from an odd location?
Rules:
a. All the array elements are unique.
b. If the length of the array is 3 or less than 3, then return 0.
c. If Array is empty then return zero.

Sample Test Case 1:
Input:
6
3 2 1 7 5 4
Output:
7

Explanation: The second largest element in the even locations (3, 1, 5) is 3. The second largest element in the odd locations (2, 7, 4) is 4. So the addition of 3 and 4 is 7. So the answer is 7.

Sample Test Case 2:
Input:
7
4 0 7 9 6 4 2
Output:
10

*/




public class SmallLargeSum {
    public static int SmallLargeSum(int[] array) {
        if (array.length <= 3) {
            return 0;
        }

        int firstEven = Integer.MIN_VALUE;
        int secondEven = Integer.MIN_VALUE;
        int firstOdd = Integer.MIN_VALUE;
        int secondOdd = Integer.MIN_VALUE;

        for (int i = 0; i < array.length; i++) {
            if (i % 2 == 0) {
                if (array[i] > firstEven) {
                    secondEven = firstEven;
                    firstEven = array[i];
                } else if (array[i] > secondEven) {
                    secondEven = array[i];
                }
            } else {
                if (array[i] > firstOdd) {
                    secondOdd = firstOdd;
                    firstOdd = array[i];
                } else if (array[i] > secondOdd) {
                    secondOdd = array[i];
                }
            }
        }

        return secondEven + secondOdd;
    }

    // Sample test cases
    public static void main(String[] args) {
        int[] array1 = {3, 2, 1, 7, 5, 4};
        System.out.println(SmallLargeSum(array1));  // Output: 7

        int[] array2 = {4, 0, 7, 9, 6, 4, 2};
        System.out.println(SmallLargeSum(array2));  // Output: 10
    }
}

 ``` 

# StandardDeviation.java 
 ```java 
import java.util.*;
public class StandardDeviation {

    public static double SD(List<Integer> arr){
        
        int n = arr.size();
        double avg = 0;
        double sum = 0;
        

        for(int i = 0; i < n; i++){
            sum += arr.get(i);
        }
        avg = sum / n;

        double sumOfSquare = 0;
        for(int i = 0; i < n; i++){
            sumOfSquare += Math.pow(arr.get(i) - avg, 2);
        }

        double sd = Math.sqrt(sumOfSquare / n);
        return sd;
    }


    public static void main(String[] args) {
    Scanner sc = new Scanner(System.in); 
        
        System.out.println("Enter the no of elements: ");
        int n = sc.nextInt();

        List<Integer> arr = new ArrayList<Integer>();

        System.out.println("Enter elements: ");
        for(int i = 0; i < n; i++){
            arr.add(sc.nextInt());
        }
        System.out.println(SD(arr));
    }
}
 ``` 

# StringDecoder.java 
 ```java 
/*

Problem Statement 

You are provided with a string which has a sequence of 1s and Os. This sequence is the encoded version of a english word. You are supposed to write a program to decode the provided string and find the original word. Each uppercase Alphabet is representing by a sequence of 1s

Input: 10110111
Output: ABC

Explanation: 1 0 1 1 0 1 1 1
             A    B      C



*/


import java.util.*;
public class StringDecoder {

    static String Decoder(String s){
        if (s.length() == 0 || s.charAt(0) == '0') {
            return ""; 
        }
        
        String ans = "";
        int count = 0;

        for(int i = 0; i < s.length(); i++){
            if(s.charAt(i) == '1'){
                count++;
            }
            else{
                ans += (char)('A' + count - 1);
                count = 0;
            }
        }
        ans += (char)('A' + count - 1);
        return ans;
    }


    public static void main(String[] args) {
    Scanner sc = new Scanner(System.in); 
        
        System.out.println("Enter string: ");
        String str = sc.nextLine();

        System.out.println("Output: " + Decoder(str));

    }
}
 ``` 

# Sum3and5.c 
 ```c 
/*

Problem Statement           (Asked in Accenture Offcampus 2 Aug 2021, Slot 3)

You are required to implement the following function:

Int Calculate(int m, int n);

The function accepts 2 positive integer ‘m’ and ‘n’ as its arguments.You are required to calculate the sum of numbers divisible both by 3 and 5, between ‘m’ and ‘n’ both inclusive and return the same.
Note
0 < m <= n

Example

Input:
m : 12
n : 50

Output
90

Explanation:
The numbers divisible by both 3 and 5, between 12 and 50 both inclusive are {15, 30, 45} and their sum is 90.
Sample Input
m : 100
n : 160
Sample Output
510

*/


#include <stdio.h>

int Calculate(int m, int n){
    int sum = 0;
    for(int i = m; i <= n; i++){
        if(i % 3 == 0 && i % 5 == 0){
            sum += i;
        }
    }
    return sum;
}


int main()
{
	int m, n, result;

    printf ("Enter the value of m : ");
    scanf ("%d", &m);

    printf ("Enter the value of n : ");
    scanf ("%d", &n);

    result = Calculate (m, n);
    printf ("%d", result);

	return 0;
}


 ``` 

# SumBinary.py 
 ```py 
# You are given an i nt eger 'n'. Write a Python function to calculate and return the sum of the digits in 'n' after converting it to its binary representation.

# For  example, 15,  which has a  binary representation of  1111,  should 
# ret urn 4.


def SumBinary(n):
    sum = 0
    
    while n > 0:
        lastDigit = n & 1
        sum += lastDigit
        n = n >> 1
    
    return sum   
    
    
def main():
    print("Enter number: ")
    n = int(input())
    result = SumBinary(n)
    print("Sum of binary digits:", result)
        
if __name__ == "__main__":
    main()
 ``` 

# SumDifference.java 
 ```java 
/*
Implement the following Function 

def differenceofSum(n. m)

The function accepts two integers n, m as arguments Find the sum of all numbers in range from 1 to m(both inclusive) that are not divisible by n. Return difference between sum of integers not divisible by n with sum of numbers divisible by n.

Assumption:

n>0 and m>0
Sum lies between integral range

Example

Input
n:4
m:20

Output
90

Explanation

Sum of numbers divisible by 4 are 4 + 8 + 12 + 16 + 20 = 60
Sum of numbers not divisible by 4 are 1 +2 + 3 + 5 + 6 + 7 + 9 + 10 + 11 + 13 + 14 + 15 + 17 + 18 + 19 = 150
Difference 150 – 60 = 90
Sample Input
n:3
m:10
Sample Output
19

*/


import java.util.Scanner;
public class SumDifference {

    public static int SumDiff(int n, int m){

        int sum1 = 0, sum2 = 0;
        for(int i = 1; i <= m; i++){
            if (i % n == 0)
                sum1 = sum1 + i;
    	    else    
                sum2 = sum2 + i;
        }

        return Math.abs(sum1 - sum2);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); 

        System.out.println("Enter value of n: ");
        int n = sc.nextInt ();

        System.out.println("Enter value of m: ");
        int m = sc.nextInt ();

        System.out.println ("Difference: " + SumDiff(n,m));
    }
}

 ``` 

# SumEvenIndex.java 
 ```java 
/*
Problem Statement 

Given an array A of length N, find the sum of even positions after reversing the array. Your task is to find and return an integer value represneting sum of the array elements present at the even index of the reveresed array.

input: N = 6, arr = 10,20,30,40,50,60
output: 120

Explanation: reversed array: 60,50,40,30,20,10 and then sum even index(index starting from 0) elements which are 60,40,20

*/


import java.util.*;

public class SumEvenIndex{
    public static int sumEvenIndex(int arr[], int n){
        if(n == 0){
            return 0;
        }
        
        int i = 0, j = n-1;
        while(i <= j){
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            i++;
            j--;
        }

        int sum = 0;
        for(int k = 0; k < n; k++){
            if(k % 2 == 0){
                sum += arr[k];
            }
        }
        return sum;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter size of array : ");
        int n = sc.nextInt();

        System.out.println("Enter elements: ");
        int arr[] = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        System.out.println("Output: "+ sumEvenIndex(arr, n));
    }
}

 ``` 

# SumOfDivisors.cpp 
 ```cpp 
// Input: 12
// Output: 28
// Explanation: Divisors of 12 between 1 to 12 are: 1,2,3,4,6,12  so by adding them we get 28.

#include <iostream>
using namespace std;

int SumOfDivisor(int N) {
    int sum = 0;
    for (int i = 1; i <= N; i++) {
        if (N % i == 0) {
            sum += i;
        }
    }
    return sum;
}

int main() {
    int N = 12;
    cout << "The sum of the divisors of " << N << " is " << SumOfDivisor(N) << endl;  
    return 0;
}
 ``` 

# SumPrimeNo.java 
 ```java 

/*
Problem Statement :

Write a function that takes an integer n as input and returns the sum of all prime numbers less than N.

Input: 10
Output: 17

Explanation: prime no less than 10 are: 2, 3, 5, 7 

*/



import java.util.*;
public class SumPrimeNo
{
    public static int sumPrime(int n) {
        int sum = 0;

        for (int i = 2; i < n; i++) {
            boolean isPrime = true;

            if (i <= 1) {
                isPrime = false;
            } 
            else {
                for (int j = 2; j <= Math.sqrt(i); j++) {
                    if (i % j == 0) {
                        isPrime = false;
                        break;
                    }
                }
            }
            if (isPrime) {
                sum += i;
            }
        }
        return sum;
    }



    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter N: ");
        int n = sc.nextInt();

        System.out.println("Output: " + sumPrime(n));
        
    }
} 


 ``` 

# Table.c 
 ```c 
/*

Problem: Write a program in C to display the table of a number and print the sum of all the multiples in it.

Test Cases:

Test Case 1:
Input:
5
Expected Result Value:
5, 10, 15, 20, 25, 30, 35, 40, 45, 50
275

Test Case 2:
Input:
12
Expected Result Value:
12, 24, 36, 48, 60, 72, 84, 96, 108, 120
660

*/


#include<stdio.h>
int main ()
{
    int n, i, value = 0, sum = 0;

    printf ("Enter the number for which you want to know the table : ");
    scanf ("%d", &n);

    for (i = 1; i <= 10; ++i){
        value = n * i;
        printf ("%d ", value);
        sum = sum + value;
    }

    printf ("\nSum is %d", sum);

    return 0;
}
 ``` 

# VowelPermutation.java 
 ```java 
/*
Problem Statement 

You are given a string S and your task is to find and return the count of permutation formed by fixing the positions of the vowels present in the string.

Input: ABC
Output: 2

Explanation: A will be constant, and remaining 2 will return their permutation which is factorial of 2

*/


import java.util.*;

public class VowelPermutation{

    public static int factorial(int n){
        if(n == 0 || n == 1){
            return 1;
        }
        int ans = 1;
        for(int i = 2; i <= n; i++){
            ans *= i;
        }
        return ans;
    }

    public static int permutation(String s){
        HashSet<Character> vowels = new HashSet<>();

        vowels.add('A');
        vowels.add('E');
        vowels.add('I');
        vowels.add('O');
        vowels.add('U');
        vowels.add('a');
        vowels.add('e');
        vowels.add('i');
        vowels.add('o');
        vowels.add('u');
        
        int nonVowelCount = 0;
        for(int i = 0; i < s.length(); i++){
            if(!vowels.contains(s.charAt(i))){
                nonVowelCount++;
            }
        }
        return factorial(nonVowelCount);
    }


    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter string : ");
        String s = sc.nextLine();

        System.out.println("Output: "+ permutation(s));
    }
}

 ``` 

# VowelRepetition.java 
 ```java 
/*

You are a given a string str of length n. You have to find the most frequent vowel in the string str
Note: You may assume that str will always hav a unique most frequent vowel.

Sample Test Case:
Input:
7 -> string length
xayuaba

Output:
a

Explanation: As the vowel 'a' occurs the most in the string str, hence 'a' is printed in the output.

*/

import java.util.HashMap;

public class VowelRepetition {

    // Method to find the most frequent vowel in the string
    public static char MostFrequentVowel(String str) {
        HashMap<Character, Integer> vowelCounts = new HashMap<>();
        char mostFrequentVowel = '\0';
        int maxCount = 0;

        for (int i = 0; i < str.length(); i++) {
            char ch = str.charAt(i);
            if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
                vowelCounts.put(ch, vowelCounts.getOrDefault(ch, 0) + 1);

                // Update most frequent vowel if current one has a higher count
                if (vowelCounts.get(ch) > maxCount) {
                    maxCount = vowelCounts.get(ch);
                    mostFrequentVowel = ch;
                }
            }
        }

        return mostFrequentVowel;
    }

    public static void main(String[] args) {
        String str = "xayuaba";
        char result = MostFrequentVowel(str);
        System.out.println("Most Frequent vowel is: "+result);  // Output: a
    }
}

 ``` 

