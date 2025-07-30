# code_writer.py
# Tool to generate code based on prompt (basic template or LLM-generated)

def generate_code(prompt: str) -> str:
    # Example template-based logic — later connect with an LLM code generator
    if "fibonacci" in prompt.lower():
        return """```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=' ')
        a, b = b, a + b
```"""
    elif "factorial" in prompt.lower():
        return """```python
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)
```"""
    else:
        return "🤖 Code generation not available for this prompt."
