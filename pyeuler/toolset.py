#!/usr/bin/python
import operator
from itertools import ifilter, ifilterfalse, islice, repeat, groupby
from itertools import count, imap, takewhile, tee, izip
from itertools import chain, starmap, cycle, dropwhile
from itertools import product as cartesian_product
from math import sqrt, log, log10, ceil

def take(n, iterable):
    """Take first n elements from iterable"""
    return islice(iterable, n)

def index(n, iterable):
    "Returns the nth item"
    return islice(iterable, n, n+1).next()

def first(iterable):
    """Take first element in the iterable"""
    return iterable.next()

def last(iterable):
    """Take last element in the iterable"""
    return reduce(lambda x, y: y, iterable)

def take_every(n, iterable):
    """Take an element from iterator every n elements"""
    return islice(iterable, 0, None, n)

def drop(n, iterable):
    """Drop n elements from iterable and return the rest"""
    return islice(iterable, n, None)

def no(seq, pred=bool):
    "Returns True if pred(x) is False for every element in the iterable"
    return (True not in imap(pred, seq))

def iterlen(it):
    """Return length exhausing an iterator"""
    return sum(1 for _ in it)

def product(nums):
    """Product of nums"""
    return reduce(operator.mul, nums, 1)

def groups(iterable, n, step):
    """Make groups of 'n' elements from the iterable advancing
    'step' elements on each iteration"""
    itlist = tee(iterable, n)
    onestepit = izip(*(starmap(drop, enumerate(itlist))))
    return take_every(step, onestepit)

def flatten(lstlsts):
    """Flatten a list of lists"""
    return list(chain.from_iterable(lstlsts))

def ireduce(func, iterable, init=None):
    """Like reduce() but using iterators (also known also scanl)"""
    # not functional
    if init is None:
        iterable = iter(iterable)
        curr = iterable.next()
    else:
        curr = init
        yield init
    for x in iterable:
        curr = func(curr, x)
        yield curr

def compact(it):
    """Filter None values from iterator"""
    return ifilterfalse(lambda x: x is None, it)

def unique(it):
    """Return items from iterator (order preserved)"""
    # non-functional 
    seen = set()
    for x in it:
        if x not in seen:
            seen.add(x)
            yield x

def _unique(it):
    """Return items from iterator (order preserved)"""
    # functional but slow as hell. Just a proof-of-concept, don't use it
    steps = ireduce(lambda (last, seen), x: ((last, seen) if x in seen 
      else ([x], seen.union([x]))), it, ([], set()))
    return (m for (m, g) in groupby(flatten(last for (last, seen) in steps)))
        
def has_different_items(it):
    """Return True if all elements in iterator are different"""
    lst = list(it)
    return (len(set(lst)) == len(lst))

def remove_from_sequence(sequence, toremove):
    """Remove some elements (given in a scalar or sequence) from sequence"""
    if isinstance(toremove, (list, tuple)):
        condition = operator.contains
    else: condition = operator.eq
    return [x for x in sequence if not condition(toremove, x)]

# Common maths functions

def identity(x):
    """Do nothing and return the variable untouched"""
    return x

def fibonacci():
    """Generate fibonnacci serie"""
    get_next = lambda (a, b), _: (b, a+b)
    return (b for a, b in ireduce(get_next, count(), (0, 1)))

def factorial(num):
    """Return factorial value of num (num!)"""
    return product(xrange(2, num+1))

def is_integer(x, epsilon=1e-6):
    """Return True if the float x "seems" an integer"""
    return (abs(round(x) - x) < epsilon)

def is_prime(n):
    """Return True if n is a prime number (1 is not considerd prime)."""
    if n < 3:
        return (n == 2)
    elif n % 2 == 0:
        return False
    elif any(((n % x) == 0) for x in xrange(3, int(sqrt(n))+1, 2)):
        return False
    return True

def primes(start=2):
    """Generate prime numbers from 'start'"""
    return ifilter(is_prime, count(start))

def primes2():
    """Generate all prime nubers (generator version)"""
    ints = count(2)
    while True:
        prime = ints.next()
        yield prime
        def filtpred(v, p=prime):
            return ((v % p) != 0)
        ints = ifilter(filtpred, ints)

def digits_from_num(num, base=10):
    """Get digits from num in base 'base'"""
    def recursive(num, base, current):
        if num < base:
            return current+[num]
        return recursive(num/base, base, current+[num%base])
    return list(reversed(recursive(num, base, [])))

def num_from_digits(digits, base=10):
    """Get digits from num in base 'base'"""
    return sum(x*(base**n) for (n, x) in enumerate(reversed(digits)))

def is_palindromic(num, base=10):
    """Check if 'num' in base 'base' is a palindrome, that's it, if it can be
    read equally from left to right and right to left."""
    digitslst = digits_from_num(num, base)
    return digitslst == list(reversed(digitslst))

def ocurrences(it, exchange=False):
    """Return dictionary with ocurrences of each item in iterable"""
    return reduce(lambda oc, x: dict(oc, **{x: oc.get(x, 0) + 1}), it, {})

def prime_factors(num, start=2):
    """Return all prime factors (ordered) of num in a list"""
    candidates = xrange(start, int(sqrt(num)) + 1)
    factor = next((x for x in candidates if (num % x == 0)), None)
    return ([factor] + prime_factors(num / factor, factor) if factor else [num])

def factorize(num):
    """Factorize a number returning ocurrences of its prime factors"""
    return ((f, iterlen(group)) for (f, group) in groupby(prime_factors(num)))

def greatest_common_divisor(a, b):
    """Return greatest common divisor of a and b"""
    return (greatest_common_divisor(b, a % b) if b else a)

def least_common_multiple(a, b): 
    """Return least common multiples of a and b"""
    return (a * b) / greatest_common_divisor(a, b)

def least_common_multiple_list(nums): 
    """Return least common multiples of nums"""
    return reduce(least_common_multiple, nums)

def transpose(matrix):
    """Transpose bidimensional matrix."""
    return zip(*matrix)

def triangle_number(x):
    """The nth triangle number is defined as the sum of [1,n] values."""
    return (x*(x+1))/2

def pentagonal_number(n):
    """Nth pentagonal number: 1, 5, 12, 22, 35, ..."""
    return n*(3*n-1)/2

def hexagonal_number(n):
    """Nth hexagonal number: 1, 6, 15, 28, 45, ..."""
    return n*(2*n-1)

def is_pentagonal(n):
    """Return True if n is a pentagonal number"""
    return (n >= 1) and isinteger((1+sqrt(1+24*n))/6.0)

def is_hexagonal(n):
    """Return True if n is an hexagonal number"""
    return (n >= 1) and isinteger((1+sqrt(1+8*n))/4.0)

def is_pythagorean((a, b, c)):
    """Return True if a**2 = b**2 + c**2 (a, b, c must be integers)"""
    return (a**2 == b**2 + c**2)

def n_combinations(n, k):
    """Combinations of k elements from a group of n"""
    return cartesian_product(xrange(n-k+1, n+1)) / factorial(k)

def get_cardinal_name(num):
    """Get cardinal name for number (0 to 1000 only)"""
    numbers = {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
        6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
        15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
        19: "nineteen", 20: "twenty", 30: "thirty", 40: "forty",
        50: "fifty", 60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}
    def get_tens(num, withand=False):
        header = (withand and num) and "and" or None
        if num == 0 and withand:
            return
        elif num <= 20:
            s = numbers[num]
        else:
            a, b = num_from_digits(num)
            s = b and "%s-%s"%(numbers[10*a], numbers[b]) or "%s"%numbers[10*a]
        return " ".join(nonvoid([header, s]))
    if num < 100:
        return get_tens(num)
    elif num < 1000:
        a, b, c = num_from_digits(num)
        tens = get_tens(10*b+c, True)
        return " ".join(nonvoid([numbers[a], "hundred", tens]))
    elif num == 1000:
        return "one thousand"
    raise ValueError, "not supported"

def get_divisors(num):
    """Get all divisors from num in a list (including 1 and itself)"""
    factors = [[pow(a, c) for c in range(0, b+1)] for a, b in factorize(num)]
    return sorted(product(nums) for nums in cartesian_product(*factors))

def amical_numbers(start=1):
    """Generate amical numbers pair from start"""
    def get_amical(x):
        sum_proper_divisors = lambda num: sum(get_divisors(num)[:-1])
        sum1 = sum_proper_divisors(x)
        if x != sum1 and sum_proper_divisors(sum1) == x:
            return x, sum1
    return take_every(2, nonvoid(imap(get_amical, count(start))))

def check_perfect(num):
    """Return -1 if num is deficient, 0 if perfect, +1 if abundant"""
    return cmp(sum(get_divisors(num)[:-1]), num)

def permutations(lst):
    """Return permutations of elements in lst"""
    if lst:
        for x in lst:
            for y in permutations(remove_from_sequence(lst, x)):
                yield (x,)+y
    else: 
        yield ()

def combinations(lst, k):
    """Return combinations of k elements take from a list"""
    if lst and k>0:
        for x in lst:
            for y in combinations(remove_from_sequence(lst, x), k-1):
                yield (x,)+y
    else: 
        yield ()

def get_nth_permutation(n, lst):
    """Get nth element in permutations of elements from lst"""
    if not lst:
        return []
    div, mod = divmod(n, factorial(len(lst)-1))
    element = lst[div]
    return [element]+get_nth_permutation(mod, remove_from_sequence(lst, element))

def n_digits(num, base=10):
    """Return number of digits of num (expressed in base 'base')"""
    return int(log10(num)/log10(base)) + 1

def get_decimals(num, div, current=([], [])):
    """Return a tuple (integer_part, decimal_part, cycle_length) for num/div"""
    headtail = lambda lst: (lst[0], lst[1:])
    memory, values = current
    if values and num == 0:
        integer, decimals = headtail(values)
        return integer, decimals, 0
    elif num in memory:
        integer, decimals = headtail(values)
        lencycle = len(memory) - memory.index(num)
        return integer, decimals, lencycle
    a, b = divmod(num, div)
    return get_decimals(10*b, div, (memory+[num], values+[a]))

def is_pandigital(digits, needed=tuple(range(1, 10))):
    """Return True if digits form a pandigital number"""
    if not digits:
        return False
    return (tuple(sorted(digits)) == tuple(needed))

def memoize(f, maxcache=None, cache={}):
    """Decorator to keep a cache of input/output for a given function"""
    cachelen = [0]
    def g(*args, **kwargs):
        key = (f, tuple(args), frozenset(kwargs.items()))
        if maxcache is not None and cachelen[0] >= maxcache:
            return f(*args, **kwargs)
        if key not in cache:
            cache[key] = f(*args, **kwargs)
            cachelen[0] += 1
        return cache[key]
    return g

class tail_recursive(object):
    """Michele Simionato's version of a tail recursive decorator.""" 
    CONTINUE = object() # sentinel

    def __init__(self, func):
        self.func = func
        self.firstcall = True

    def __call__(self, *args, **kwd):
        try:
            if self.firstcall: # start looping
                self.firstcall = False
                while True:
                    result = self.func(*args, **kwd)
                    if result is self.CONTINUE: # update arguments
                        args, kwd = self.argskwd
                    else: # last call
                        break
            else: # return the arguments of the tail call
                self.argskwd = args, kwd
                return self.CONTINUE
        except: # reset and re-raise
            self.firstcall = True
            raise
        else: # reset and exit
            self.firstcall = True
            return result
