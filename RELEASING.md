# Orix Release Guide

This document contains the complete workflow for building, testing, and releasing Orix to PyPI.

## Prerequisites

Ensure you have:
- Python 3.10+
- `pip` and `pipx` installed
- A PyPI account with API token (for production releases)

## 1. Local Development Setup

Clone the repository and install in development mode:

```bash
git clone https://github.com/kryonara/orix.git
cd orix
python -m venv venv

# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install with dev extras
pip install -e ".[dev]"
```

## 2. Running the Test Suite

Execute all integration tests to validate the scaffolding engine:

```bash
pytest tests/ -v --tb=short
```

Run with coverage report:

```bash
pytest tests/ -v --cov=core --cov=orix --cov-report=html
```

Individual test categories:

```bash
# Test Django scaffolding
pytest tests/test_scaffolder.py::TestProjectBuilder::test_django_structure_sqlite -v

# Test FastAPI scaffolding
pytest tests/test_scaffolder.py::TestProjectBuilder::test_fastapi_structure -v

# Test Next.js scaffolding
pytest tests/test_scaffolder.py::TestProjectBuilder::test_nextjs_structure -v

# Test React scaffolding
pytest tests/test_scaffolder.py::TestProjectBuilder::test_react_structure -v

# Test Flutter scaffolding
pytest tests/test_scaffolder.py::TestProjectBuilder::test_flutter_structure -v

# Test Docker integration
pytest tests/test_scaffolder.py -k "docker" -v
```

## 3. Code Quality Checks

Format code with Black:

```bash
black .
```

Lint with Flake8:

```bash
flake8 orix.py core/ tests/
```

Type check with mypy:

```bash
mypy orix.py core/
```

## 4. Manual CLI Testing

Test the CLI interactively:

```bash
# Interactive mode (prompts for all inputs)
python orix.py

# Django with SQLite
python orix.py test_django_app --framework django

# FastAPI with PostgreSQL and Docker
python orix.py test_fastapi_app --framework fastapi --docker --database postgres

# Next.js with Tailwind
python orix.py test_nextjs_app --framework nextjs --docker

# React with Docker
python orix.py test_react_app --framework react --docker

# Flutter
python orix.py test_flutter_app --framework flutter
```

Test in a fresh directory:

```bash
cd /tmp
python /path/to/orix/orix.py demo_project --framework django --docker
cd demo_project
cat README.md
cat requirements.txt
cat Dockerfile
```

## 5. Building Distribution Artifacts

Install build tools:

```bash
pip install build twine
```

Build both source distribution and wheel:

```bash
python -m build
```

This creates:
- `dist/orix-0.1.0.tar.gz` - Source distribution
- `dist/orix-0.1.0-py3-none-any.whl` - Universal wheel

Verify the build:

```bash
twine check dist/*
```

List contents of the wheel:

```bash
unzip -l dist/orix-0.1.0-py3-none-any.whl
```

## 6. Testing the Distribution Locally

Create a fresh virtual environment and install from the built wheel:

```bash
python -m venv test_venv

# On Windows
.\test_venv\Scripts\activate
# On macOS/Linux
source test_venv/bin/activate

pip install dist/orix-0.1.0-py3-none-any.whl
```

Test the installed CLI:

```bash
orix test_app --framework nextjs
cd test_app
npm install
npm run dev
```

## 7. Preparing for PyPI Release

### Update version number

Edit `pyproject.toml`:

```toml
[project]
version = "0.2.0"  # Bump version
```

### Update CHANGELOG

Create or update a `CHANGELOG.md` file with:

```markdown
# Changelog

## [0.2.0] - 2026-05-29

### Added
- Support for PostgreSQL in Django scaffolds
- Docker Compose integration for all frameworks
- Enhanced authentication boilerplate

### Fixed
- Unicode encoding issues in CLI output
- CORS configuration for FastAPI

### Changed
- Improved project naming validation
```

### Create release tag

```bash
git add .
git commit -m "Release v0.2.0"
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main --tags
```

## 8. PyPI Upload (TestPyPI first)

### Register on TestPyPI

1. Create account at https://test.pypi.org/account/register/
2. Generate API token at https://test.pypi.org/manage/account/tokens/
3. Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    testpypi
    pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgE...  # Your TestPyPI token

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgE...  # Your PyPI token
```

### Upload to TestPyPI

```bash
twine upload --repository testpypi dist/*
```

Test installation from TestPyPI:

```bash
python -m venv test_pypi_venv

# On Windows
.\test_pypi_venv\Scripts\activate
# On macOS/Linux
source test_pypi_venv/bin/activate

pip install --index-url https://test.pypi.org/simple/ orix
orix --help
```

## 9. Production PyPI Release

Once TestPyPI testing passes:

```bash
twine upload dist/*
```

Verify the package is live:

```bash
pip install --upgrade orix
orix --version
```

## 10. Installation via pipx (Recommended for users)

```bash
pipx install orix
orix my-project --framework django
```

## 11. Post-Release

### Update GitHub release

```bash
# Create a GitHub release with:
# - Tag: v0.2.0
# - Title: Orix 0.2.0
# - Description: Link to CHANGELOG
# - Attach: dist/orix-0.1.0.tar.gz, dist/orix-0.1.0-py3-none-any.whl
```

### Announce release

- Post on relevant channels (Twitter, Reddit, GitHub Discussions, etc.)
- Update package manager repositories if applicable

## Quick Reference: Complete Release Checklist

```bash
# 1. Update version
# Edit pyproject.toml, bump version

# 2. Run tests
pytest tests/ -v

# 3. Code quality
black .
flake8 orix.py core/ tests/
mypy orix.py core/

# 4. Build
python -m build

# 5. Verify build
twine check dist/*

# 6. Test locally
pip install dist/orix-*.whl
orix test --framework django

# 7. Upload to TestPyPI
twine upload --repository testpypi dist/*

# 8. Test from TestPyPI
pip install --index-url https://test.pypi.org/simple/ orix --upgrade

# 9. Upload to production PyPI
twine upload dist/*

# 10. Verify
pip install --upgrade orix
orix --help
```

## Troubleshooting

### Build fails due to missing dependencies

```bash
pip install --upgrade build setuptools wheel
python -m build
```

### Twine not found

```bash
pip install twine
```

### Permission denied on PyPI

Ensure your `~/.pypirc` has correct credentials and proper file permissions:

```bash
chmod 600 ~/.pypirc
```

### Old version still installed

```bash
pip install --force-reinstall orix
```

## Questions?

For issues or questions, open an issue on GitHub: https://github.com/kryonara/orix/issues
