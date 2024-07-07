"""
Utilities
"""

from random import randint, sample
from nzmath.arith1 import product as prod

def HitRet():
    """
    pause to wait for key input
    """
    print("Hit Return!")
    input("\x1b[1A\x1b[12C")
    print("\x1b[1A\x1b[2K")

def again(func, i = 5):
    """
    Input
        func: function to be repeated
        i: minimum of repeated times, positive integer
    Output
        repeat func at least i times
        after that ask 'again (y/N) ?' and wait for key input
        repeat func once more if key input is 'y' or 'Y' else end func
    """
    if i <= 0:
        raise ValueError("i shoud be positive, execute at least once")
    while i:
        func()
        i -= 1
        if not i:
            print("again? (y/N) ")
            i += (input("\x1b[1A\x1b[14C") == ('y' or 'Y'))
            print("\x1b[1A\x1b[2K\x1b[1A")

def strInt(n, d = 50):
    """
    Input
        n: integer
        d: upper bound of digits, d >= 5
    Output
        string of integer n at most in d digits (without \n)
            if n does not exceed d digits, then str(n) as ordinary
            else upper d - 3 digits of n and '...' are concatenated
    """
    if d < 5:
        raise ValueError("Digits upper bound d >= 5.")
    s = str(n); l = len(s)
    if l <= d:
        return s 
    else:
        return s[-l : d - 3 - l] + 3*'.'

def randFactLists(P, ub):
    """
    Input
        P: list of possible primes p below
        ub: upper bound of len(a), len(f), e below
    Output
        a: random list of factor lists f of pairs (p, e) = (prime, exponent)
    """
    a = []
    for _ in range(randint(1, ub)):
        f = sample(P, randint(1, ub))
        for k in range(len(f)):
            f[k] = (f[k], randint(1, ub))
        a.append(f)
    return a

def lcm_def(*a):
    """
    Input
        a: non-zero integers
    Output
        cm: the set of positive common multiples of a at most abs(prod(a))
        min(cm): the least common multiple of a
    """
    a = {abs(i) for i in a}
    if a == set() or min(a) == 0:
        raise ValueError("Non-zero integers are required.")
    u = prod(a) + 1
    i = a.pop()
    cm = set(range(i, u, i))
    for i in a:
        cm = set.intersection(cm, set(range(i, u, i)))
    return cm, min(cm)

def allDivisors_def(a):
    """
    Input
        a: positive integer
    Output
        the set of positive divisors of a
    """
    if a <= 0:
        raise ValueError("Positive integer is required.")
    sqrta, s = int(a**.5), {1, a}
    for d in range(2, sqrta + 1):
        q, r = divmod(a, d)
        if r == 0:
            s = s | {d, q}
    return s

def gcd_def(*a):
    """
    Input
        a: integers, at least one non-zero
    Output
        cd: the set of positive common divisors of a
        max(cd): the greatest common divisor of a
    """
    a = {abs(i) for i in a if i}
    if a == set():
        raise ValueError("At least one non-zero integer is required.")
    cd = set.intersection(*[allDivisors_def(i) for i in a])
    return cd, max(cd)

def countDivisors_def(a):
    """
    Input
        a: positive integer
    Output
        the number of positive divisors of a
    """
    return len(allDivisors_def(a))

def sumDivisors_def(a):
    """
    Input
        a: positive integer
    Output
        the sum of divisors of a
    """
    return sum(allDivisors_def(a))

