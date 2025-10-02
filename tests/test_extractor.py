#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic tests for Al-Kafeel Book Extractor
Created by: Eylias Sharar
"""

import pytest
import asyncio
from pathlib import Path
import tempfile
import os

# Add src to path for testing
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from alkafeel_extractor import AlkafeelExtractor


class TestAlkafeelExtractor:
    """Test cases for AlkafeelExtractor class."""
    
    def setup_method(self):
        """Setup test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.extractor = AlkafeelExtractor(output_dir=self.temp_dir, verbose=False)
    
    def test_validate_url_valid(self):
        """Test URL validation with valid URLs."""
        valid_urls = [
            "https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b",
            "https://library.alkafeel.net/dic/book/?e=test-id&other=param",
        ]
        
        for url in valid_urls:
            assert self.extractor.validate_url(url) == True
    
    def test_validate_url_invalid(self):
        """Test URL validation with invalid URLs."""
        invalid_urls = [
            "https://google.com",
            "https://library.alkafeel.net/other/path",
            "not-a-url",
            "https://other-site.net/dic/book/?e=test",
        ]
        
        for url in invalid_urls:
            assert self.extractor.validate_url(url) == False
    
    def test_extract_book_id(self):
        """Test book ID extraction from URLs."""
        test_cases = [
            (
                "https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b",
                "38c15-44c77-06464-07b96-de2b7-82795-3b"
            ),
            (
                "https://library.alkafeel.net/dic/book/?e=test-id&other=param",
                "test-id"
            ),
        ]
        
        for url, expected_id in test_cases:
            result = self.extractor.extract_book_id(url)
            assert result == expected_id
    
    def test_extract_pdf_data(self):
        """Test PDF data extraction from content."""
        # Mock content with PDF data
        content_with_pdf = '''
        <html>
        <script>
        var pdfData = "JVBERi0xLjUNJeLjz9MNCjE1OTg4IDAgb2JqDTw8L0ZpbHRlci9GbGF0ZURlY29kZS9GaXJzdCA4L0xlbmd0aCAyMDkvTiAxL1R5cGUvT2JqU3RtPj5zdHJlYW0=";
        </script>
        </html>
        '''
        
        result = self.extractor.extract_pdf_data(content_with_pdf)
        assert result is not None
        assert result.startswith("JVBERi0xLjU")
    
    def test_extract_pdf_data_not_found(self):
        """Test PDF data extraction when no PDF data exists."""
        content_without_pdf = '''
        <html>
        <script>
        var otherData = "some other data";
        </script>
        </html>
        '''
        
        result = self.extractor.extract_pdf_data(content_without_pdf)
        assert result is None
    
    def test_output_directory_creation(self):
        """Test that output directories are created properly."""
        output_path = Path(self.temp_dir)
        
        # Check that subdirectories were created
        assert (output_path / "pdfs").exists()
        assert (output_path / "metadata").exists()
        assert (output_path / "screenshots").exists()
        assert (output_path / "logs").exists()
    
    @pytest.mark.asyncio
    async def test_browser_setup(self):
        """Test browser setup and teardown."""
        browser = await self.extractor.setup_browser()
        assert browser is not None
        
        # Test page setup
        page = await self.extractor.setup_page(browser)
        assert page is not None
        
        # Cleanup
        await browser.close()
    
    def teardown_method(self):
        """Cleanup test environment."""
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)


@pytest.mark.integration
class TestIntegration:
    """Integration tests (require internet connection)."""
    
    @pytest.mark.asyncio
    async def test_full_extraction(self):
        """Test full extraction process with a real URL."""
        # This is an integration test that requires internet access
        # Skip if running in CI without network
        pytest.skip("Integration test - requires manual verification")
        
        # Uncomment and modify for actual testing:
        # from alkafeel_extractor import extract_single_book
        # 
        # test_url = "https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b"
        # result = await extract_single_book(test_url, output_dir="test_output")
        # 
        # assert result['success'] == True
        # assert Path(result['pdf_path']).exists()


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])