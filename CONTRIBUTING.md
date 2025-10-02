# Contributing to Al-Kafeel Book Extractor

🚀 **Created by Eylias Sharar - EB software solutions team**

Thank you for your interest in contributing to the Al-Kafeel Book Extractor! This document provides guidelines and information for contributors.

## 🌟 Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Examples of behavior that contributes to creating a positive environment include:**

- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing viewpoints and experiences
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what is best for the community
- ✅ Showing empathy towards other community members

**Examples of unacceptable behavior include:**

- ❌ The use of sexualized language or imagery
- ❌ Trolling, insulting/derogatory comments, and personal or political attacks
- ❌ Public or private harassment
- ❌ Publishing others' private information without explicit permission
- ❌ Other conduct which could reasonably be considered inappropriate

## 🛠️ How to Contribute

### Reporting Bugs 🐛

Before creating bug reports, please check the existing issues as you might find that the problem has already been reported. When creating a bug report, please include:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, etc.)
- **Console output** with `--verbose` flag
- **Log files** from the `logs/` directory
- **Screenshots** if applicable

### Suggesting Enhancements ✨

Enhancement suggestions are welcome! Please provide:

- **Clear description** of the enhancement
- **Use case** - why would this be useful?
- **Implementation ideas** if you have any
- **Examples** of how the feature would work

### Pull Requests 🔄

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Add tests** for your changes
5. **Ensure** all tests pass
6. **Update** documentation if needed
7. **Commit** your changes (`git commit -m 'Add amazing feature'`)
8. **Push** to the branch (`git push origin feature/amazing-feature`)
9. **Open** a Pull Request

## 💻 Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Internet connection (for testing)

### Local Development

```bash
# Clone your fork
git clone https://github.com/bio-colab/alkafeel-book-extractor.git
cd alkafeel-book-extractor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make install-dev
# Or manually:
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8 mypy
playwright install chromium

# Install package in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
make test

# Run tests with verbose output
make test-verbose

# Run specific test file
pytest tests/test_extractor.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Check everything
make check
```

## 📋 Coding Standards

### Python Style

- Follow **PEP 8** guidelines
- Use **Black** for code formatting (line length: 100)
- Use **type hints** where appropriate
- Write **docstrings** for all functions and classes
- Use **meaningful variable names**

### Code Organization

```
src/
└── alkafeel_extractor.py    # Main extractor logic
tests/
└── test_extractor.py        # Unit tests
main.py                     # CLI interface
```

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good examples
git commit -m "Add support for batch extraction with progress bar"
git commit -m "Fix PDF decoding error for large files"
git commit -m "Update README with new installation instructions"

# Bad examples
git commit -m "fix bug"
git commit -m "update"
git commit -m "changes"
```

### Documentation

- Update **README.md** for user-facing changes
- Add **docstrings** for new functions
- Update **type hints** and **examples**
- Include **usage examples** for new features

## 🧪 Testing Guidelines

### Test Types

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test complete extraction workflow
3. **Manual Tests**: Test with real URLs (marked as skip in CI)

### Test Structure

```python
class TestAlkafeelExtractor:
    def test_function_name(self):
        # Arrange
        extractor = AlkafeelExtractor()
        
        # Act
        result = extractor.some_method()
        
        # Assert
        assert result == expected_value
```

### Test Coverage

- Aim for **80%+ code coverage**
- Test **error cases** and **edge cases**
- Use **mocking** for external dependencies
- Include **async/await** tests where applicable

## 📚 Documentation

### README Updates

When adding features, update:

- **Usage examples**
- **Command-line options**
- **Configuration options**
- **Troubleshooting section**

### Code Documentation

```python
def extract_book(self, url: str) -> Dict:
    """
    Extract a book from Al-Kafeel library.
    
    Args:
        url (str): Book URL from library.alkafeel.net
        
    Returns:
        Dict: Extraction results with success status
        
    Raises:
        ValueError: If URL is invalid
        ConnectionError: If network request fails
    """
```

## 🚀 Release Process

### Version Numbers

We use **Semantic Versioning** (SemVer):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated in `setup.py`
- [ ] CHANGELOG.md updated
- [ ] Release notes prepared
- [ ] Manual testing completed

## 🔍 Review Process

### Pull Request Reviews

All PRs require review before merging:

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainer
3. **Testing** on different platforms
4. **Documentation** review

### Review Criteria

- ✅ Code follows style guidelines
- ✅ Tests are included and pass
- ✅ Documentation is updated
- ✅ No breaking changes (unless intentional)
- ✅ Performance impact considered

## 🎆 Recognition

### Contributors

All contributors will be:

- **Listed** in the CONTRIBUTORS.md file
- **Mentioned** in release notes
- **Thanked** in the project documentation

### Types of Contributions

- 💻 **Code**: Bug fixes, features, improvements
- 📚 **Documentation**: README, guides, examples
- 🐛 **Testing**: Bug reports, test cases
- 💡 **Ideas**: Feature suggestions, enhancements
- 🎆 **Community**: Helping other users, spreading the word

## 📞 Getting Help

### Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Email**: Contact aliasbio80@gmail.com for sensitive issues

### Response Times

- **Bug reports**: Within 24-48 hours
- **Feature requests**: Within 1 week
- **Pull requests**: Within 1 week

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the same **MIT License** that covers the project.

---

## 🙏 Thank You!

Thank you for contributing to the Al-Kafeel Book Extractor! Your efforts help make this tool better for researchers, students, and knowledge seekers worldwide.

**Created with ❤️ by Eylias Sharar - EB software solutions team**

*Together, we're making knowledge more accessible!*
