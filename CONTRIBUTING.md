# Contributing to Fiber Ops Dashboard

Thank you for considering contributing to the Fiber Ops Dashboard! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

## 📜 Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the repository maintainer.

## 🤝 How Can I Contribute?

### Reporting Bugs

- Use the GitHub issue tracker
- Check if the bug has already been reported
- Include detailed steps to reproduce
- Specify your environment (OS, Docker version, etc.)
- Include relevant logs and error messages

### Suggesting Enhancements

- Use GitHub issues to suggest features
- Clearly describe the feature and its benefits
- Include examples of how it would work
- Consider backward compatibility

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## 💻 Development Setup

### Prerequisites

```bash
# Install Python 3.11+
# Install Docker and Docker Compose
```

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/fiber-ops-dashboard.git
cd fiber-ops-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r app/requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your test credentials

# Run in development mode
cd app
python app.py
```

### Testing

```bash
# Run tests (when available)
pytest

# Check code style
flake8 app/

# Type checking
mypy app/
```

## 🔄 Pull Request Process

### Before Submitting

1. **Update documentation** - If you add features, update relevant docs
2. **Test your changes** - Ensure everything works
3. **Follow style guidelines** - Keep code consistent
4. **Write clear commit messages** - Explain what and why
5. **Keep PRs focused** - One feature/fix per PR

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No new warnings
```

### Review Process

1. Maintainer reviews PR
2. Address feedback if requested
3. Once approved, PR will be merged
4. Thank you for contributing!

## 📐 Style Guidelines

### Python Code Style

- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions

```python
def sync_from_sheets() -> tuple[bool, str]:
    """
    Sync data from Google Sheets to local database.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    # Implementation
```

### Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line: brief summary (50 chars max)
- Blank line, then detailed description if needed

```
Add: Real-time sync status indicator

Implements a visual indicator in the UI that shows when
data is being synced from Google Sheets. Includes spinner
and success/error messages.

Fixes #123
```

### Documentation

- Use clear, concise language
- Include code examples
- Keep docs up-to-date with code
- Use proper markdown formatting

## 🏷️ Branch Naming

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/update-description` - Documentation
- `refactor/component-name` - Code refactoring

## 🧪 Testing Guidelines

### What to Test

- New features must include tests
- Bug fixes should include regression tests
- Test edge cases and error conditions
- Verify backward compatibility

### Test Structure

```python
import pytest

def test_sync_from_sheets():
    """Test successful sync from Google Sheets"""
    # Setup
    # Execute
    # Assert
    # Cleanup
```

## 📦 Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release branch
4. Tag release
5. Merge to main

## ❓ Questions?

Feel free to open an issue with the "question" label or reach out to the maintainers.

## 🎉 Recognition

All contributors will be recognized in the project README and release notes!

---

Thank you for contributing to Fiber Ops Dashboard! 🚀
