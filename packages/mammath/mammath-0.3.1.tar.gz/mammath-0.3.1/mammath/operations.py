import math
from .helper import parse_standard, parse_to_standard
from .sequences import terms_in_range

"""
OPERATIONS
"""

def add(*args):
    """
    Adds any amount of numbers
    """
    return sum(args)

def subtract(a, *args):
    """
    Subtracts any amount of numbers
    """
    return a - sum(args)

def multiply(*args):
    """
    Multiplies any amount of numbers
    """
    x = 1
    y = 0
    while y < len(args):
        x = x*args[y]
        y+=1
    return x

def divide(a, *args):
    """
    Divides any amount of numbers
    """
    return a / multiply(*args)


def listMultiply(lis):
    """
    Returns the product of a list
    """
    x = 1
    y = 0
    while y < len(lis):
        x = x*lis[y]
        y+=1
    return x

def power(base, exponent):
    """
    Returns base^exponent
    """
    
    if exponent == 0:
        return 1
    if exponent > 0:
        return (base * power(base, exponent - 1))
    return 1 /(base * power(base, -exponent - 1))

def sqrt(a):
    return a ** (1/2)

def csqrt(a):
    if a < 0:
        return 1j*sqrt(-a)
    return sqrt(a)

def root(a, b):
    """
    Returns the bth root of a
    """

    return a**(1/b)

def factorial(n):
    """
    Performs the factorial operation on any real number. 
    For the extended domain of this function, the the Gamma and Pi functions.
    """
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def log(num, base):
    """
    Returns the logarithm of num with the given base
    """
    
    return math.log(num, base)

def ln(num):
    """
    Returns the natural log (log base e) of num
    """
    
    return log(num, math.e)

def sig_fig(num, figs):
    """
    Rounds num to figs significant figures
    """
    
    rounded = round(num, figs - int(math.floor(math.log10(abs(num)))) - 1)
    return rounded

def abs_val(num):
    """
    Returns the absoltue value of num
    """
    
    return math.fabs(num)

def remainder(a, b):
    """
    Returns the remainder when a is divided by b
    """
    
    return a % b

def HCF(a, b):
    """
    Returns the highest common factor of a and b
    """
    
    a, b = max(a, b), min(a, b)
    while b!=0:
        a, b = b, a % b
    return a

def LCM(a, b):
    """
    Returns the lowest common multiple of a and b
    """
    
    return (a*b)/HCF(a, b)
    
def summate(n, a, b):
    return sum(terms_in_range(n, a, b))

def product(n, a, b):
    return listMultiply(terms_in_range(n, a, b))

def nchoosek(n, k):
    """
    Returns nCk given by the formula n!/k!(n-k)!
    """
    return factorial(n)/(factorial(n-k)*factorial(k))

def permutations(n, r):
    """
    Returns nPr given by the formula n!/(n-k)!
    """
    return factorial(n)/factorial(n-r)

def to_standard_form(n):
    """
    Converts the integer n to standard form as a tuple, (a, b) where n = a * 10 ** b
    """
    t = 0
    while n > 10:
        n /= 10
        t += 1
    return n, t

def standard_add(*args, rt=to_standard_form):
    """
    Adds any number of numbers in standard form, given in (a, b) where a * 10 ** b
    """
    if isinstance(args[0], tuple):        
        return parse_to_standard(rt(add(*[i[0] * 10 ** i[1] for i in args])))
    else:
        args = list(args)
        for i in range(0, len(args)):
            args[i] = parse_standard(args[i])
        return parse_to_standard(rt(add(*[i[0] * 10 ** i[1] for i in args])))

def standard_mult(*args, rt=to_standard_form):
    """
    Multiplies any number of numbers in standard form, given in (a, b) where a * 10 ** b
    """
    if isinstance(args[0], tuple):        
        return parse_to_standard(rt(multiply(*[i[0] * 10 ** i[1] for i in args])))
    else:
        args = list(args)
        for i in range(0, len(args)):
            args[i] = parse_standard(args[i])
        return parse_to_standard(rt(multiply(*[i[0] * 10 ** i[1] for i in args])))

def standard_div(a, *args, rt=to_standard_form):
    """
    Divides one number by any number of numbers, all in standard form, given in (a, b) where a * 10 ** b
    """
    if isinstance(args[0], tuple):
        print(a[0] * 10 ** a[1])
        return parse_to_standard(rt(divide(a[0] * 10 ** a[1], *[i[0] * 10 ** i[1] for i in args])))
    else:
        args = list(args)
        for i in range(0, len(args)):
            args[i] = parse_standard(args[i])
        return parse_to_standard(rt(divide(parse_standard(a)[0] * 10 ** parse_standard(a)[1], *[i[0] * 10 ** i[1] for i in args])))

def standard_sub(a, *args, rt=to_standard_form):
    """
    Subtracts one number by any number of numbers, all in standard form, given in (a, b) where a * 10 ** b
    """
    if isinstance(args[0], tuple):        
        return parse_to_standard(rt(subtract(a[0] * 10 ** a[1], *[i[0] * 10 ** i[1] for i in args])))
    else:
        args = list(args)
        for i in range(0, len(args)):
            args[i] = parse_standard(args[i])
        
        return parse_to_standard(rt(subtract(parse_standard(a)[0]*10**parse_standard(a)[1], *[i[0] * 10 ** i[1] for i in args])))

def binomialdist(n, x, p):
    """
    The probability of x successful events in n attempts where the probability of success is p.
    """
    return factorial(n) * p ** x * (1 - p) ** (n - x) / (factorial(x) * factorial(n - x))
    
"""
END OF OPERATIONS
"""

