#!/usr/bin/python
from toolset import *
import data

def problem1():
    """Add all the natural numbers below 1000 that are multiples of 3 or 5.""" 
    return sum(x for x in xrange(1, 1000) if x % 3 == 0 or x % 5 == 0)

def problem2():
    """Find the sum of all the even-valued terms in the Fibonacci < four million."""
    even_fibonacci = (x for x in fibonacci() if x % 2)
    return sum(takewhile(lambda x: x < 4e6, even_fibonacci))
  
def problem3():
    """Find the largest prime factor of a composite number."""
    return max(prime_factors(600851475143))

def problem4():
    """Find the largest palindrome made from the product of two 3-digit numbers."""
    # A brute-force solution works fine, but we can simplify it a little bit:
    # x*y = "abccda" = 100001a + 10010b + 1100c = 11 * (9091a + 910b + 100c)
    # So at least one of them must be multiple of 11 (let's say it's x) 
    candidates = (x*y for x in xrange(110, 1000, 11) for y in xrange(x, 1000))
    return max(ifilter(is_palindromic, candidates))

def problem5():
    """What is the smallest positive number that is evenly divisible by all of 
    the numbers from 1 to 20?."""
    return reduce(least_common_multiple, range(2, 20+1))

def problem6():
    """Find the difference between the sum of the squares of the first one 
    hundred natural numbers and the square of the sum."""
    sum_of_squares = sum(x**2 for x in xrange(1, 100+1))
    square_of_sums = sum(xrange(1, 100+1))**2
    return square_of_sums - sum_of_squares

def problem7():
    """What is the 10001st prime number?."""
    return index(10001-1, primes())
  
def problem8():
    """Find the greatest product of five consecutive digits in the 1000-digit number"""
    digits = (int(c) for c in "".join(data.problem8.strip().splitlines()))
    return max(product(nums) for nums in groups(digits, 5, 1))
  
def problem9():
    """There exists exactly one Pythagorean triplet for which a + b + c = 1000.
    Find the product abc."""
    triplets = ((a, b, 1000-a-b) for a in xrange(1, 999) for b in xrange(a+1, 999))
    return first(a*b*c for (a, b, c) in triplets if a**2+b**2==c**2)
  
def problem10():
    """Find the sum of all the primes below two million."""
    return sum(takewhile(lambda x: x<2e6, primes()))

def problem11():
    """What is the greatest product of four adjacent numbers in any direction 
    (up, down, left, right, or diagonally) in the 20x20 grid?"""
    def _grid_get(g, nr, nc, sr, sc):
        return (g[nr][nc] if 0 <= nr < sr and 0 <= nc < sc else 0)
    grid = [map(int, line.split()) for line in data.problem11.strip().splitlines()]
    diffs = [(0, +1), (+1, 0), (+1, +1), (+1, -1)]
    sr, sc = len(grid), len(grid[0]),
    return max(product(_grid_get(grid, nr+i*dr, nc+i*dc, sr, sc) for i in range(4))
        for nr in range(sr) for nc in range(sc) for (dr, dc) in diffs)
        
def problem12():
    """What is the value of the first triangle number to have over five 
    hundred divisors?"""
    def _divisors(n):
        all_factors = [[f**p for p in range(fp+1)] for (f, fp) in factorize(n)]
        return (product(ns) for ns in cartesian_product(*all_factors))
    triangle_numbers = (triangle_number(n) for n in count(1))
    return first(tn for tn in triangle_numbers if iterlen(_divisors(tn)) > 500)

def problem13():
    """Work out the first ten digits of the sum of the following one-hundred 
    50-digit numbers."""
    numbers = (int(x) for x in data.problem13.strip().splitlines())
    return int(str(sum(numbers))[:10])

def problem14():
    """The following iterative sequence is defined for the set of positive 
    integers: n -> n/2 (n is even), n -> 3n + 1 (n is odd). Which starting 
    number, under one million, produces the longest chain?"""
    def _collatz_function(n):
        return ((3*n + 1) if (n % 2) else (n/2))
    @memoize
    def _collatz_series_length(n):
        return (1+_collatz_series_length(_collatz_function(n)) if n>1 else 0)
    return max(xrange(1, int(1e6)), key=_collatz_series_length)
