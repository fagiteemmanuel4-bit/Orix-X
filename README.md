# Orix

Orix is a lightweight, premium CLI scaffolder for modern full-stack projects. Generate production-ready boilerplate for Django, FastAPI, Next.js, React, and Flutter in seconds.

## Features

- **Multi-framework support**: Django, FastAPI, Next.js + Tailwind, React (Vite), Flutter
- **Production-ready boilerplate**: JWT auth, CORS, proper directory structure
- **Docker integration**: Multi-stage builds, clean docker-compose.yml
- **Interactive CLI**: Hybrid flow for humans and CI/CD agents
- **Zero placeholders**: All generated files are 100% complete and functional

## Install

### From PyPI (once released)

```bash
pip install orix
# or
pipx install orix
```

### Local development

```bash
git clone https://github.com/kryonara/orix
cd orix
pip install -e .
```

## Quick start

```bash
orix my-app --framework django --docker --auth --database postgres
cd my-app
python manage.py migrate
python manage.py runserver
```

### Interactive mode

```bash
orix
```

### Supported frameworks

- `django` - Django REST Framework with JWT + CORS
- `fastapi` - FastAPI with JWT auth + CORS
- `nextjs` - Next.js with Tailwind CSS and App Router
- `react` - React with Vite and auth context
- `flutter` - Flutter with Provider state management

### CLI options

- `--framework [django|fastapi|nextjs|react|flutter]` - Project stack
- `--docker` - Generate Docker and docker-compose.yml
- `--auth` - Include authentication scaffolding
- `--database [sqlite|postgres]` - Database backend (Django/FastAPI)
- `--output-dir` - Where to create the project

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest tests/ -v
```

Format code:

```bash
black .
```

## Distribution & Release

See [RELEASING.md](RELEASING.md) for complete build and deployment instructions.

## License

MIT

