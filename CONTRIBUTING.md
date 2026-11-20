# Contributing to The Ant Farm

## Getting Started

1. Fork the repository
2. Create a branch following the naming convention:
   - `feature/your-feature-name` for new features
   - `improvement/your-change-name` for enhancements
   - `fix/your-bug-name` for bug fixes
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/TheAntFarm.git
cd TheAntFarm
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on Linux/macOS
pip install -r requirements.txt
pip install -r requirements-test.txt
```

## Code Style

This project uses automated formatting and linting:

- **Ruff** for formatting, import order and linting (line length: 120); the rules and the excluded files are in
  `pyproject.toml`
- **mypy** (ignore missing imports)

Run checks before committing:

```bash
ruff check src tests
ruff format --check src tests
mypy src tests --ignore-missing-imports
```

Or apply formatting and the safe fixes automatically:

```bash
ruff format src tests
ruff check --fix src tests
```

## Pre-commit Hooks

This project includes a `.pre-commit-config.yaml` for optional manual use:

```bash
pip install pre-commit
pre-commit run --all-files
```

## Testing

```bash
pytest tests -v
pytest tests -v --cov=src/TheAntFarm --cov-report=term-missing
```

## Pull Request Process

1. Ensure all tests pass and code is formatted
2. Link any related issues in the PR description
3. Request review from maintainers

## Questions?

Open an issue or discussion on GitHub.
