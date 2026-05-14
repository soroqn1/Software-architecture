import os
import sys

# Add the project root to sys.path to allow relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.lab2.ui.console import ConsoleUI

if __name__ == "__main__":
    app = ConsoleUI()
    try:
        app.start()
    except KeyboardInterrupt:
        print("\nПрограму завершено користувачем.")
        sys.exit(0)
