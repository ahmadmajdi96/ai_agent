# fast_api/__init__.py

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .main import create_app

def main():
    app = create_app()
    app.run()

if __name__ == "__main__":
    main()