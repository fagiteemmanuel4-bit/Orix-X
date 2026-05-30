import json
import tempfile
from pathlib import Path

import pytest

from core.engine import ProjectBuilder, SUPPORTED_DATABASES, SUPPORTED_FRAMEWORKS


class TestProjectBuilder:
    """Comprehensive integration tests for Orix project scaffolding."""

    def test_all_frameworks_supported(self):
        """Verify all framework constants are defined."""
        assert SUPPORTED_FRAMEWORKS == ["django", "fastapi", "nextjs", "react", "flutter"]

    def test_all_databases_supported(self):
        """Verify all database constants are defined."""
        assert SUPPORTED_DATABASES == ["sqlite", "postgres"]

    @pytest.mark.parametrize("framework", SUPPORTED_FRAMEWORKS)
    def test_project_generation_basic(self, framework: str):
        """Test that all frameworks generate a project structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="test_project",
                framework=framework,
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "test_project"
            assert project_path.exists()
            assert project_path.is_dir()

    def test_django_structure_sqlite(self):
        """Test Django project with SQLite generates required files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="django_app",
                framework="django",
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "django_app"

            # Core files
            assert (project_path / "manage.py").exists()
            assert (project_path / "requirements.txt").exists()
            assert (project_path / "README.md").exists()

            # Core package
            assert (project_path / "core" / "__init__.py").exists()
            assert (project_path / "core" / "settings.py").exists()
            assert (project_path / "core" / "urls.py").exists()
            assert (project_path / "core" / "wsgi.py").exists()
            assert (project_path / "core" / "asgi.py").exists()

            # API package
            assert (project_path / "api" / "__init__.py").exists()
            assert (project_path / "api" / "urls.py").exists()
            assert (project_path / "api" / "views.py").exists()

            # Validate content
            settings_content = (project_path / "core" / "settings.py").read_text()
            assert "rest_framework" in settings_content
            assert "corsheaders" in settings_content
            assert "rest_framework_simplejwt" in settings_content
            assert "ALLOWED_HOSTS" in settings_content
            assert "DATABASES" in settings_content

            # Check requirements
            req_content = (project_path / "requirements.txt").read_text()
            assert "Django" in req_content
            assert "djangorestframework" in req_content
            assert "djangorestframework-simplejwt" in req_content
            assert "django-cors-headers" in req_content

    def test_django_structure_postgres(self):
        """Test Django project with PostgreSQL generates database config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="django_pg_app",
                framework="django",
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="postgres",
            )
            builder.build()
            project_path = Path(tmpdir) / "django_pg_app"

            # Core files exist
            assert (project_path / "core" / "settings.py").exists()

            # Validate PostgreSQL config in settings
            settings_content = (project_path / "core" / "settings.py").read_text()
            assert "DJANGO_USE_POSTGRES" in settings_content
            assert "postgresql" in settings_content
            assert "POSTGRES_DB" in settings_content
            assert "POSTGRES_USER" in settings_content
            assert "POSTGRES_PASSWORD" in settings_content
            assert "POSTGRES_HOST" in settings_content
            assert "POSTGRES_PORT" in settings_content

            # Check requirements include psycopg2
            req_content = (project_path / "requirements.txt").read_text()
            assert "psycopg2-binary" in req_content

    def test_django_with_docker(self):
        """Test Django Docker integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="django_docker_app",
                framework="django",
                target_dir=tmpdir,
                docker=True,
                auth=False,
                database="postgres",
            )
            builder.build()
            project_path = Path(tmpdir) / "django_docker_app"

            # Docker files
            assert (project_path / "Dockerfile").exists()
            assert (project_path / "docker-compose.yml").exists()

            # Validate Dockerfile content
            dockerfile_content = (project_path / "Dockerfile").read_text()
            assert "python:3.12-slim" in dockerfile_content
            assert "pip install" in dockerfile_content
            assert "gunicorn" in dockerfile_content

            # Validate docker-compose.yml
            compose_content = (project_path / "docker-compose.yml").read_text()
            assert "services:" in compose_content
            assert "web:" in compose_content or "app:" in compose_content
            assert "postgres:" in compose_content or "db:" in compose_content

    def test_fastapi_structure(self):
        """Test FastAPI project generates required files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="fastapi_app",
                framework="fastapi",
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "fastapi_app"

            # Core files
            assert (project_path / "requirements.txt").exists()
            assert (project_path / "README.md").exists()

            # App package
            assert (project_path / "app" / "__init__.py").exists()
            assert (project_path / "app" / "main.py").exists()
            assert (project_path / "app" / "auth.py").exists()

            # Validate main.py content
            main_content = (project_path / "app" / "main.py").read_text()
            assert "FastAPI" in main_content
            assert "CORSMiddleware" in main_content
            assert "/health" in main_content
            assert "/token" in main_content
            assert "create_access_token" in main_content

            # Validate auth.py content
            auth_content = (project_path / "app" / "auth.py").read_text()
            assert "jwt" in auth_content
            assert "HTTPBearer" in auth_content
            assert "token_auth_dependency" in auth_content
            assert "SECRET_KEY" in auth_content

            # Validate requirements
            req_content = (project_path / "requirements.txt").read_text()
            assert "fastapi" in req_content
            assert "uvicorn" in req_content
            assert "pyjwt" in req_content
            assert "passlib" in req_content

    def test_fastapi_with_docker(self):
        """Test FastAPI Docker integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="fastapi_docker_app",
                framework="fastapi",
                target_dir=tmpdir,
                docker=True,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "fastapi_docker_app"

            # Docker files
            assert (project_path / "Dockerfile").exists()
            assert (project_path / "docker-compose.yml").exists()

            # Validate Dockerfile for FastAPI
            dockerfile_content = (project_path / "Dockerfile").read_text()
            assert "python:3.12-slim" in dockerfile_content
            assert "uvicorn" in dockerfile_content

    def test_nextjs_structure(self):
        """Test Next.js project generates required files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="nextjs_app",
                framework="nextjs",
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "nextjs_app"

            # Core files
            assert (project_path / "package.json").exists()
            assert (project_path / "tailwind.config.js").exists()
            assert (project_path / "postcss.config.js").exists()
            assert (project_path / "tsconfig.json").exists()
            assert (project_path / "next.config.js").exists()
            assert (project_path / "README.md").exists()

            # App directory
            app_path = project_path / "src" / "app"
            assert (app_path / "layout.tsx").exists()
            assert (app_path / "page.tsx").exists()
            assert (app_path / "globals.css").exists()

            # Validate package.json
            pkg_content = json.loads((project_path / "package.json").read_text())
            assert pkg_content["name"] == "nextjs_app"
            assert "next" in pkg_content["dependencies"]
            assert "react" in pkg_content["dependencies"]
            assert "tailwindcss" in pkg_content["dependencies"]

            # Validate page.tsx includes auth
            page_content = (app_path / "page.tsx").read_text()
            assert "'use client'" in page_content
            assert "useState" in page_content
            assert "handleLogin" in page_content

            # Validate tailwind.config.js
            tailwind_content = (project_path / "tailwind.config.js").read_text()
            assert "module.exports" in tailwind_content
            assert "content:" in tailwind_content

    def test_nextjs_with_docker(self):
        """Test Next.js Docker integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="nextjs_docker_app",
                framework="nextjs",
                target_dir=tmpdir,
                docker=True,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "nextjs_docker_app"

            # Docker files
            assert (project_path / "Dockerfile").exists()
            assert (project_path / "docker-compose.yml").exists()

            # Validate multi-stage Node Dockerfile
            dockerfile_content = (project_path / "Dockerfile").read_text()
            assert "node:20-alpine" in dockerfile_content
            assert "builder" in dockerfile_content
            assert "npm run build" in dockerfile_content

    def test_react_structure(self):
        """Test React project generates required files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="react_app",
                framework="react",
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "react_app"

            # Core files
            assert (project_path / "package.json").exists()
            assert (project_path / "vite.config.js").exists()
            assert (project_path / "index.html").exists()
            assert (project_path / "README.md").exists()

            # Src directory
            src_path = project_path / "src"
            assert (src_path / "App.jsx").exists()
            assert (src_path / "index.js").exists()
            assert (src_path / "styles.css").exists()

            # Validate package.json
            pkg_content = json.loads((project_path / "package.json").read_text())
            assert pkg_content["name"] == "react_app"
            assert "react" in pkg_content["dependencies"]
            assert "react-dom" in pkg_content["dependencies"]

            # Validate App.jsx has auth context
            app_content = (src_path / "App.jsx").read_text()
            assert "AuthContext" in app_content
            assert "createContext" in app_content
            assert "useState" in app_content
            assert "LoginForm" in app_content

    def test_react_with_docker(self):
        """Test React Docker integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="react_docker_app",
                framework="react",
                target_dir=tmpdir,
                docker=True,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "react_docker_app"

            # Docker files
            assert (project_path / "Dockerfile").exists()
            assert (project_path / "docker-compose.yml").exists()

            # Validate Dockerfile for React
            dockerfile_content = (project_path / "Dockerfile").read_text()
            assert "node:20-alpine" in dockerfile_content
            assert "nginx" in dockerfile_content

    def test_flutter_structure(self):
        """Test Flutter project generates required files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="flutter_app",
                framework="flutter",
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "flutter_app"

            # Core files
            assert (project_path / "pubspec.yaml").exists()
            assert (project_path / "README.md").exists()

            # Lib directory
            lib_path = project_path / "lib"
            assert (lib_path / "main.dart").exists()

            # Validate pubspec.yaml
            pubspec_content = (project_path / "pubspec.yaml").read_text()
            assert "name: flutter_app" in pubspec_content
            assert "flutter:" in pubspec_content
            assert "http:" in pubspec_content
            assert "provider:" in pubspec_content

            # Validate main.dart has auth flow
            main_content = (lib_path / "main.dart").read_text()
            assert "MaterialApp" in main_content
            assert "AuthState" in main_content
            assert "ChangeNotifier" in main_content
            assert "LoginPage" in main_content
            assert "HomePage" in main_content

    def test_flutter_with_docker(self):
        """Test Flutter Docker integration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="flutter_docker_app",
                framework="flutter",
                target_dir=tmpdir,
                docker=True,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "flutter_docker_app"

            # Docker files
            assert (project_path / "Dockerfile").exists()
            assert (project_path / "docker-compose.yml").exists()

    def test_project_already_exists(self):
        """Test that building in an existing project directory raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="existing_project",
                framework="django",
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="sqlite",
            )
            builder.build()

            # Try to build again in the same location
            builder2 = ProjectBuilder(
                project_name="existing_project",
                framework="fastapi",
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="sqlite",
            )
            with pytest.raises(FileExistsError):
                builder2.build()

    def test_invalid_framework_raises_error(self):
        """Test that invalid framework raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="Unsupported framework"):
                ProjectBuilder(
                    project_name="invalid_app",
                    framework="nonexistent",
                    target_dir=tmpdir,
                    docker=False,
                    auth=False,
                    database="sqlite",
                )

    def test_invalid_database_raises_error(self):
        """Test that invalid database raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="Unsupported database"):
                ProjectBuilder(
                    project_name="invalid_db_app",
                    framework="django",
                    target_dir=tmpdir,
                    docker=False,
                    auth=False,
                    database="mongodb",
                )

    def test_readme_content_quality(self):
        """Test that generated README files have meaningful content."""
        for framework in SUPPORTED_FRAMEWORKS:
            with tempfile.TemporaryDirectory() as tmpdir:
                builder = ProjectBuilder(
                    project_name="test_readme",
                    framework=framework,
                    target_dir=tmpdir,
                    docker=False,
                    auth=False,
                    database="sqlite",
                )
                builder.build()
                project_path = Path(tmpdir) / "test_readme"

                readme_path = project_path / "README.md"
                assert readme_path.exists()
                readme_content = readme_path.read_text()
                assert "test_readme" in readme_content
                assert framework in readme_content.lower() or "Orix" in readme_content
                assert len(readme_content) > 100  # Ensure meaningful content

    def test_django_api_views_functional(self):
        """Test Django API views are properly structured."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="django_api_test",
                framework="django",
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "django_api_test"

            views_content = (project_path / "api" / "views.py").read_text()
            assert "CurrentUserView" in views_content
            assert "APIView" in views_content
            assert "IsAuthenticated" in views_content
            assert "get" in views_content

    def test_fastapi_auth_implementation(self):
        """Test FastAPI auth implementation is complete."""
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = ProjectBuilder(
                project_name="fastapi_auth_test",
                framework="fastapi",
                target_dir=tmpdir,
                docker=False,
                auth=False,
                database="sqlite",
            )
            builder.build()
            project_path = Path(tmpdir) / "fastapi_auth_test"

            auth_content = (project_path / "app" / "auth.py").read_text()
            main_content = (project_path / "app" / "main.py").read_text()

            # Auth module
            assert "create_access_token" in auth_content
            assert "token_auth_dependency" in auth_content
            assert "HS256" in auth_content
            assert "SECRET_KEY" in auth_content

            # Main module
            assert "TokenRequest" in main_content
            assert "/token" in main_content
            assert "/secure" in main_content

    def test_all_files_are_utf8_encoded(self):
        """Test that all generated files are UTF-8 readable."""
        for framework in SUPPORTED_FRAMEWORKS:
            with tempfile.TemporaryDirectory() as tmpdir:
                builder = ProjectBuilder(
                    project_name="encoding_test",
                    framework=framework,
                    target_dir=tmpdir,
                    docker=False,
                    auth=False,
                    database="sqlite",
                )
                builder.build()
                project_path = Path(tmpdir) / "encoding_test"

                # Check all generated files can be read as UTF-8
                for file_path in project_path.rglob("*"):
                    if file_path.is_file() and not file_path.name.startswith("."):
                        try:
                            file_path.read_text(encoding="utf-8")
                        except UnicodeDecodeError:
                            pytest.fail(f"File {file_path} is not UTF-8 encoded")
