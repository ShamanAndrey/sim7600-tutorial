# Contributing to SMS Logger

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, modem model)

### Suggesting Features

Feature suggestions are welcome! Please open an issue describing:
- The feature you'd like to see
- Why it would be useful
- How you envision it working

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Install in development mode**: `pip install -e .`
3. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes** thoroughly with a real SIM7600 modem if possible
5. **Submit a pull request** with a clear description of your changes

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/sms-logger.git
cd sms-logger

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # On Windows
# or: source .venv/bin/activate  # On Linux/Mac

# Install in editable mode
pip install -e .

# Run the program
python -m sms_logger --init-only
```

### Code Style

- Use type hints where appropriate
- Keep functions focused and small
- Write descriptive variable names
- Follow PEP 8 guidelines

### Testing with Different Modems

If you have access to other SIM/GSM modems (not just SIM7600), contributions to improve compatibility are very welcome!

## Questions?

Feel free to open an issue with your question, or start a discussion.

Thank you for contributing! 🙏

