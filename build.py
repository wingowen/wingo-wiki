#!/usr/bin/env python3
"""
Wrapper script to run the modular build system
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.build import main

if __name__ == "__main__":
    main()
