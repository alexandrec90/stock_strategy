"""Module: src.utils
Purpose: Utility scripts and tools for the stock_strategy project
Dependencies: pathlib, ast (built-in)
Output: Various utility outputs (file summaries, etc.)

Key Concepts:
- docstring_summarizer: Generates AI-friendly file summaries
- Utilities for maintaining project documentation and tooling
"""

# Import key utilities for easy access
from .docstring_summarizer import summarize_file, summarize_project

__all__ = ["summarize_project", "summarize_file"]
