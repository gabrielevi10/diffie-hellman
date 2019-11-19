#!/usr/bin/env python3

import secrets

def fast_expo(base, exp, prime):
  base %= prime
  answer = 1

  while exp > 0:
    if exp % 2 == 1:
      answer = (answer * base) % prime
    exp //= 2
    base = (base * base) % prime

  return answer

def millerRabin(x):
  d = n-1
  while d % 2 is 0:
    d /= 2
  random = secrets.choice(range(2, n-2))
  x = fast_expo(random, d, n)
  if x == 1 or x == n-1: 
    return True
  while d is not n-1:
    x = (x*x) % n
    d *= 2
    if x == 1: 
      return False
    if x == n-1:
      return True
  return False

def generateRandomNumber():
  x = int('inf') 
  print(secrets.choice(2, x))

generateRandomNumber()