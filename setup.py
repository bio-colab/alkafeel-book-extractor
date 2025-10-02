#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup configuration for Al-Kafeel Book Extractor
Created by: Eylias Sharar
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="alkafeel-book-extractor",
    version="1.0.0",
    author="Eylias Sharar",
    author_email="aliasbio80@gmail.com",
    description="Extract PDF books from Al-Kafeel Digital Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bio-colab/alkafeel-book-extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    install_requires=[
        "playwright>=1.40.0",
        "beautifulsoup4>=4.12.2",
        "lxml>=4.9.3",
        "requests>=2.31.0",
        "click>=8.1.7",
        "tqdm>=4.66.1",
        "colorama>=0.4.6",
        "PyPDF2>=3.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.1",
            "black>=23.9.1",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "alkafeel-extract=main:cli",
        ],
    },
    keywords=[
        "pdf-extraction",
        "web-automation",
        "digital-library",
        "book-extractor",
        "playwright",
        "alkafeel",
        "academic-research",
    ],
    project_urls={
        "Bug Reports": "https://github.com/bio-colab/alkafeel-book-extractor/issues",
        "Source": "https://github.com/bio-colab/alkafeel-book-extractor",
        "Documentation": "https://github.com/bio-colab/alkafeel-book-extractor#readme",
    },
    include_package_data=True,
    zip_safe=False,
)
