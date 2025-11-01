# calculator/__init__.py

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .addition import add
from .subtraction import subtract
from .multiplication import multiply
from .division import divide

def main():
    print("Welcome to the Calculator!")
    # Example usage of the calculator functions
    print(f"2 + 3 = {add(2, 3)}")
    print(f"5 - 2 = {subtract(5, 2)}")
    print(f"4 * 6 = {multiply(4, 6)}")
    print(f"8 / 2 = {divide(8, 2)}")

if __name__ == "__main__":
    main()