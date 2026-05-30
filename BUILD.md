ORIX - DEPLOYMENT & RELEASE COMMANDS
=====================================

This file contains the exact terminal commands needed to build, test, and release Orix to PyPI.

---
## SECTION 1: LOCAL SETUP & TESTING
---

### 1.1 Initial Setup

```bash
# Clone the repository
git clone https://github.com/kryonara/orix.git
cd orix

# Create virtual environment
python3 -m venv venv

# Activate (on macOS/Linux)
source venv/bin/activate

# Activate (on Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (on Windows Command Prompt)
venv\Scripts\activate.bat

# Install in development mode with all extras
pip install -e ".[dev,publish]"
```

### 1.2 Run Full Test Suite

```bash
# Execute all integration tests
pytest tests/ -v --tb=short

# Run with coverage report
pytest tests/ -v --cov=core --cov=orix --cov-report=html

# Run specific test (e.g., Django tests)
pytest tests/test_scaffolder.py::TestProjectBuilder::test_django_structure_sqlite -v

# Run Docker integration tests only
pytest tests/test_scaffolder.py -k docker -v
```

### 1.3 Code Quality Checks

```bash
# Format code with Black
black .

# Check formatting without changes
black --check .

# Lint with Flake8
flake8 orix.py core/ tests/

# Type checking with mypy
mypy orix.py core/
```

### 1.4 Manual CLI Verification

```bash
# Interactive mode
python orix.py

# Test Django generation
python orix.py test_django --framework django

# Test Django with Docker and PostgreSQL
python orix.py test_django_prod --framework django --docker --database postgres

# Test FastAPI
python orix.py test_fastapi --framework fastapi --docker

# Test Next.js
python orix.py test_nextjs --framework nextjs --docker

# Test React
python orix.py test_react --framework react

# Test Flutter
python orix.py test_flutter --framework flutter
```

---
## SECTION 2: BUILD & PACKAGING
---

### 2.1 Prepare for Release

```bash
# Update version in pyproject.toml
# Change [project] version = "0.1.0" to "0.2.0" (or your version)

# Commit changes
git add .
git commit -m "Release v0.2.0"

# Create git tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main --tags
```

### 2.2 Build Distribution Artifacts

```bash
# Install build tools (if not already installed)
pip install build twine

# Clean old builds
rm -rf build dist *.egg-info

# Build source distribution and wheel
python -m build

# Verify build contents
twine check dist/*

# List wheel contents
unzip -l dist/orix-0.2.0-py3-none-any.whl
```

### 2.3 Resulting Artifacts

After running `python -m build`, you should have:

```
dist/
├── orix-0.2.0.tar.gz              # Source distribution (~50 KB)
└── orix-0.2.0-py3-none-any.whl    # Universal wheel (~40 KB)
```

---
## SECTION 3: LOCAL DISTRIBUTION TESTING
---

### 3.1 Test Wheel Installation

```bash
# Create fresh virtual environment for testing
python3 -m venv test_env

# Activate test environment
source test_env/bin/activate          # macOS/Linux
.\test_env\Scripts\Activate.ps1       # Windows PowerShell

# Install from built wheel
pip install dist/orix-0.2.0-py3-none-any.whl

# Verify installation
orix --help

# Test scaffolding
orix demo_app --framework nextjs
cd demo_app
npm install
npm run dev
```

### 3.2 Test Source Distribution

```bash
# Create another test environment
python3 -m venv test_src_env
source test_src_env/bin/activate

# Install from source distribution
pip install dist/orix-0.2.0.tar.gz

# Verify
orix --help
```

---
## SECTION 4: TESTPYPI RELEASE
---

### 4.1 Configure PyPI Credentials

Create or update `~/.pypirc`:

```ini
[distutils]
index-servers =
    testpypi
    pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHl...YOUR_TESTPYPI_TOKEN...

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHl...YOUR_PYPI_TOKEN...
```

Set file permissions (Unix-like systems):

```bash
chmod 600 ~/.pypirc
```

### 4.2 Upload to TestPyPI

```bash
# Upload all distributions to TestPyPI
twine upload --repository testpypi dist/*

# You should see output like:
# Uploading distributions to https://test.pypi.org/legacy/
# Uploading orix-0.2.0.tar.gz: 100%
# Uploading orix-0.2.0-py3-none-any.whl: 100%
```

### 4.3 Test Installation from TestPyPI

```bash
# Create new environment
python3 -m venv testpypi_env
source testpypi_env/bin/activate

# Install from TestPyPI (bypasses main PyPI)
pip install --index-url https://test.pypi.org/simple/ orix

# Verify
orix --help
orix my_testapp --framework django
```

---
## SECTION 5: PRODUCTION PYPI RELEASE
---

### 5.1 Upload to Production PyPI

```bash
# Upload all distributions to production PyPI
twine upload dist/*

# Expected output:
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading orix-0.2.0.tar.gz: 100%
# Uploading orix-0.2.0-py3-none-any.whl: 100%
```

### 5.2 Verify Production Release

```bash
# Give PyPI a moment to process (~30 seconds)
sleep 30

# Verify package on PyPI
pip search orix  # (if available)
# OR visit: https://pypi.org/project/orix/

# Install from production PyPI
pip install --upgrade orix

# Verify
orix --version
orix --help

# Final test
orix production_app --framework fastapi --docker
cd production_app
cat requirements.txt
```

---
## SECTION 6: POST-RELEASE VERIFICATION
---

### 6.1 Installation Methods

```bash
# Method 1: Traditional pip
pip install orix

# Method 2: Using pipx (recommended)
pipx install orix
orix --help

# Method 3: From GitHub directly
pip install git+https://github.com/kryonara/orix.git

# Method 4: One-liner installer
bash <(curl -s https://raw.githubusercontent.com/kryonara/orix/main/install.sh)
```

### 6.2 Multi-Platform Validation

```bash
# Test on fresh environments across platforms

# macOS/Linux
python3 -m venv orix_test
source orix_test/bin/activate
pip install orix
orix test_app --framework django

# Windows PowerShell
python -m venv orix_test
.\orix_test\Scripts\Activate.ps1
pip install orix
orix test_app --framework django

# Docker
docker run -it python:3.12 bash
pip install orix
orix test_app --framework fastapi
```

---
## SECTION 7: TROUBLESHOOTING
---

### Common Issues & Solutions

```bash
# Issue: "twine not found"
# Solution:
pip install twine

# Issue: "build command not found"
# Solution:
pip install build

# Issue: Authentication failed on PyPI
# Solution: Check ~/.pypirc, ensure token is correct
cat ~/.pypirc

# Issue: "ModuleNotFoundError: rich" during testing
# Solution:
pip install -e ".[dev,publish]"

# Issue: Old version still appears after upload
# Solution: Wait 15-30 seconds for PyPI CDN to update, then:
pip cache purge
pip install --upgrade orix

# Issue: Tests fail in CI/CD
# Solution: Ensure all test dependencies are installed
pip install -e ".[dev]"
pytest tests/ -v
```

---
## SECTION 8: AUTOMATED RELEASE SCRIPT
---

Run the provided build script for a fully automated workflow:

```bash
# On macOS/Linux
bash build.sh

# On Windows (using Git Bash or WSL)
bash build.sh

# The script will:
# 1. Set up virtual environment
# 2. Install dependencies
# 3. Run full test suite
# 4. Run code quality checks
# 5. Build distributions
# 6. Verify builds
# 7. Display summary
```

---
## SECTION 9: FINAL CHECKLIST
---

Before releasing to production PyPI:

- [ ] All tests pass: `pytest tests/ -v`
- [ ] Code formatted: `black .` (no changes)
- [ ] Linting passes: `flake8 orix.py core/ tests/`
- [ ] Version updated in pyproject.toml
- [ ] CHANGELOG updated
- [ ] Git tag created: `git tag -a v0.2.0`
- [ ] Build verified: `twine check dist/*`
- [ ] Tested from TestPyPI
- [ ] Tested wheel installation locally
- [ ] README.md reflects current features
- [ ] CLI help text is accurate

---
## SECTION 10: SUPPORT & DOCUMENTATION
---

### Project Repository
- GitHub: https://github.com/kryonara/orix
- PyPI: https://pypi.org/project/orix/
- Issues: https://github.com/kryonara/orix/issues

### Documentation Files
- README.md - User guide and quick start
- RELEASING.md - Detailed release workflow
- CHANGELOG.md - Version history and changes
- BUILD.md - This file

### Getting Help
```bash
# CLI help
orix --help

# Framework-specific help
orix my-app --framework django --help

# Python API documentation
python -c "from core.engine import ProjectBuilder; help(ProjectBuilder)"
```

---

DEPLOYMENT COMPLETE!
Orix is ready for production release to the community.
