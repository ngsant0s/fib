import unittest
from app import fibonacci

class TestFibonacci(unittest.TestCase):
    def test_fibonacci(self):
        self.assertEqual(fibonacci(15), 610)
    
if __name__ == '__main__':
    unittest.main()