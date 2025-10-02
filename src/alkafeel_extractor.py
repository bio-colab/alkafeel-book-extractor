#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Al-Kafeel Library Book Extractor
================================

A comprehensive tool for extracting PDF books from Al-Kafeel Digital Library
(library.alkafeel.net) using web automation and PDF decoding techniques.

Created by:Eylias Sharar
Date: 2025-10-02
License: MIT

This tool automatically:
1. Navigates to the book URL
2. Handles dynamic iframe content
3. Extracts base64-encoded PDF data
4. Decodes and saves the PDF file
5. Provides detailed extraction reports
"""

import asyncio
import base64
import json
import re
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse

from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup
import click
from tqdm import tqdm
import colorama
from colorama import Fore, Back, Style

# Initialize colorama for cross-platform colored output
colorama.init(autoreset=True)


class AlkafeelExtractor:
    """
    Main extractor class for Al-Kafeel Digital Library books.
    
    This class provides comprehensive functionality to extract PDF books
    from the Al-Kafeel Digital Library by handling dynamic content,
    iframe processing, and PDF decoding.
    """
    
    def __init__(self, output_dir: str = "output", verbose: bool = False):
        """
        Initialize the extractor.
        
        Args:
            output_dir (str): Directory to save extracted files
            verbose (bool): Enable verbose logging
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "pdfs").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
        (self.output_dir / "screenshots").mkdir(exist_ok=True)
        (self.output_dir / "logs").mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging(verbose)
        
        # Browser configuration
        self.browser_args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor'
        ]
        
        self.logger.info(f"{Fore.GREEN}Al-Kafeel Extractor initialized")
        self.logger.info(f"{Fore.BLUE}Output directory: {self.output_dir.absolute()}")
    
    def setup_logging(self, verbose: bool):
        """Setup logging configuration."""
        log_level = logging.DEBUG if verbose else logging.INFO
        log_file = self.output_dir / "logs" / f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def validate_url(self, url: str) -> bool:
        """
        Validate if the URL is from Al-Kafeel library.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid Al-Kafeel URL
        """
        try:
            parsed = urlparse(url)
            is_alkafeel = 'library.alkafeel.net' in parsed.netloc
            has_book_path = '/dic/book/' in parsed.path
            
            if not is_alkafeel:
                self.logger.error(f"{Fore.RED}URL must be from library.alkafeel.net domain")
                return False
                
            if not has_book_path:
                self.logger.error(f"{Fore.RED}URL must contain '/dic/book/' path")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"{Fore.RED}Invalid URL format: {e}")
            return False
    
    def extract_book_id(self, url: str) -> str:
        """
        Extract book ID from the URL for filename generation.
        
        Args:
            url (str): Book URL
            
        Returns:
            str: Extracted book ID
        """
        try:
            # Extract the 'e' parameter which contains the book ID
            match = re.search(r'[?&]e=([^&]+)', url)
            if match:
                return match.group(1)
            
            # Fallback: use timestamp
            return f"book_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        except Exception as e:
            self.logger.warning(f"{Fore.YELLOW}Could not extract book ID: {e}")
            return f"book_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    async def setup_browser(self) -> Browser:
        """
        Setup and configure the browser instance.
        
        Returns:
            Browser: Configured Playwright browser
        """
        playwright = await async_playwright().start()
        
        browser = await playwright.chromium.launch(
            headless=True,
            args=self.browser_args
        )
        
        self.logger.info(f"{Fore.GREEN}Browser launched successfully")
        return browser
    
    async def setup_page(self, browser: Browser) -> Page:
        """
        Setup and configure a new page with proper headers and settings.
        
        Args:
            browser (Browser): Browser instance
            
        Returns:
            Page: Configured page
        """
        page = await browser.new_page()
        
        # Set viewport and user agent
        await page.set_viewport_size({"width": 1280, "height": 720})
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        return page
    
    async def navigate_to_book(self, page: Page, url: str) -> bool:
        """
        Navigate to the book URL and wait for content to load.
        
        Args:
            page (Page): Browser page
            url (str): Book URL
            
        Returns:
            bool: True if navigation successful
        """
        try:
            self.logger.info(f"{Fore.BLUE}Navigating to: {url}")
            
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(3)  # Additional wait for dynamic content
            
            self.logger.info(f"{Fore.GREEN}Successfully navigated to book page")
            return True
            
        except Exception as e:
            self.logger.error(f"{Fore.RED}Navigation failed: {e}")
            return False
    
    async def extract_iframe_content(self, page: Page, book_id: str) -> Optional[Dict]:
        """
        Extract content from iframe including PDF data.
        
        Args:
            page (Page): Browser page
            book_id (str): Book identifier
            
        Returns:
            Optional[Dict]: Extracted content or None if failed
        """
        try:
            self.logger.info(f"{Fore.BLUE}Searching for iframe content...")
            
            # Find iframe elements
            iframe_elements = await page.query_selector_all('iframe')
            
            if not iframe_elements:
                self.logger.error(f"{Fore.RED}No iframe found on the page")
                return None
            
            self.logger.info(f"{Fore.GREEN}Found {len(iframe_elements)} iframe(s)")
            
            for i, iframe in enumerate(iframe_elements):
                try:
                    self.logger.info(f"{Fore.BLUE}Processing iframe {i+1}...")
                    
                    # Get iframe src
                    iframe_src = await iframe.get_attribute('src')
                    self.logger.info(f"Iframe src: {iframe_src}")
                    
                    # Access iframe content
                    iframe_content = await iframe.content_frame()
                    if not iframe_content:
                        self.logger.warning(f"{Fore.YELLOW}Could not access iframe {i+1} content")
                        continue
                    
                    # Wait for content to load
                    await asyncio.sleep(3)
                    
                    # Extract text content
                    iframe_text = await iframe_content.text_content('body')
                    if not iframe_text or len(iframe_text.strip()) < 100:
                        self.logger.warning(f"{Fore.YELLOW}Iframe {i+1} has insufficient content")
                        continue
                    
                    self.logger.info(f"{Fore.GREEN}Extracted {len(iframe_text)} characters from iframe {i+1}")
                    
                    # Take screenshot
                    screenshot_path = self.output_dir / "screenshots" / f"{book_id}_iframe_{i+1}.png"
                    try:
                        await page.screenshot(path=str(screenshot_path))
                        self.logger.info(f"{Fore.GREEN}Screenshot saved: {screenshot_path}")
                    except Exception as screenshot_error:
                        self.logger.warning(f"{Fore.YELLOW}Screenshot failed: {screenshot_error}")
                    
                    # Return the content for processing
                    return {
                        'iframe_index': i + 1,
                        'iframe_src': iframe_src,
                        'content': iframe_text,
                        'content_length': len(iframe_text)
                    }
                    
                except Exception as iframe_error:
                    self.logger.error(f"{Fore.RED}Error processing iframe {i+1}: {iframe_error}")
                    continue
            
            self.logger.error(f"{Fore.RED}No valid iframe content found")
            return None
            
        except Exception as e:
            self.logger.error(f"{Fore.RED}Failed to extract iframe content: {e}")
            return None
    
    def extract_pdf_data(self, content: str) -> Optional[str]:
        """
        Extract base64-encoded PDF data from iframe content.
        
        Args:
            content (str): Iframe text content
            
        Returns:
            Optional[str]: Base64-encoded PDF data or None if not found
        """
        try:
            self.logger.info(f"{Fore.BLUE}Searching for PDF data in content...")
            
            # Search for pdfData variable
            pdf_pattern = r'var pdfData = ["\']([^"\']+)["\']'
            match = re.search(pdf_pattern, content, re.DOTALL)
            
            if match:
                pdf_data_b64 = match.group(1)
                self.logger.info(f"{Fore.GREEN}Found PDF data ({len(pdf_data_b64)} characters)")
                return pdf_data_b64
            
            # Alternative patterns
            alternative_patterns = [
                r'pdfData\s*=\s*["\']([^"\']+)["\']',
                r'["\']data:application/pdf;base64,([^"\']+)["\']',
                r'["\'](JVBERi[^"\']+)["\']'  # Direct PDF header
            ]
            
            for pattern in alternative_patterns:
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    pdf_data_b64 = match.group(1)
                    self.logger.info(f"{Fore.GREEN}Found PDF data with alternative pattern ({len(pdf_data_b64)} characters)")
                    return pdf_data_b64
            
            self.logger.error(f"{Fore.RED}No PDF data found in content")
            return None
            
        except Exception as e:
            self.logger.error(f"{Fore.RED}Error extracting PDF data: {e}")
            return None
    
    def decode_and_save_pdf(self, pdf_data_b64: str, book_id: str) -> Optional[str]:
        """
        Decode base64 PDF data and save to file.
        
        Args:
            pdf_data_b64 (str): Base64-encoded PDF data
            book_id (str): Book identifier
            
        Returns:
            Optional[str]: Path to saved PDF file or None if failed
        """
        try:
            self.logger.info(f"{Fore.BLUE}Decoding PDF data...")
            
            # Decode base64 data
            pdf_data = base64.b64decode(pdf_data_b64)
            
            # Generate filename
            pdf_filename = f"{book_id}.pdf"
            pdf_path = self.output_dir / "pdfs" / pdf_filename
            
            # Save PDF file
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(pdf_data)
            
            self.logger.info(f"{Fore.GREEN}PDF saved successfully: {pdf_path}")
            self.logger.info(f"{Fore.GREEN}File size: {len(pdf_data):,} bytes")
            
            return str(pdf_path)
            
        except Exception as e:
            self.logger.error(f"{Fore.RED}Failed to decode/save PDF: {e}")
            return None
    
    def save_metadata(self, book_id: str, url: str, extraction_data: Dict) -> str:
        """
        Save extraction metadata to JSON file.
        
        Args:
            book_id (str): Book identifier
            url (str): Original book URL
            extraction_data (Dict): Extraction results and metadata
            
        Returns:
            str: Path to metadata file
        """
        metadata = {
            'book_id': book_id,
            'original_url': url,
            'extraction_date': datetime.now().isoformat(),
            'extractor_version': '1.0.0',
            'created_by': 'Eylias Sharar',
            **extraction_data
        }
        
        metadata_file = self.output_dir / "metadata" / f"{book_id}_metadata.json"
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"{Fore.GREEN}Metadata saved: {metadata_file}")
        return str(metadata_file)
    
    async def extract_book(self, url: str) -> Dict:
        """
        Main extraction method - orchestrates the entire process.
        
        Args:
            url (str): Book URL from Al-Kafeel library
            
        Returns:
            Dict: Extraction results
        """
        extraction_start = datetime.now()
        
        # Validate URL
        if not self.validate_url(url):
            return {
                'success': False,
                'error': 'Invalid URL',
                'url': url
            }
        
        # Extract book ID
        book_id = self.extract_book_id(url)
        
        self.logger.info(f"{Fore.CYAN}{'='*60}")
        self.logger.info(f"{Fore.CYAN}Starting extraction for book ID: {book_id}")
        self.logger.info(f"{Fore.CYAN}{'='*60}")
        
        browser = None
        try:
            # Setup browser and page
            browser = await self.setup_browser()
            page = await self.setup_page(browser)
            
            # Navigate to book
            if not await self.navigate_to_book(page, url):
                raise Exception("Failed to navigate to book page")
            
            # Extract iframe content
            iframe_data = await self.extract_iframe_content(page, book_id)
            if not iframe_data:
                raise Exception("Failed to extract iframe content")
            
            # Extract PDF data
            pdf_data_b64 = self.extract_pdf_data(iframe_data['content'])
            if not pdf_data_b64:
                raise Exception("Failed to extract PDF data")
            
            # Decode and save PDF
            pdf_path = self.decode_and_save_pdf(pdf_data_b64, book_id)
            if not pdf_path:
                raise Exception("Failed to decode/save PDF")
            
            # Prepare results
            extraction_data = {
                'success': True,
                'book_id': book_id,
                'url': url,
                'pdf_path': pdf_path,
                'pdf_size_bytes': len(base64.b64decode(pdf_data_b64)),
                'iframe_data': {
                    'iframe_index': iframe_data['iframe_index'],
                    'iframe_src': iframe_data['iframe_src'],
                    'content_length': iframe_data['content_length']
                },
                'extraction_duration': str(datetime.now() - extraction_start)
            }
            
            # Save metadata
            metadata_path = self.save_metadata(book_id, url, extraction_data)
            extraction_data['metadata_path'] = metadata_path
            
            self.logger.info(f"{Fore.GREEN}{'='*60}")
            self.logger.info(f"{Fore.GREEN}EXTRACTION SUCCESSFUL!")
            self.logger.info(f"{Fore.GREEN}Book ID: {book_id}")
            self.logger.info(f"{Fore.GREEN}PDF Path: {pdf_path}")
            self.logger.info(f"{Fore.GREEN}Duration: {extraction_data['extraction_duration']}")
            self.logger.info(f"{Fore.GREEN}{'='*60}")
            
            return extraction_data
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"{Fore.RED}{'='*60}")
            self.logger.error(f"{Fore.RED}EXTRACTION FAILED!")
            self.logger.error(f"{Fore.RED}Error: {error_msg}")
            self.logger.error(f"{Fore.RED}{'='*60}")
            
            return {
                'success': False,
                'error': error_msg,
                'book_id': book_id,
                'url': url,
                'extraction_duration': str(datetime.now() - extraction_start)
            }
            
        finally:
            if browser:
                await browser.close()
                self.logger.info(f"{Fore.BLUE}Browser closed")


async def extract_single_book(url: str, output_dir: str = "output", verbose: bool = False) -> Dict:
    """
    Convenience function to extract a single book.
    
    Args:
        url (str): Book URL
        output_dir (str): Output directory
        verbose (bool): Enable verbose logging
        
    Returns:
        Dict: Extraction results
    """
    extractor = AlkafeelExtractor(output_dir=output_dir, verbose=verbose)
    return await extractor.extract_book(url)


async def extract_multiple_books(urls: list, output_dir: str = "output", verbose: bool = False) -> Dict:
    """
    Extract multiple books with progress tracking.
    
    Args:
        urls (list): List of book URLs
        output_dir (str): Output directory
        verbose (bool): Enable verbose logging
        
    Returns:
        Dict: Combined extraction results
    """
    extractor = AlkafeelExtractor(output_dir=output_dir, verbose=verbose)
    
    results = {
        'total_books': len(urls),
        'successful_extractions': [],
        'failed_extractions': [],
        'start_time': datetime.now().isoformat()
    }
    
    print(f"{Fore.CYAN}Starting batch extraction of {len(urls)} books...")
    
    for i, url in enumerate(tqdm(urls, desc="Extracting books")):
        print(f"\n{Fore.BLUE}Processing book {i+1}/{len(urls)}: {url}")
        
        result = await extractor.extract_book(url)
        
        if result['success']:
            results['successful_extractions'].append(result)
            print(f"{Fore.GREEN}✓ Book {i+1} extracted successfully")
        else:
            results['failed_extractions'].append(result)
            print(f"{Fore.RED}✗ Book {i+1} extraction failed: {result.get('error', 'Unknown error')}")
    
    results['end_time'] = datetime.now().isoformat()
    results['success_rate'] = len(results['successful_extractions']) / len(urls) * 100
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}BATCH EXTRACTION COMPLETE")
    print(f"{Fore.GREEN}Successful: {len(results['successful_extractions'])}/{len(urls)}")
    print(f"{Fore.RED}Failed: {len(results['failed_extractions'])}/{len(urls)}")
    print(f"{Fore.BLUE}Success Rate: {results['success_rate']:.1f}%")
    print(f"{Fore.CYAN}{'='*60}")
    
    return results


if __name__ == "__main__":
    # Example usage
    test_url = "https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b"
    
    print(f"{Fore.CYAN}Al-Kafeel Book Extractor - Test Run")
    print(f"{Fore.CYAN}Created by: Eylias Sharar")
    print(f"{Fore.CYAN}{'='*60}")
    
    # Run test extraction
    result = asyncio.run(extract_single_book(test_url, verbose=True))
    
    if result['success']:
        print(f"\n{Fore.GREEN}Test extraction completed successfully!")
        print(f"{Fore.GREEN}Check the 'output' directory for results.")
    else:
        print(f"\n{Fore.RED}Test extraction failed: {result.get('error', 'Unknown error')}")