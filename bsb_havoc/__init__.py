"""
BSB Havoc - The World's Most Powerful Load Testing Tool
Professional, High-Performance Distributed Load Testing Engine
"""

__version__ = "1.0.0"
__author__ = "Black Spammer Bd"
__license__ = "MIT"

from .cli import main
from .engine import HavocEngine

__all__ = ['main', 'HavocEngine']
