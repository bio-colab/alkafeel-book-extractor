# 🚀 Al-Kafeel Library Book Extractor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Enabled-green.svg)](https://playwright.dev/)

> **Created by Eylias Sharar** - EB software solutions team 🤖

A powerful, comprehensive tool for extracting PDF books from **Al-Kafeel Digital Library** (library.alkafeel.net) using advanced web automation and PDF decoding techniques.

## ✨ Features

- 🎯 **Automatic Content Detection**: Intelligently navigates iframe-based content
- 🔓 **Base64 PDF Decoding**: Extracts and decodes embedded PDF data
- 📚 **Batch Processing**: Extract multiple books efficiently
- 📊 **Detailed Logging**: Comprehensive extraction reports and metadata
- 🖼️ **Screenshot Capture**: Visual debugging and verification
- 🎨 **Colored Output**: Beautiful, informative console interface
- ⚡ **Progress Tracking**: Real-time extraction progress
- 🛡️ **Error Handling**: Robust error handling and recovery
- 📁 **Organized Output**: Clean, structured file organization

## 🔧 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **Internet Connection**: Required for web automation
- **Disk Space**: Variable (depends on book sizes)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bio-colab/alkafeel-book-extractor.git
cd alkafeel-book-extractor
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Playwright Browsers

```bash
# Install Playwright browsers
playwright install chromium

# Or use the built-in setup command
python main.py setup
```

## 🚀 Quick Start

### Extract a Single Book

```bash
python main.py extract \"https://library.alkafeel.net/dic/book/?e=YOUR_BOOK_ID\"
```

### Test the Installation

```bash
python main.py test
```

### Get Help

```bash
python main.py --help
```

## 📖 Usage Guide

### Command Line Interface

The extractor provides a comprehensive CLI with multiple commands:

#### 1. Extract Single Book

```bash
python main.py extract [URL] [OPTIONS]

Options:
  --output, -o TEXT    Output directory (default: output)
  --verbose, -v        Enable verbose logging
  --help              Show help message
```

**Example:**
```bash
python main.py extract \"https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b\" --output ./my_books --verbose
```

#### 2. Batch Extract Multiple Books

```bash
python main.py batch-extract [URLS_FILE] [OPTIONS]

Options:
  --output, -o TEXT           Output directory (default: output)
  --verbose, -v              Enable verbose logging
  --continue-on-error        Continue even if some extractions fail
  --help                    Show help message
```

**Create a URLs file (e.g., `book_urls.txt`):**
```
https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b
https://library.alkafeel.net/dic/book/?e=ANOTHER_BOOK_ID
# Lines starting with # are ignored
```

**Run batch extraction:**
```bash
python main.py batch-extract book_urls.txt --output ./extracted_books
```

#### 3. Setup Environment

```bash
python main.py setup [OPTIONS]

Options:
  --output, -o TEXT    Output directory to setup (default: output)
  --help              Show help message
```

#### 4. Run Test Extraction

```bash
python main.py test
```

#### 5. Show Information

```bash
python main.py info
```

### Programmatic Usage

You can also use the extractor in your Python code:

```python
import asyncio
from src.alkafeel_extractor import extract_single_book, extract_multiple_books

# Extract single book
async def extract_book():
    url = \"https://library.alkafeel.net/dic/book/?e=YOUR_BOOK_ID\"
    result = await extract_single_book(url, output_dir=\"./output\", verbose=True)
    
    if result['success']:
        print(f\"Book extracted: {result['pdf_path']}\")
    else:
        print(f\"Extraction failed: {result['error']}\")

# Run extraction
asyncio.run(extract_book())
```

## 📁 Output Structure

The extractor creates a well-organized output structure:

```
output/
├── pdfs/                    # 📚 Extracted PDF files
│   ├── book_id_1.pdf
│   ├── book_id_2.pdf
│   └── ...
├── metadata/                # 📋 Extraction metadata (JSON)
│   ├── book_id_1_metadata.json
│   ├── book_id_2_metadata.json
│   └── ...
├── screenshots/             # 🖼️ Page screenshots (for debugging)
│   ├── book_id_1_iframe_1.png
│   └── ...
├── logs/                    # 📝 Detailed logs
│   ├── extraction_20251002_235959.log
│   └── ...
└── batch_results.json       # 📊 Batch extraction summary
```

### Metadata Example

Each extraction generates detailed metadata:

```json
{
  \"book_id\": \"38c15-44c77-06464-07b96-de2b7-82795-3b\",
  \"original_url\": \"https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b\",
  \"extraction_date\": \"2025-10-02T23:59:59.123456\",
  \"extractor_version\": \"1.0.0\",
  \"created_by\": \"Eylias Sharar\",
  \"success\": true,
  \"pdf_path\": \"output/pdfs/38c15-44c77-06464-07b96-de2b7-82795-3b.pdf\",
  \"pdf_size_bytes\": 1180047,
  \"iframe_data\": {
    \"iframe_index\": 1,
    \"iframe_src\": \"https://library.alkafeel.net/dic/book/?bk&e=...\",
    \"content_length\": 1581034
  },
  \"extraction_duration\": \"0:00:15.432123\"
}
```

## 🎯 Supported URLs

The extractor supports book URLs from Al-Kafeel Digital Library:

- ✅ `https://library.alkafeel.net/dic/book/?e=BOOK_ID`
- ✅ URLs must be from `library.alkafeel.net` domain
- ✅ URLs must contain `/dic/book/` path
- ❌ Other domains are not supported

### URL Format Breakdown

```
https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b
       ^^^^^^^^^^^^^^^^^^   ^^^^^^^^     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
       Domain               Path         Book ID Parameter
```

## 🔍 How It Works

The extractor uses a sophisticated multi-step process:

1. **🌐 Browser Automation**: Launches Chromium browser with Playwright
2. **🔍 Navigation**: Navigates to the book URL and waits for content
3. **📑 Iframe Detection**: Locates and accesses iframe content
4. **🔓 Content Extraction**: Extracts JavaScript variables containing PDF data
5. **🔄 Base64 Decoding**: Decodes base64-encoded PDF data
6. **💾 File Saving**: Saves the decoded PDF to disk
7. **📊 Metadata Generation**: Creates detailed extraction reports
8. **🖼️ Screenshot Capture**: Takes screenshots for verification

### Technical Details

- **Web Automation**: Playwright with Chromium browser
- **Content Processing**: Beautiful Soup for HTML parsing
- **PDF Handling**: Base64 decoding for embedded PDF data
- **Logging**: Comprehensive logging with colored output
- **Error Handling**: Robust error handling and recovery mechanisms

## 🛠️ Advanced Configuration

### Environment Variables

You can configure the extractor using environment variables:

```bash
# Browser configuration
export PLAYWRIGHT_BROWSERS_PATH=/custom/path/to/browsers

# Logging level
export LOG_LEVEL=DEBUG

# Output directory
export OUTPUT_DIR=/custom/output/path
```

### Custom Browser Settings

Modify the browser configuration in `src/alkafeel_extractor.py`:

```python
self.browser_args = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-web-security',
    '--disable-features=VizDisplayCompositor',
    # Add your custom arguments here
]
```

## 🧪 Testing

### Run the Built-in Test

```bash
python main.py test
```

### Manual Testing

```bash
# Test with a specific book
python main.py extract \"https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b\" --verbose

# Test batch extraction
echo \"https://library.alkafeel.net/dic/book/?e=38c15-44c77-06464-07b96-de2b7-82795-3b\" > test_urls.txt
python main.py batch-extract test_urls.txt --verbose
```

### Unit Tests (Future Enhancement)

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. **Playwright Browser Not Found**

```bash
# Solution: Install Playwright browsers
playwright install chromium
```

#### 2. **Permission Denied on Output Directory**

```bash
# Solution: Create directory with proper permissions
mkdir -p output
chmod 755 output
```

#### 3. **Network Connection Issues**

- Check your internet connection
- Verify the book URL is accessible in a regular browser
- Try with `--verbose` flag for detailed logs

#### 4. **PDF Extraction Failed**

- The book might not be available or accessible
- Some books might have different content structures
- Check the logs for detailed error information

#### 5. **Import Errors**

```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Debug Mode

Enable verbose logging for detailed troubleshooting:

```bash
python main.py extract \"URL\" --verbose
```

This will provide:
- Detailed browser automation steps
- Content extraction progress
- Error stack traces
- Performance metrics

## 📊 Performance Considerations

### Optimization Tips

1. **Batch Processing**: Use batch extraction for multiple books
2. **Output Directory**: Use SSD storage for better performance
3. **Network**: Stable internet connection recommended
4. **Memory**: 4GB+ RAM recommended for large books
5. **Concurrent Extractions**: Currently single-threaded (future enhancement)

### Typical Performance Metrics

- **Small Book** (< 5MB): 10-30 seconds
- **Medium Book** (5-20MB): 30-60 seconds
- **Large Book** (> 20MB): 60+ seconds

*Performance varies based on network speed and system specifications.*

## 🔄 Updates and Maintenance

### Version History

- **v1.0.0** (2025-10-02): Initial release
  - Basic extraction functionality
  - CLI interface
  - Batch processing
  - Comprehensive logging

### Future Enhancements

- 🚀 **Concurrent Extractions**: Parallel processing for batch operations
- 🔍 **Content Analysis**: Automatic book metadata extraction
- 📱 **GUI Interface**: Desktop application interface
- 🌐 **Web Interface**: Browser-based extraction tool
- 📚 **Library Integration**: Direct library browsing and search
- 🔄 **Auto-Updates**: Automatic tool updates
- 🛡️ **Enhanced Security**: Additional security measures

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/bio-colab/alkafeel-book-extractor.git
cd alkafeel-book-extractor

# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # On Windows: dev-env\\Scripts\\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8

# Run tests
pytest tests/

# Format code
black src/ main.py

# Lint code
flake8 src/ main.py
```

## ⚠️ Disclaimer

This tool is designed for **educational and research purposes**. Users are responsible for:

- Respecting the library's terms of service
- Ensuring legal compliance in their jurisdiction
- Using extracted content appropriately
- Not overloading the library's servers

The creators of this tool are not responsible for any misuse or legal issues arising from its use.

## 📞 Support

### Getting Help

1. **Read the Documentation**: This README contains comprehensive information
2. **Check Issues**: Look for existing issues on GitHub
3. **Create New Issue**: If you find a bug or need a feature
4. **Contact**: Reach out to https://tmkniq.com/EB/

### Reporting Bugs

When reporting bugs, please include:

- 📋 **System Information**: OS, Python version, etc.
- 🔗 **Book URL**: The URL you're trying to extract
- 📝 **Error Message**: Complete error message and stack trace
- 🖥️ **Console Output**: Output with `--verbose` flag
- 📁 **Log Files**: Relevant log files from the `logs/` directory

### Feature Requests

We welcome feature requests! Please provide:

- 📝 **Clear Description**: What you want to achieve
- 🎯 **Use Case**: Why this feature would be useful
- 💡 **Implementation Ideas**: If you have technical suggestions

## 🙏 Acknowledgments

- **Al-Kafeel Digital Library**: For providing access to valuable digital resources
- **Playwright Team**: For the excellent web automation framework
- **Python Community**: For the amazing ecosystem of libraries
- **EB Team**: For supporting team

## 🏆 Credits

**Created with ❤️ by Eylias Sharar - EB software solution team**

*Empowering researchers, students, and knowledge seekers worldwide with advanced AI-powered tools.*

---

<div align=\"center\">
  <p><strong>🚀 Happy Extracting! 📚</strong></p>
  <p>If this tool helped you, please consider giving it a ⭐ star on GitHub!</p>
</div>