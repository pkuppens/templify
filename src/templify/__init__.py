"""
Templify - Advanced templating features for Python
"""

__version__ = "0.1.0"

from .core import render_data, render_pdf_file, render_text

__all__ = ["render_text", "render_data", "render_pdf_file", "render_jinja2"]
