# mini_calc/utils.py

def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Return the difference between two numbers."""
    return a - b

def multiply(a, b):
    """Return the product of two numbers."""
    return a * b

def divide(a, b):
    """Return the quotient of two numbers. Raises ValueError if divisor is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def power(base, exponent):
    """Return the base raised to the power of the exponent."""
    return base ** exponent

def modulus(a, b):
    """Return the remainder of the division of two numbers. Raises ValueError if divisor is zero."""
    if b == 0:
        raise ValueError("Cannot take modulus with zero.")
    return a % b