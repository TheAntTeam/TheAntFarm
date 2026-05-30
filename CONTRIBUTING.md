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

- **Black** (line length: 120)
- **isort** (profile: black, line length: 120)
- **flake8** (max line length: 120, extend-ignore: E203)
- **mypy** (ignore missing imports)

Run checks before committing:

```bash
black --check --exclude="(app_resources_rc|ui_the_ant_farm|hook-vispy|vispy_qt_widget)\.py" src tests
isort --check-only --profile=black --line-length=120 src tests
flake8 --exclude app_resources_rc.py,ui_the_ant_farm.py,hook-vispy.py,vispy_qt_widget.py src tests
mypy src tests --ignore-missing-imports
```

Or apply formatting automatically:

```bash
black --exclude="(app_resources_rc|ui_the_ant_farm|hook-vispy|vispy_qt_widget)\.py" src tests
isort --profile=black --line-length=120 src tests
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
