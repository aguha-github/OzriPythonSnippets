import unittest

# function to add numbers
def add_numbers(num1, num2):
    return num1 + num2

class MySimpleTests(unittest.TestCase):

    def test_calc(self):
        result = add_numbers(7, 12)
        self.assertEqual(19, result)


if __name__ == '__main__':
    unittest.main()