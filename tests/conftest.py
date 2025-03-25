"""
Pytest configuration file.
"""
import os
import sys
from pathlib import Path

# Add the tests directory to the Python path
tests_dir = Path(__file__).parent
sys.path.append(str(tests_dir.parent))
