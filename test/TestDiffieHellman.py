import sys
sys.path.append('../src/')

import unittest
from Math import Math
from DiffieHellman import DiffieHellman

class TestDiffieHellmanMethods(unittest.TestCase):
    """
    Implements tests for DiffieHellman Module.
    """
    def test_diffie_hellman_exchange(self):
        """
        Simulates a diffie-hellman key exchange
        """

        # Alice and Bob agree for a secure generator and prime 
        base, modulus = Math.generate_generator_and_prime(128) 
        alice = DiffieHellman(base, modulus)
        bob = DiffieHellman(base, modulus)

        # Alice calculates her exponentiation
        alice_result = alice.get_result()

        # Bob calculates his exponentiation
        bob_result = bob.get_result()

        # so, they exchange the result and calculates the shared secret
        secret_alice = alice.calculate_shared_secret(bob_result)
        secret_bob = bob.calculate_shared_secret(alice_result)

        # And if right, both secrets must be equal.
        self.assertEqual(secret_alice, secret_bob)

        
