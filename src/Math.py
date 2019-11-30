#!/usr/bin/env python3

import secrets
import queue
import threading
import os

class Math:
  """
  Math is a module with useful math operations,
  it hold methods for large probably primes generation,
  primality test and fast exponentiation.
  """
  @staticmethod
  def __generate_number(bits_size : int):
    """
    Private method to generate a number with `bits_size` bits.
    """
    #number = random.getrandbits(bits_size)
    number = secrets.randbits(bits_size)
    number |= (1 << bits_size - 1) | 1     # ensures that number is odd and most significant byte is one.
    return number

  @staticmethod
  def fast_exponentiation(base : int, exponent : int, prime : int):
    """
    Calculate the exponantiation of integers
    (base ^ exponent) % prime in logarithmic time: O(lg(exponent)).

    Returns an integer, the result of the operation.
    """
    if base == 0 and exponent == 0:
      return None

    base %= prime # ensure that base is in the range of the answer.
    result = 1    # starts with one because it's the neutral element of multiplication.

    while exponent > 0:
      if exponent & 1:
        result = (result * base) % prime
      
      # applies (base ^= 2) and divides exponent by 2.
      exponent //= 2
      base = (base * base) % prime
    
    return result # (base ^ exponent) % prime
  
  @staticmethod
  def miller_rabin_test(number : int, tests : int = 128):
    """
    Tests if `number` is a prime number.

    Returns a boolean value
    """
    if number == 3 or number == 2:
      return True      # random.randrange(2, number - 1) throws and exception when number is either 2 or 3.  

    if number <= 1 or number % 2 == 0: 
      if(number != 2):
        return False   # immediately discarts if number is even different from 2 or less than one.

    s = 0
    r = number - 1

    # Miller-Rabin test
    while r & 1 == 0:  # finds s and r
      s += 1
      r //= 2
    
    # Miller-Rabin test
    for _ in range(tests): 
      a = max(2, secrets.randbelow(number - 1))
      x = Math.fast_exponentiation(a, r, number)

      if x != 1 and x != number - 1:
        for i in range(1, s):
          if x == number - 1:
            break

          x = Math.fast_exponentiation(x, 2, number)
          if x == 1:
            return False
          
        if x != number - 1:
          return False

    return True

  @staticmethod
  def generate_prime_number(bits_size : int = 256):
    """
    Generates a, probably, prime number with length `bits_size` in bits. By default bits_size = 2014.

    Returns, probably, a prime.
    """
    prime = Math.__generate_number(bits_size)
    while not Math.miller_rabin_test(prime):
      prime += 2 

    return prime # returns a probably prime

  @staticmethod
  def generate_safe_prime_number(bits_size : int = 256):
    """
    Generates a safe prime number. A prime number p is safe is (p - 1) / 2 is a prime.
    """
    prime = Math.generate_prime_number(bits_size)       # gets prime number
    while not Math.miller_rabin_test((prime - 1) // 2): # tests if (p - 1) / 2 is prime.
      prime = Math.generate_prime_number(bits_size)     # if not, generates another prime number and retry.
    
    return prime

  @staticmethod
  def __generate_generator_and_prime(id : int, bits_size : int , result_queue : queue):
    """
    Generates a safe prime number p and the generator of Zp, Zp = (Z, * mod p)
    Returns both numbers
    """
    safe_prime = Math.generate_safe_prime_number(bits_size)         # Gets a safe prime number p
    factor = (safe_prime - 1) // 2                                  # derivate a prime from safe prime.

    generator = max(2, secrets.randbelow(safe_prime - 1)) # Choose a random integer in the range [2, safe_prime - 2]
    exponentation = Math.fast_exponentiation(generator, factor, safe_prime) 

    while exponentation == 1: # Some guy in stack overflow taugth this test to me.
      generator = max(2, secrets.randbelow(safe_prime - 1))
      exponentation = Math.fast_exponentiation(generator, factor, safe_prime) 

    result_queue.put((generator, safe_prime)) # save in the queue the result of the operation.

  @staticmethod
  def generate_generator_and_prime(bits_size : int = 256):
    """
    Generates a safe prime number p and the generator of Zp, Zp = (Z, * mod p)
    Returns both numbers
    """
    q = queue.Queue()
    # threads to search for prime and generator.
    threads = [threading.Thread(target=Math.__generate_generator_and_prime, 
              args=(i, bits_size, q)) for i in range(os.cpu_count() // 2)]

    for thread in threads:
      thread.daemon = True
      thread.start()
    
    return q.get() # returns the first result of the threads