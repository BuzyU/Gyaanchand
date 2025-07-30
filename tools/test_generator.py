# test_generator.py
# Tool to generate test cases for functions/code

def generate_tests(code_description: str) -> str:
    if "fibonacci" in code_description.lower():
        return """```python
import unittest

class TestFibonacci(unittest.TestCase):
    def test_fibonacci(self):
        self.assertEqual(fibonacci(5), [0, 1, 1, 2, 3])

if __name__ == '__main__':
    unittest.main()
```"""
    elif "factorial" in code_description.lower():
        return """```python
import unittest

class TestFactorial(unittest.TestCase):
    def test_factorial(self):
        self.assertEqual(factorial(5), 120)

if __name__ == '__main__':
    unittest.main()
```"""
    else:
        return "📦 No test cases available for the given code."
