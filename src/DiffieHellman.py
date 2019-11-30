#!/usr/bin/env python3

import sys
import secrets
from Math import Math

class DiffieHellman:
  """
  Encapsulate methods necessary to calculate the shared secret
  between two peers.
  """
  def __init__(self, generator : int, modulus : int): # agreed numbers
    self.__generator = generator
    self.__modulus = modulus
    self.__result, self.__exponent = self.__calculate_local_number()
  
  def __calculate_local_number(self):
    """
    Returns the random chosen exponent and to number to send
    to the other peer.
    """
    exponent = 2 + secrets.randbelow(sys.maxsize) # range [2, sys.maxsize + 1]
    result = Math.fast_exponentiation(self.__generator, exponent, self.__modulus)
    
    return result, exponent

  def calculate_shared_secret(self, received_number):
    """
    Calculates the shared secret having the received number and the exponent
    used for it's own operation
    """
    result = Math.fast_exponentiation(received_number, self.__exponent, self.__modulus)
    return result

  def get_result(self):
    """ get method for result """
    return self.__result
  
  def get_exponent(self):
    """ get method for exponent """
    return self.__exponent
