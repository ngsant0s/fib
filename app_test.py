import unittest
import app

class AppTest(unittest.TestCase):
    def test_fibonacci(self):
        self.assertEqual(app.fibonacci(15), 610)
    
if __name__ == '__main__':
    unittest.main()