#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Al-Kafeel Library Book Extractor - Main CLI Interface
====================================================

Command-line interface for extracting PDF books from Al-Kafeel Digital Library.

Created by: Eylias Sharar
Date: 2025-10-02
License: MIT

Usage Examples:
    # Extract single book
    python main.py extract "https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b"
    
    # Extract multiple books from file
    python main.py batch-extract urls.txt
    
    # Extract with custom output directory
    python main.py extract "URL" --output ./my_books
    
    # Extract with verbose logging
    python main.py extract "URL" --verbose
"""

import asyncio
import sys
import os
from pathlib import Path

import click
from colorama import Fore, Style, init as colorama_init

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from alkafeel_extractor import AlkafeelExtractor, extract_single_book, extract_multiple_books

# Initialize colorama
colorama_init(autoreset=True)


@click.group()
@click.version_option(version='1.0.0', prog_name='Al-Kafeel Book Extractor')
def cli():
    """
    🚀 Al-Kafeel Library Book Extractor
    
    A powerful tool for extracting PDF books from Al-Kafeel Digital Library.
    
    Created by Eylias Sharar - EB software solutions team
    """
    print_banner()


def print_banner():
    """Print the application banner."""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
{Fore.CYAN}║                                                              ║
{Fore.CYAN}║         Al-Kafeel Library Book Extractor v1.0.0              ║
{Fore.CYAN}║                                                              ║
{Fore.CYAN}║              Created by Eylias Sharar                        ║
{Fore.CYAN}║              EB doftware solutions team                      ║
{Fore.CYAN}║                                                              ║
{Fore.CYAN}║     Extract PDF books from library.alkafeel.net              ║
{Fore.CYAN}║                                                              ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)


@cli.command()
@click.argument('url')
@click.option('--output', '-o', default='output', 
              help='Output directory for extracted files (default: output)')
@click.option('--verbose', '-v', is_flag=True, 
              help='Enable verbose logging')
def extract(url, output, verbose):
    """
    Extract a single book from Al-Kafeel library.
    
    URL: The book URL from library.alkafeel.net
    
    Example:
        python main.py extract "https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b"
    """
    click.echo(f"{Fore.BLUE}🔄 Starting extraction...")
    click.echo(f"{Fore.BLUE}📖 URL: {url}")
    click.echo(f"{Fore.BLUE}📁 Output: {output}")
    
    try:
        # Run extraction
        result = asyncio.run(extract_single_book(url, output_dir=output, verbose=verbose))
        
        if result['success']:
            click.echo(f"\n{Fore.GREEN}✅ SUCCESS!")
            click.echo(f"{Fore.GREEN}📚 Book ID: {result['book_id']}")
            click.echo(f"{Fore.GREEN}💾 PDF saved: {result['pdf_path']}")
            click.echo(f"{Fore.GREEN}📊 Size: {result['pdf_size_bytes']:,} bytes")
            click.echo(f"{Fore.GREEN}⏱️  Duration: {result['extraction_duration']}")
            
            if 'metadata_path' in result:
                click.echo(f"{Fore.BLUE}📋 Metadata: {result['metadata_path']}")
        else:
            click.echo(f"\n{Fore.RED}❌ FAILED!")
            click.echo(f"{Fore.RED}🔥 Error: {result.get('error', 'Unknown error')}")
            click.echo(f"{Fore.RED}⏱️  Duration: {result.get('extraction_duration', 'N/A')}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        click.echo(f"\n{Fore.YELLOW}⚠️  Extraction cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"\n{Fore.RED}💥 Unexpected error: {e}")
        sys.exit(1)


@cli.command('batch-extract')
@click.argument('urls_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='output', 
              help='Output directory for extracted files (default: output)')
@click.option('--verbose', '-v', is_flag=True, 
              help='Enable verbose logging')
@click.option('--continue-on-error', is_flag=True, 
              help='Continue extraction even if some books fail')
def batch_extract(urls_file, output, verbose, continue_on_error):
    """
    Extract multiple books from a file containing URLs.
    
    URLS_FILE: Text file with one URL per line
    
    Example:
        python main.py batch-extract book_urls.txt --output ./extracted_books
    """
    click.echo(f"{Fore.BLUE}📚 Starting batch extraction...")
    click.echo(f"{Fore.BLUE}📄 URLs file: {urls_file}")
    click.echo(f"{Fore.BLUE}📁 Output: {output}")
    
    try:
        # Read URLs from file
        with open(urls_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not urls:
            click.echo(f"{Fore.RED}❌ No valid URLs found in file")
            sys.exit(1)
        
        click.echo(f"{Fore.GREEN}📊 Found {len(urls)} URLs to process")
        
        # Run batch extraction
        results = asyncio.run(extract_multiple_books(urls, output_dir=output, verbose=verbose))
        
        # Display final results
        click.echo(f"\n{Fore.CYAN}📊 BATCH EXTRACTION SUMMARY")
        click.echo(f"{Fore.CYAN}{'='*50}")
        click.echo(f"{Fore.GREEN}✅ Successful: {len(results['successful_extractions'])}")
        click.echo(f"{Fore.RED}❌ Failed: {len(results['failed_extractions'])}")
        click.echo(f"{Fore.BLUE}📈 Success Rate: {results['success_rate']:.1f}%")
        
        if results['failed_extractions'] and not continue_on_error:
            click.echo(f"\n{Fore.YELLOW}⚠️  Some extractions failed. Use --continue-on-error to ignore failures.")
        
        # Save batch results
        import json
        batch_results_file = Path(output) / "batch_results.json"
        with open(batch_results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        click.echo(f"\n{Fore.BLUE}📋 Batch results saved: {batch_results_file}")
        
    except KeyboardInterrupt:
        click.echo(f"\n{Fore.YELLOW}⚠️  Batch extraction cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"\n{Fore.RED}💥 Unexpected error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--output', '-o', default='output', 
              help='Output directory to setup (default: output)')
def setup(output):
    """
    Setup the environment and install browser dependencies.
    
    This command will:
    1. Create output directories
    2. Install Playwright browsers
    3. Verify the installation
    """
    click.echo(f"{Fore.BLUE}🔧 Setting up Al-Kafeel Book Extractor...")
    
    try:
        # Create output directories
        output_path = Path(output)
        directories = ['pdfs', 'metadata', 'screenshots', 'logs']
        
        for dir_name in directories:
            dir_path = output_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            click.echo(f"{Fore.GREEN}✓ Created directory: {dir_path}")
        
        # Install Playwright browsers
        click.echo(f"\n{Fore.BLUE}📥 Installing Playwright browsers...")
        import subprocess
        
        try:
            result = subprocess.run(['playwright', 'install', 'chromium'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                click.echo(f"{Fore.GREEN}✓ Playwright browsers installed successfully")
            else:
                click.echo(f"{Fore.YELLOW}⚠️  Playwright installation warning: {result.stderr}")
                
        except FileNotFoundError:
            click.echo(f"{Fore.RED}❌ Playwright not found. Make sure it's installed:")
            click.echo(f"{Fore.BLUE}   pip install playwright")
            sys.exit(1)
        
        # Verify installation
        click.echo(f"\n{Fore.BLUE}🔍 Verifying installation...")
        
        # Test import
        try:
            from playwright.async_api import async_playwright
            click.echo(f"{Fore.GREEN}✓ Playwright import successful")
        except ImportError as e:
            click.echo(f"{Fore.RED}❌ Playwright import failed: {e}")
            sys.exit(1)
        
        click.echo(f"\n{Fore.GREEN}🎉 Setup completed successfully!")
        click.echo(f"{Fore.BLUE}💡 You can now use the extractor:")
        click.echo(f"{Fore.BLUE}   python main.py extract \"YOUR_BOOK_URL\"")
        
    except Exception as e:
        click.echo(f"\n{Fore.RED}💥 Setup failed: {e}")
        sys.exit(1)


@cli.command()
def test():
    """
    Run a test extraction with a sample book URL.
    
    This will test the extractor with a known working book URL
    to verify everything is working correctly.
    """
    test_url = "https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b"
    
    click.echo(f"{Fore.BLUE}🧪 Running test extraction...")
    click.echo(f"{Fore.BLUE}📖 Test URL: {test_url}")
    
    try:
        result = asyncio.run(extract_single_book(test_url, output_dir='test_output', verbose=True))
        
        if result['success']:
            click.echo(f"\n{Fore.GREEN}✅ TEST PASSED!")
            click.echo(f"{Fore.GREEN}📚 The extractor is working correctly")
            click.echo(f"{Fore.GREEN}💾 Test file saved: {result['pdf_path']}")
        else:
            click.echo(f"\n{Fore.RED}❌ TEST FAILED!")
            click.echo(f"{Fore.RED}🔥 Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"\n{Fore.RED}💥 Test failed with exception: {e}")
        sys.exit(1)


@cli.command()
def info():
    """
    Display information about the extractor and supported URLs.
    """
    info_text = f"""
{Fore.CYAN}📖 Al-Kafeel Library Book Extractor Information
{Fore.CYAN}{'='*50}

{Fore.GREEN}🎯 Purpose:
{Fore.WHITE}   Extract PDF books from Al-Kafeel Digital Library (library.alkafeel.net)

{Fore.GREEN}✨ Features:
{Fore.WHITE}   • Automatic iframe content detection
   • Base64 PDF decoding
   • Batch processing support
   • Detailed logging and metadata
   • Progress tracking with colored output
   • Screenshot capture for debugging

{Fore.GREEN}🔗 Supported URLs:
{Fore.WHITE}   • https://library.alkafeel.net/dic/book/?e=BOOK_ID
   • Must be from library.alkafeel.net domain
   • Must contain '/dic/book/' path

{Fore.GREEN}📁 Output Structure:
{Fore.WHITE}   output/
   ├── pdfs/           # Extracted PDF files
   ├── metadata/       # Extraction metadata (JSON)
   ├── screenshots/    # Page screenshots
   └── logs/           # Detailed logs

{Fore.GREEN}👨‍💻 Created by:
{Fore.WHITE}   Eylias SHarar - EB software solutions team

{Fore.GREEN}📄 License:
{Fore.WHITE}   MIT License

{Fore.GREEN}🔧 Requirements:
{Fore.WHITE}   • Python 3.8+
   • Playwright (with Chromium)
   • Internet connection

{Fore.BLUE}💡 Usage Examples:
{Fore.WHITE}   # Extract single book
   python main.py extract "BOOK_URL"
   
   # Extract multiple books
   python main.py batch-extract urls.txt
   
   # Run test
   python main.py test
   
   # Setup environment
   python main.py setup

{Fore.YELLOW}⚠️  Note:
{Fore.WHITE}   This tool is for educational and research purposes.
   Please respect the library's terms of service.
    """
    
    click.echo(info_text)


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}💥 Unexpected error: {e}")
        sys.exit(1)