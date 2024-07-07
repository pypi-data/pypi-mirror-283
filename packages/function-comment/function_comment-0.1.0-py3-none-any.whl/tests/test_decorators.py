# tests/test_decorators.py
import unittest
from function_comment.decorators import bbkp, ujmp

class TestDecorators(unittest.TestCase):
    def test_function_commented_out(self):
        @bbkp
        @ujmp
        def some_function():
            return "This should not be executed"

        result = some_function()
        self.assertIsNone(result)

    def test_function_normal(self):
        @ujmp
        def normal_function():
            return "This should be executed"

        result = normal_function()
        self.assertEqual(result, "This should be executed")

if __name__ == '__main__':
    unittest.main()
