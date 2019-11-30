import sys
sys.path.append('../src/')

import unittest
from Math import Math

class TestMathMethods(unittest.TestCase):
    """
    Implements tests for Math Module.
    """
    def test_fast_exponentiation(self):
        power = Math.fast_exponentiation
        
        self.assertEqual(power(3, 2, 4), 1)
        self.assertEqual(power(10, 9, 6), 4)
        self.assertEqual(power(450, 768, 517), 34)
        self.assertEqual(power(0, 100, 4), 0)
        self.assertEqual(power(100, 100, 100), 0)
        self.assertEqual(power(71045970, 41535484, 64735492), 20805472)
        self.assertEqual(power(0, 0, 7), None)

    def test_miller_rabin(self):
        primes_count = 0
        total = 10000
        for i in range(total):
            if Math.miller_rabin_test(i + 1):
                primes_count += 1
        
        self.assertEqual(primes_count, 1229)
