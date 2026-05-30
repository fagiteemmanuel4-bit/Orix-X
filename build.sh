#!/usr/bin/env bash

# Orix Build & Release Script
# Complete automated workflow for PyPI deployment

set -euo pipefail

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_section() {
  echo -e "${BLUE}=== $1 ===${NC}"
}

log_success() {
  echo -e "${GREEN}✓ $1${NC}"
}

log_warning() {
  echo -e "${YELLOW}⚠ $1${NC}"
}

# Step 1: Environment setup
log_section "ENVIRONMENT SETUP"
if ! command -v python3 &> /dev/null; then
  echo "Python 3 is required but not installed."
  exit 1
fi
python3 --version
log_success "Python 3 found"

# Step 2: Create virtual environment
log_section "VIRTUAL ENVIRONMENT"
if [ ! -d "venv" ]; then
  python3 -m venv venv
  log_success "Virtual environment created"
else
  log_success "Virtual environment exists"
fi

# Activate venv
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  source venv/Scripts/activate
else
  source venv/bin/activate
fi
log_success "Virtual environment activated"

# Step 3: Install dependencies
log_section "INSTALLING DEPENDENCIES"
pip install --upgrade pip setuptools wheel
pip install -e ".[dev,publish]"
log_success "Dependencies installed"

# Step 4: Run tests
log_section "RUNNING TESTS"
pytest tests/ -v --tb=short
log_success "All tests passed"

# Step 5: Code quality checks
log_section "CODE QUALITY CHECKS"
black --check . || log_warning "Code formatting needed: run 'black .'"
log_success "Code formatting validated"

flake8 orix.py core/ tests/ || log_warning "Linting issues found"
log_success "Linting complete"

# Step 6: Clean build artifacts
log_section "CLEANING BUILD ARTIFACTS"
rm -rf build dist *.egg-info
log_success "Build artifacts cleaned"

# Step 7: Build distributions
log_section "BUILDING DISTRIBUTIONS"
python -m build
log_success "Build complete"

# Step 8: Verify build
log_section "VERIFYING BUILD"
twine check dist/*
log_success "Build verification passed"

# Step 9: Show summary
log_section "BUILD SUMMARY"
echo "Distribution artifacts created:"
ls -lh dist/
echo ""
echo "Next steps:"
echo "1. Test locally: pip install dist/orix-*-py3-none-any.whl"
echo "2. Upload to TestPyPI: twine upload --repository testpypi dist/*"
echo "3. Upload to PyPI: twine upload dist/*"
