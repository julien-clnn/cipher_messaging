import random

def decomposeForPrimalityTest(n):
    """Intermediate function for Rabin Miller Primality test

    Args:
        n (int): an integer we try to apply Rabin Miller Primality test
    Returns:
        s: the greatest exponent
        d: an odd integer
    """
    s = 0
    d = n - 1

    while d % 2 == 0:
        s += 1
        d //= 2

    return s, d

def proofOfMiller(n, a):
    """Verify if the number 'a' is a proof of Miller for the primality of 'n'

    Args:
        n (int): an integer we try to apply Rabin Miller Primality test 
        a (int): the proof of Miller
    Returns:
        bool: this returns 'False' if 'a' is a proof of Miller, returns 'True' if 'a' is not a proof of Miller
    """
    s, d = decomposeForPrimalityTest(n)
    
    x = modularExponentiation(a, d, n)
    if x == 1 or x == n - 1:
        return False
    
    for _ in range(s - 1):
        x = modularExponentiation(x, 2, n)
        if x == n - 1:
            return False
    
    return True

def rabinMiller(n, k=5):
    """Use to determine if an integer 'n' is probably prime (probabilistic)

    Args:
        n (int): an integer we try to apply Rabin Miller Primality test 
        k (int): number of rounds
    Returns:
        bool: this returns 'True' if 'n' is probably prime, this returns 'False' if this is not the case
    """
    # Increase k to increase the fiability of the primality test (reduce the error)
    for _ in range(k): 
        a = random.randint(2, n - 1)
        if proofOfMiller(n, a):
            return False
    
    return True

def isPrime(n, k=5):
    """Use to determine if an integer 'n' is prime (use of Rabin Miller test)

    Args:
        n (int): an integer we try to apply for the primality test 
        k (int): number of rounds
    Returns:
        bool: this returns 'True' if 'n' is prime, this returns 'False' if this is not the case
    """
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    return rabinMiller(n, k)

def pgcd(a, b):
    """Use in order to determine the greatest common divisor (PGCD in french)

    Args:
        a (int): a first integer 
        b (int): a second integer
    Returns:
        int: this returns the greatest common divisor
    """
    while b:
        a, b = b, a % b
    return a

def modularInverse(a, modulo):
    """Applying the modular inverse operation. Use to process the private key based on the public key.

    Args:
        a (int): an integer we want to find the inverse mod 'm'
        m (int): modulo
    Returns:
        : the modular inverse
    """
    m0, x0, x1 = modulo, 0, 1
    
    while a > 1:
        q = a // modulo
        modulo, a = a % modulo, modulo
        x0, x1 = x1 - q * x0, x0
    
    return x1 + m0 if x1 < 0 else x1

def modularExponentiation(base, exponent, modulo):
    """Applying the modular exponentiation operation

    Args:
        base (int): the number we want to compute
        exponent (int): the exponent the base is compute
        modulo (int): modulo
    Returns:
        int: this returns the result of the operation
    """
    result = 1
    base = base % modulo
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulo
        exponent = exponent // 2
        base = (base * base) % modulo

    # (base^exponent) mod modulo
    return result

def generatePrimeNumber(prime_length, seed=None):
    """_summary_

    Args:
        prime_length (int): _description_
    Returns:
        _type_: _description_
    """
    # Seed
    if seed is not None:
        random.seed(seed)

    # A number to test for primality test
    number_to_test = random.getrandbits(prime_length)
    
    # We do it until we find a correct number
    while not isPrime(number_to_test):
        number_to_test = random.getrandbits(prime_length)
    
    return number_to_test