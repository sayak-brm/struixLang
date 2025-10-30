# Agent Guidelines for struixLang

## Build/Lint/Test Commands
- **Install dependencies**: `pip install -r requirements.txt`
- **Run all tests**: `python src/tests/test_runner.py`
- **Run single test**: `python src/tests/test_runner.py <index>` (e.g., `python src/tests/test_runner.py 1`)
- **No linting tools configured** - use your judgment for code quality

## Code Style Guidelines
- **Naming**: Classes (PascalCase), methods/functions (camelCase), variables/constants (snake_case)
- **Imports**: Standard library first, then third-party, then local. Use relative imports with `from . import`
- **Docstrings**: Use triple quotes for all public methods/classes with brief descriptions
- **Error handling**: Use try/except blocks with specific exception types when possible
- **Formatting**: 4-space indentation, consistent spacing around operators
- **Comments**: Use `##` for copyright headers, `#` for inline comments
- **Types**: No type hints required (legacy codebase), but add them for new code if beneficial
- **Strings**: Prefer f-strings for formatting, use raw strings (r'') for regex/C-like code