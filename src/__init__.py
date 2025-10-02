# Al-Kafeel Book Extractor Package
# Created by MiniMax Agent

__version__ = "1.0.0"
__author__ = "MiniMax Agent"
__email__ = "minimax@example.com"
__description__ = "Extract PDF books from Al-Kafeel Digital Library"

from .alkafeel_extractor import (
    AlkafeelExtractor,
    extract_single_book,
    extract_multiple_books
)

__all__ = [
    "AlkafeelExtractor",
    "extract_single_book",
    "extract_multiple_books"
]
