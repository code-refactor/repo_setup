#!/usr/bin/env python3

from collections import deque as de
import math
class My_stack():
    def __init__(self):
        self.data = []
    def my_push(self, x):
        return (self.data.append(x))
    def my_pop(self):
        return (self.data.pop())
    def my_peak(self):
        return (self.data[-1])
    def my_contains(self, x):
        return (self.data.count(x))
    def my_show_all(self):
        return (self.data)
    def isEmpty(self):
      return len(self.data)==0

arrStack = My_stack()    
# A optimized school method based 
# Python3 program to check 
# if a number is prime 


def isPrime(n) : 

	# Corner cases 
	if (n <= 1) : 
		return False
	if (n <= 3) : 
		return True

	# This is checked so that we can skip 
	# middle five numbers in below loop 
	if (n % 2 == 0 or n % 3 == 0) : 
		return False

	i = 5
	while(i * i <= n) : 
		if (n % i == 0 or n % (i + 2) == 0) : 
			return False
		i = i + 6

	return True

def get_prime_factors(number):
    # create an empty list and later I will
    # run a for loop with range() function using the append() method to add elements to the list.
    prime_factors = []

    # First get the number of two's that divide number
    # i.e the number of 2's that are in the factors
    while number % 2 == 0:
        prime_factors.append(2)
        number = number / 2

    # After the above while loop, when number has been
    # divided by all the 2's - so the number must be odd at this point
    # Otherwise it would be perfectly divisible by 2 another time
    # so now that its odd I can skip 2 ( i = i + 2) for each increment
    for i in range(3, int(math.sqrt(number)) + 1, 2):
        while number % i == 0:
            prime_factors.append(int(i))
            number = number / i


    # Here is the crucial part.
    # First quick refreshment on the two key mathematical conjectures of Prime factorization of any non-Prime number
    # Which is - 1. If n is not a prime number AT-LEAST one Prime factor would be less than sqrt(n)
    # And - 2. If n is not a prime number - There can be AT-MOST 1 prime factor of n greater than sqrt(n).
    # Like 7 is a prime-factor for 14 which is greater than sqrt(14)
    # But if the above loop DOES NOT go beyond square root of the initial n.
    # Then how does that greater than sqrt(n) prime-factor
    # will be captured in my prime factorization function.
    # ANS to that is - in my first for-loop I am dividing n with the prime number if that prime is a factor of n.
    # Meaning, after this first for-loop gets executed completely, the adjusted initial n should become
    # either 1 or greater than 1
    # And if n has NOT become 1 after the previous for-loop, that means that
    # The remaining n is that prime factor which is greater that the square root of initial n.
    # And that's why in the next part of my gorithm, I need to check whether n becomes 1 or not,
    #This code is taken ny rohan paul's github
    if number > 2:
        prime_factors.append(int(number))

    return prime_factors
n=int(input())
if isPrime(n):
    print(1)
else:
    if n%2:
        l=get_prime_factors(n)
        print(((n-l[0])//2)+1)
    else:
        print(n//2)