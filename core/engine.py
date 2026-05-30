from __future__ import annotations

import json
import os
import shutil
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

SUPPORTED_FRAMEWORKS = ["django", "fastapi", "nextjs", "react", "flutter"]
SUPPORTED_DATABASES = ["sqlite", "postgres"]


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_directory(path.parent)
    path.write_text(content, encoding="utf-8")


def render_json(value: Any) -> str:
    return json.dumps(value, indent=2)


class ProjectBuilder:
    def __init__(self, project_name: str, framework: str, target_dir: str = ".", docker: bool = False, auth: bool = False, database: str = "sqlite") -> None:
        self.project_name = project_name.strip()
        self.framework = framework.lower().strip()
        self.target_dir = Path(target_dir).resolve()
        self.docker = docker
        self.auth = auth
        self.database = database.lower().strip()
        self.root_path = self.target_dir / self.project_name
        if self.framework not in SUPPORTED_FRAMEWORKS:
            raise ValueError(f"Unsupported framework: {self.framework}")
        if self.database not in SUPPORTED_DATABASES:
            raise ValueError(f"Unsupported database: {self.database}")

    def build(self) -> None:
        if self.root_path.exists():
            raise FileExistsError(f"Project directory already exists: {self.root_path}")

        with Progress(SpinnerColumn(), TextColumn("[bold green]{task.description}"), transient=True) as progress:
            task = progress.add_task("Creating project structure", total=None)
            self.root_path.mkdir(parents=True, exist_ok=False)
            if self.framework == "django":
                self._build_django()
            elif self.framework == "fastapi":
                self._build_fastapi()
            elif self.framework == "nextjs":
                self._build_nextjs()
            elif self.framework == "react":
                self._build_react()
            elif self.framework == "flutter":
                self._build_flutter()
            if self.docker:
                self._build_docker()
            progress.update(task, description="Finalizing project files")
        console.print(f":sparkles: [bold blue]Created [green]{self.project_name}[/green] with [cyan]{self.framework}[/cyan] support in [magenta]{self.root_path}[/magenta].")

    def _build_django(self) -> None:
        self._write_file(self.root_path / "manage.py", self._django_manage_py())
        core_path = self.root_path / "core"
        api_path = self.root_path / "api"
        ensure_directory(core_path)
        ensure_directory(api_path)
        self._write_file(core_path / "__init__.py", "")
        self._write_file(core_path / "settings.py", self._django_settings())
        self._write_file(core_path / "urls.py", self._django_urls())
        self._write_file(core_path / "wsgi.py", self._django_wsgi())
        self._write_file(core_path / "asgi.py", self._django_asgi())
        self._write_file(api_path / "__init__.py", "")
        self._write_file(api_path / "urls.py", self._django_api_urls())
        self._write_file(api_path / "views.py", self._django_api_views())
        self._write_file(self.root_path / "requirements.txt", self._django_requirements())
        self._write_file(self.root_path / "README.md", self._django_readme())

    def _build_fastapi(self) -> None:
        app_path = self.root_path / "app"
        ensure_directory(app_path)
        self._write_file(app_path / "__init__.py", "")
        self._write_file(app_path / "main.py", self._fastapi_main())
        self._write_file(app_path / "auth.py", self._fastapi_auth())
        self._write_file(self.root_path / "requirements.txt", self._fastapi_requirements())
        self._write_file(self.root_path / "README.md", self._fastapi_readme())

    def _build_nextjs(self) -> None:
        self._write_file(self.root_path / "package.json", self._nextjs_package_json())
        self._write_file(self.root_path / "tailwind.config.js", self._nextjs_tailwind_config())
        self._write_file(self.root_path / "postcss.config.js", self._nextjs_postcss_config())
        self._write_file(self.root_path / "tsconfig.json", self._nextjs_tsconfig())
        self._write_file(self.root_path / "next-env.d.ts", self._nextjs_env())
        self._write_file(self.root_path / "next.config.js", self._nextjs_config())
        src_app = self.root_path / "src" / "app"
        ensure_directory(src_app)
        self._write_file(src_app / "layout.tsx", self._nextjs_layout())
        self._write_file(src_app / "page.tsx", self._nextjs_page())
        self._write_file(src_app / "globals.css", self._nextjs_globals())
        self._write_file(self.root_path / "README.md", self._nextjs_readme())

    def _build_react(self) -> None:
        self._write_file(self.root_path / "package.json", self._react_package_json())
        self._write_file(self.root_path / "vite.config.js", self._react_vite_config())
        self._write_file(self.root_path / "index.html", self._react_index_html())
        src_path = self.root_path / "src"
        ensure_directory(src_path)
        self._write_file(src_path / "App.jsx", self._react_app_jsx())
        self._write_file(src_path / "index.js", self._react_index_js())
        self._write_file(src_path / "styles.css", self._react_styles_css())
        self._write_file(self.root_path / "README.md", self._react_readme())

    def _build_flutter(self) -> None:
        self._write_file(self.root_path / "pubspec.yaml", self._flutter_pubspec())
        lib_path = self.root_path / "lib"
        ensure_directory(lib_path)
        self._write_file(lib_path / "main.dart", self._flutter_main())
        self._write_file(self.root_path / "README.md", self._flutter_readme())

    def _build_docker(self) -> None:
        self._write_file(self.root_path / "Dockerfile", self._dockerfile())
        self._write_file(self.root_path / "docker-compose.yml", self._docker_compose())

    def _django_manage_py(self) -> str:
        return textwrap.dedent(f"""\
            #!/usr/bin/env python
            import os
            import sys

            def main() -> int:
                os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
                try:
                    from django.core.management import execute_from_command_line
                except ImportError as exc:
                    raise ImportError(
                        'Could not import Django. Ensure it is installed and available on your PYTHONPATH.'
                    ) from exc
                return execute_from_command_line(sys.argv)

            if __name__ == '__main__':
                raise SystemExit(main())
        """)

    def _django_settings(self) -> str:
        secret_key = "get_random_secret_key()"
        database_config = textwrap.dedent(
            """\
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }
            """
        )
        postgres_block = textwrap.dedent(
            """\
                if os.getenv('DJANGO_USE_POSTGRES', 'False').lower() in {'true', '1', 'yes'}:
                    DATABASES['default'] = {
                        'ENGINE': 'django.db.backends.postgresql',
                        'NAME': os.getenv('POSTGRES_DB', 'orix_db'),
                        'USER': os.getenv('POSTGRES_USER', 'orix_user'),
                        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'orix_pass'),
                        'HOST': os.getenv('POSTGRES_HOST', 'db'),
                        'PORT': os.getenv('POSTGRES_PORT', '5432'),
                    }
            """
        )
        return textwrap.dedent("""\
            import os
            from pathlib import Path
            from django.core.management.utils import get_random_secret_key

            BASE_DIR = Path(__file__).resolve().parent.parent
            SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())
            DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in {'true', '1', 'yes'}
            ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1').split()

            INSTALLED_APPS = [
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'rest_framework',
                'corsheaders',
                'rest_framework_simplejwt',
                'api',
            ]

            MIDDLEWARE = [
                'corsheaders.middleware.CorsMiddleware',
                'django.middleware.security.SecurityMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.middleware.clickjacking.XFrameOptionsMiddleware',
            ]

            ROOT_URLCONF = 'core.urls'

            TEMPLATES = [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': [],
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.template.context_processors.debug',
                            'django.template.context_processors.request',
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',
                        ],
                    },
                },
            ]

            WSGI_APPLICATION = 'core.wsgi.application'
            ASGI_APPLICATION = 'core.asgi.application'

            %s

            AUTH_PASSWORD_VALIDATORS = [
                {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
                {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
                {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
                {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
            ]

            LANGUAGE_CODE = 'en-us'
            TIME_ZONE = 'UTC'
            USE_I18N = True
            USE_L10N = True
            USE_TZ = True

            STATIC_URL = '/static/'
            DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

            REST_FRAMEWORK = {
                'DEFAULT_AUTHENTICATION_CLASSES': [
                    'rest_framework_simplejwt.authentication.JWTAuthentication',
                ],
                'DEFAULT_PERMISSION_CLASSES': [
                    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
                ],
            }

            CORS_ALLOW_ALL_ORIGINS = True
            CORS_ALLOW_CREDENTIALS = True
            CORS_ALLOW_HEADERS = ['*']
        """ % (database_config + postgres_block))

    def _django_urls(self) -> str:
        return textwrap.dedent("""\
            from django.contrib import admin
            from django.urls import path, include
            from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

            urlpatterns = [
                path('admin/', admin.site.urls),
                path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                path('api/user/', include('api.urls')),
            ]
        """)

    def _django_api_urls(self) -> str:
        return textwrap.dedent("""\
            from django.urls import path
            from .views import CurrentUserView

            urlpatterns = [
                path('', CurrentUserView.as_view(), name='current-user'),
            ]
        """)

    def _django_api_views(self) -> str:
        return textwrap.dedent("""\
            from rest_framework.permissions import IsAuthenticated
            from rest_framework.response import Response
            from rest_framework.views import APIView

            class CurrentUserView(APIView):
                permission_classes = [IsAuthenticated]

                def get(self, request):
                    return Response({
                        'username': request.user.username,
                        'email': request.user.email,
                        'is_staff': request.user.is_staff,
                    })
        """)

    def _django_wsgi(self) -> str:
        return textwrap.dedent("""\
            import os
            from django.core.wsgi import get_wsgi_application

            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
            application = get_wsgi_application()
        """)

    def _django_asgi(self) -> str:
        return textwrap.dedent("""\
            import os
            from django.core.asgi import get_asgi_application

            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
            application = get_asgi_application()
        """)

    def _django_requirements(self) -> str:
        packages = [
            'Django>=4.2',
            'djangorestframework>=3.14',
            'djangorestframework-simplejwt>=2.0',
            'django-cors-headers>=4.0',
        ]
        if self.database == 'postgres':
            packages.append('psycopg2-binary>=2.9')
        return '\n'.join(packages) + '\n'

    def _django_readme(self) -> str:
        return textwrap.dedent(f"""\
            # {self.project_name}

            Generated by Orix. This Django starter ships with Django REST Framework, JWT support via SimpleJWT, and CORS enabled for frontend integration.

            ## Quick start

            python -m pip install -r requirements.txt
            python manage.py migrate
            python manage.py runserver
        """)

    def _fastapi_main(self) -> str:
        return textwrap.dedent("""\
            from datetime import timedelta
            from fastapi import Depends, FastAPI, HTTPException, status
            from fastapi.middleware.cors import CORSMiddleware
            from pydantic import BaseModel

            from .auth import create_access_token, token_auth_dependency

            class TokenRequest(BaseModel):
                username: str
                password: str

            app = FastAPI(
                title='Orix FastAPI Starter',
                version='1.0.0',
                description='Modern FastAPI starter with JWT authentication and CORS support.',
            )

            app.add_middleware(
                CORSMiddleware,
                allow_origins=['*'],
                allow_credentials=True,
                allow_methods=['*'],
                allow_headers=['*'],
            )

            @app.get('/health')
            def health() -> dict:
                return {'status': 'ok', 'framework': 'fastapi'}

            @app.post('/token')
            def token(payload: TokenRequest) -> dict:
                if payload.username != 'admin' or payload.password != 'password':
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Invalid authentication credentials',
                    )
                access_token = create_access_token(subject=payload.username, expires_delta=timedelta(minutes=60))
                return {'access_token': access_token, 'token_type': 'bearer'}

            @app.get('/secure')
            def secure_route(username: str = Depends(token_auth_dependency)) -> dict:
                return {'message': f'Hello, {username}. You are authenticated.'}
        """)

    def _fastapi_auth(self) -> str:
        return textwrap.dedent("""\
            import os
            from datetime import datetime, timedelta
            from typing import Optional

            import jwt
            from fastapi import Depends, HTTPException, status
            from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

            SECRET_KEY = os.getenv('FASTAPI_SECRET_KEY', 'change-this-secret-key')
            ALGORITHM = 'HS256'
            ACCESS_TOKEN_EXPIRE_MINUTES = 60

            security = HTTPBearer()

            def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
                expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
                payload = {'sub': subject, 'exp': expire}
                return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

            def token_auth_dependency(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
                token = credentials.credentials
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    return payload.get('sub', 'anonymous')
                except jwt.PyJWTError as exc:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Could not validate authentication credentials',
                    ) from exc
        """)

    def _fastapi_requirements(self) -> str:
        return textwrap.dedent("""\
            fastapi>=0.110.0
            uvicorn>=0.24.0
            pyjwt>=2.8.0
            passlib[bcrypt]>=1.8.0
        """)

    def _fastapi_readme(self) -> str:
        return textwrap.dedent("""\
            # {project_name}

            FastAPI starter project with JWT authentication and open CORS middleware.

            ## Run locally

            python -m pip install -r requirements.txt
            uvicorn app.main:app --reload
        """.format(project_name=self.project_name))

    def _nextjs_package_json(self) -> str:
        return render_json(
            {
                "name": self.project_name,
                "private": True,
                "version": "0.1.0",
                "scripts": {
                    "dev": "next dev",
                    "build": "next build",
                    "start": "next start",
                    "lint": "next lint",
                },
                "dependencies": {
                    "next": "14.2.5",
                    "react": "18.3.1",
                    "react-dom": "18.3.1",
                    "tailwindcss": "3.4.4",
                    "postcss": "8.4.35",
                    "autoprefixer": "10.4.19",
                },
                "devDependencies": {
                    "typescript": "5.5.4",
                    "@types/react": "18.3.3",
                    "@types/react-dom": "18.3.0",
                },
            }
        )

    def _nextjs_tailwind_config(self) -> str:
        return textwrap.dedent("""\
            module.exports = {
              content: ['./src/**/*.{js,jsx,ts,tsx}'],
              theme: {
                extend: {},
              },
              plugins: [],
            }
        """)

    def _nextjs_postcss_config(self) -> str:
        return textwrap.dedent("""\
            module.exports = {
              plugins: {
                tailwindcss: {},
                autoprefixer: {},
              },
            }
        """)

    def _nextjs_tsconfig(self) -> str:
        return textwrap.dedent("""\
            {
              "compilerOptions": {
                "target": "es2020",
                "lib": ["dom", "dom.iterable", "esnext"],
                "allowJs": true,
                "skipLibCheck": true,
                "strict": true,
                "forceConsistentCasingInFileNames": true,
                "noEmit": true,
                "esModuleInterop": true,
                "module": "esnext",
                "moduleResolution": "node",
                "resolveJsonModule": true,
                "isolatedModules": true,
                "jsx": "preserve"
              },
              "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
              "exclude": ["node_modules"]
            }
        """)

    def _nextjs_env(self) -> str:
        return "/// <reference types=\"next\" />\n/// <reference types=\"next/image-types/global\" />\n\n// NOTE: This file should not be edited."

    def _nextjs_config(self) -> str:
        return textwrap.dedent("""\
            const nextConfig = {
              reactStrictMode: true,
            }
            module.exports = nextConfig
        """)

    def _nextjs_layout(self) -> str:
        return textwrap.dedent("""\
            import './globals.css'
            import type { Metadata } from 'next'

            export const metadata: Metadata = {
              title: 'Orix Next.js Starter',
              description: 'Next.js starter with Tailwind and App Router support.',
            }

            export default function RootLayout({ children }: { children: React.ReactNode }) {
              return (
                <html lang="en">
                  <body>{children}</body>
                </html>
              )
            }
        """)

    def _nextjs_page(self) -> str:
        return textwrap.dedent("""\
            'use client'

            import { useMemo, useState } from 'react'

            const validCredentials = {
              username: 'admin',
              password: 'password',
            }

            export default function Home() {
              const [username, setUsername] = useState('')
              const [password, setPassword] = useState('')
              const [user, setUser] = useState<string | null>(null)
              const [error, setError] = useState('')

              const isAuthenticated = useMemo(() => !!user, [user])

              const handleLogin = (event: React.FormEvent<HTMLFormElement>) => {
                event.preventDefault()
                if (username === validCredentials.username && password === validCredentials.password) {
                  setUser(username)
                  setError('')
                  setUsername('')
                  setPassword('')
                  return
                }
                setError('Invalid username or password. Use admin / password.')
              }

              const handleLogout = () => {
                setUser(null)
              }

              return (
                <main className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center px-6 py-12">
                  <div className="w-full max-w-3xl rounded-3xl border border-slate-800 bg-slate-900/95 p-10 shadow-2xl shadow-slate-950/40">
                    <div className="mb-10 text-center">
                      <p className="text-sm uppercase tracking-[0.35em] text-teal-400">Orix • Next.js + Tailwind</p>
                      <h1 className="mt-4 text-4xl font-semibold text-white sm:text-5xl">Modern auth-ready frontend starter</h1>
                      <p className="mt-4 text-slate-400">Client-side login demo with a responsive Tailwind layout and App Router support.</p>
                    </div>

                    {isAuthenticated ? (
                      <section className="space-y-6 rounded-3xl bg-slate-950 p-8 shadow-inner shadow-slate-900/60">
                        <h2 className="text-2xl font-semibold text-white">Welcome back, {user}!</h2>
                        <p className="text-slate-400">This starter includes a login flow that can be extended to API-backed authentication.</p>
                        <button onClick={handleLogout} className="w-full rounded-2xl bg-teal-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-teal-300">
                          Sign out
                        </button>
                      </section>
                    ) : (
                      <form onSubmit={handleLogin} className="space-y-6 rounded-3xl bg-slate-950 p-8 shadow-inner shadow-slate-900/60">
                        <div>
                          <label className="block text-sm font-medium text-slate-300">Username</label>
                          <input
                            value={username}
                            onChange={(event) => setUsername(event.target.value)}
                            className="mt-3 w-full rounded-2xl border border-slate-800 bg-slate-900 px-4 py-3 text-slate-100 outline-none transition focus:border-teal-400"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-slate-300">Password</label>
                          <input
                            type="password"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            className="mt-3 w-full rounded-2xl border border-slate-800 bg-slate-900 px-4 py-3 text-slate-100 outline-none transition focus:border-teal-400"
                          />
                        </div>

                        {error && <p className="text-sm text-rose-400">{error}</p>}

                        <button type="submit" className="w-full rounded-2xl bg-teal-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-teal-300">
                          Sign in
                        </button>
                      </form>
                    )}
                  </div>
                </main>
              )
            }
        """)

    def _nextjs_globals(self) -> str:
        return textwrap.dedent("""\
            @tailwind base;
            @tailwind components;
            @tailwind utilities;

            :root {
              color-scheme: dark;
            }

            html {
              scroll-behavior: smooth;
            }

            body {
              margin: 0;
              min-height: 100vh;
              font-family: Inter, ui-sans-serif, system-ui, sans-serif;
              background: #020617;
            }

            * {
              box-sizing: border-box;
            }
        """)

    def _nextjs_readme(self) -> str:
        return textwrap.dedent(f"""\
            # {self.project_name}

            Next.js starter with Tailwind CSS and App Router structure.

            ## Install

            npm install
            npm run dev
        """)

    def _react_package_json(self) -> str:
        return render_json(
            {
                "name": self.project_name,
                "private": True,
                "version": "0.1.0",
                "type": "module",
                "scripts": {
                    "dev": "vite",
                    "build": "vite build",
                    "preview": "vite preview",
                    "test": "echo \"No tests specified\" && exit 0",
                },
                "dependencies": {
                    "react": "18.3.1",
                    "react-dom": "18.3.1",
                    "react-router-dom": "6.14.2",
                },
                "devDependencies": {
                    "@vitejs/plugin-react": "4.3.1",
                    "vite": "5.4.1",
                },
            }
        )

    def _react_vite_config(self) -> str:
        return textwrap.dedent("""\
            import { defineConfig } from 'vite'
            import react from '@vitejs/plugin-react'

            export default defineConfig({
              plugins: [react()],
            })
        """)

    def _react_index_html(self) -> str:
        return textwrap.dedent("""\
            <!DOCTYPE html>
            <html lang="en">
              <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Orix React Starter</title>
              </head>
              <body>
                <div id="root"></div>
                <script type="module" src="/src/index.js"></script>
              </body>
            </html>
        """)

    def _react_app_jsx(self) -> str:
        return textwrap.dedent("""\
            import { createContext, useContext, useState } from 'react'
            import './styles.css'

            const AuthContext = createContext(null)

            function AuthProvider({ children }) {
              const [user, setUser] = useState(null)
              const login = (username, password) => {
                if (username === 'admin' && password === 'password') {
                  setUser({ username })
                  return true
                }
                return false
              }

              const logout = () => setUser(null)

              return (
                <AuthContext.Provider value={{ user, login, logout }}>
                  {children}
                </AuthContext.Provider>
              )
            }

            function LoginForm() {
              const { login } = useContext(AuthContext)
              const [username, setUsername] = useState('')
              const [password, setPassword] = useState('')
              const [error, setError] = useState('')

              const handleSubmit = (event) => {
                event.preventDefault()
                const success = login(username, password)
                setError(success ? '' : 'Invalid credentials. Try admin/password.')
              }

              return (
                <form onSubmit={handleSubmit} className="card">
                  <h1>Log in</h1>
                  <label>
                    Username
                    <input value={username} onChange={(event) => setUsername(event.target.value)} />
                  </label>
                  <label>
                    Password
                    <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
                  </label>
                  <button type="submit">Sign in</button>
                  {error && <p className="error">{error}</p>}
                </form>
              )
            }

            function Dashboard() {
              const { user, logout } = useContext(AuthContext)
              return (
                <div className="card">
                  <h1>Welcome back, {user.username}</h1>
                  <p>This React starter shows a basic auth flow using context.</p>
                  <button onClick={logout}>Sign out</button>
                </div>
              )
            }

            export default function App() {
              const { user } = useContext(AuthContext)
              return (
                <AuthProvider>
                  <main className="page-shell">
                    <section className="hero">
                      <h1>Orix React Starter</h1>
                      <p>Modern, lightweight app shell with auth context.</p>
                    </section>
                    {user ? <Dashboard /> : <LoginForm />}
                  </main>
                </AuthProvider>
              )
            }
        """)

    def _react_index_js(self) -> str:
        return textwrap.dedent("""\
            import React from 'react'
            import ReactDOM from 'react-dom/client'
            import App from './App'

            ReactDOM.createRoot(document.getElementById('root')).render(
              <React.StrictMode>
                <App />
              </React.StrictMode>
            )
        """)

    def _react_styles_css(self) -> str:
        return textwrap.dedent("""\
            :root {
              color-scheme: dark;
              font-family: Inter, system-ui, sans-serif;
              background: #0f172a;
              color: #e2e8f0;
            }

            body {
              margin: 0;
              min-height: 100vh;
            }

            .page-shell {
              display: grid;
              place-items: center;
              min-height: 100vh;
              gap: 2rem;
              padding: 2rem;
            }

            .hero {
              text-align: center;
              max-width: 44rem;
            }

            .card {
              background: rgba(15, 23, 42, 0.96);
              border: 1px solid rgba(148, 163, 184, 0.16);
              border-radius: 1rem;
              box-shadow: 0 20px 60px rgba(15, 23, 42, 0.35);
              padding: 2rem;
              width: min(100%, 420px);
            }

            label {
              display: block;
              margin-top: 1rem;
              font-size: 0.95rem;
            }

            input {
              width: 100%;
              margin-top: 0.5rem;
              padding: 0.95rem 1rem;
              border-radius: 0.75rem;
              border: 1px solid rgba(148, 163, 184, 0.4);
              background: #020617;
              color: #e2e8f0;
            }

            button {
              margin-top: 1.5rem;
              width: 100%;
              padding: 1rem;
              border: none;
              border-radius: 0.75rem;
              background: #38bdf8;
              color: #020617;
              font-weight: 700;
              cursor: pointer;
            }

            .error {
              margin-top: 1rem;
              color: #fb7185;
            }
        """)

    def _react_readme(self) -> str:
        return textwrap.dedent(f"""\
            # {self.project_name}

            Vite-powered React starter with auth context scaffolding.

            ## Install

            npm install
            npm run dev
        """)

    def _flutter_pubspec(self) -> str:
        return textwrap.dedent(f"""\
            name: {self.project_name.lower().replace(' ', '_')}
            description: A new Flutter project generated by Orix.
            publish_to: 'none'
            version: 1.0.0+1
            environment:
              sdk: '>=2.19.0 <4.0.0'

            dependencies:
              flutter:
                sdk: flutter
              cupertino_icons: ^1.0.5
              http: ^1.1.0
              provider: ^6.0.7

            dev_dependencies:
              flutter_test:
                sdk: flutter
              flutter_lints: ^2.0.1

            flutter:
              uses-material-design: true
        """)

    def _flutter_main(self) -> str:
        return textwrap.dedent("""\
            import 'package:flutter/material.dart';
            import 'package:provider/provider.dart';
            import 'package:http/http.dart' as http;

            void main() {
              runApp(const OrixApp());
            }

            class AuthState extends ChangeNotifier {
              bool _signedIn = false;
              String _username = '';
              bool get signedIn => _signedIn;
              String get username => _username;

              Future<bool> login(String username, String password) async {
                final response = await http.get(Uri.parse('https://httpbin.org/get'));
                if (response.statusCode == 200 && username == 'admin' && password == 'password') {
                  _signedIn = true;
                  _username = username;
                  notifyListeners();
                  return true;
                }
                return false;
              }

              void logout() {
                _signedIn = false;
                _username = '';
                notifyListeners();
              }
            }

            class OrixApp extends StatelessWidget {
              const OrixApp({super.key});

              @override
              Widget build(BuildContext context) {
                return ChangeNotifierProvider(
                  create: (_) => AuthState(),
                  child: MaterialApp(
                    title: 'Orix Flutter Starter',
                    theme: ThemeData(
                      colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
                      useMaterial3: true,
                    ),
                    home: const AuthGate(),
                  ),
                );
              }
            }

            class AuthGate extends StatelessWidget {
              const AuthGate({super.key});

              @override
              Widget build(BuildContext context) {
                final auth = Provider.of<AuthState>(context);
                return auth.signedIn ? HomePage(username: auth.username) : const LoginPage();
              }
            }

            class LoginPage extends StatefulWidget {
              const LoginPage({super.key});

              @override
              State<LoginPage> createState() => _LoginPageState();
            }

            class _LoginPageState extends State<LoginPage> {
              final TextEditingController _usernameController = TextEditingController();
              final TextEditingController _passwordController = TextEditingController();
              String _error = '';
              bool _isLoading = false;

              @override
              Widget dispose() {
                _usernameController.dispose();
                _passwordController.dispose();
                super.dispose();
              }

              Future<void> _submit() async {
                setState(() {
                  _isLoading = true;
                  _error = '';
                });
                final auth = Provider.of<AuthState>(context, listen: false);
                final success = await auth.login(
                  _usernameController.text.trim(),
                  _passwordController.text.trim(),
                );
                setState(() {
                  _isLoading = false;
                  _error = success ? '' : 'Use admin / password to continue.';
                });
              }

              @override
              Widget build(BuildContext context) {
                return Scaffold(
                  appBar: AppBar(title: const Text('Orix Flutter Starter')),
                  body: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        const Text(
                          'Sign in to Orix',
                          style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 24),
                        TextField(
                          controller: _usernameController,
                          decoration: const InputDecoration(labelText: 'Username'),
                        ),
                        const SizedBox(height: 16),
                        TextField(
                          controller: _passwordController,
                          obscureText: true,
                          decoration: const InputDecoration(labelText: 'Password'),
                        ),
                        const SizedBox(height: 24),
                        FilledButton.tonal(
                          onPressed: _isLoading ? null : _submit,
                          child: _isLoading ? const CircularProgressIndicator() : const Text('Sign in'),
                        ),
                        if (_error.isNotEmpty)
                          Padding(
                            padding: const EdgeInsets.only(top: 12.0),
                            child: Text(
                              _error,
                              style: const TextStyle(color: Colors.redAccent),
                              textAlign: TextAlign.center,
                            ),
                          ),
                      ],
                    ),
                  ),
                );
              }
            }

            class HomePage extends StatelessWidget {
              final String username;
              const HomePage({required this.username, super.key});

              @override
              Widget build(BuildContext context) {
                final auth = Provider.of<AuthState>(context, listen: false);
                return Scaffold(
                  appBar: AppBar(
                    title: const Text('Welcome'),
                    actions: [
                      IconButton(
                        icon: const Icon(Icons.logout),
                        onPressed: auth.logout,
                      ),
                    ],
                  ),
                  body: Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text('Welcome back, $username!', style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
                          const SizedBox(height: 12),
                          const Text('Your mobile starter includes provider state management and a modular route-ready shell.'),
                        ],
                      ),
                    ),
                  ),
                );
              }
            }
        """)

    def _flutter_readme(self) -> str:
        return textwrap.dedent(f"""\
            # {self.project_name}

            Flutter mobile starter with Provider state management and a login flow.

            ## Run locally

            flutter pub get
            flutter run
        """)

    def _dockerfile(self) -> str:
        if self.framework == 'django':
            return textwrap.dedent("""\
                FROM python:3.12-slim AS base
                WORKDIR /app
                ENV PYTHONDONTWRITEBYTECODE=1
                ENV PYTHONUNBUFFERED=1

                COPY requirements.txt .
                RUN pip install --upgrade pip && pip install -r requirements.txt

                COPY . .
                EXPOSE 8000
                CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
            """)
        if self.framework == 'fastapi':
            return textwrap.dedent("""\
                FROM python:3.12-slim AS base
                WORKDIR /app
                ENV PYTHONDONTWRITEBYTECODE=1
                ENV PYTHONUNBUFFERED=1

                COPY requirements.txt .
                RUN pip install --upgrade pip && pip install -r requirements.txt

                COPY . .
                EXPOSE 8000
                CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
            """)
        if self.framework == 'nextjs':
            return textwrap.dedent("""\
                FROM node:20-alpine AS builder
                WORKDIR /app
                COPY package.json package-lock.json* ./
                RUN npm install
                COPY . .
                RUN npm run build

                FROM node:20-alpine AS runner
                WORKDIR /app
                COPY --from=builder /app/package.json ./
                COPY --from=builder /app/node_modules ./node_modules
                COPY --from=builder /app/.next ./ .next
                COPY --from=builder /app/public ./public
                EXPOSE 3000
                CMD ["npm", "start"]
            """)
        if self.framework == 'react':
            return textwrap.dedent("""\
                FROM node:20-alpine AS builder
                WORKDIR /app
                COPY package.json package-lock.json* ./
                RUN npm install
                COPY . .
                RUN npm run build

                FROM nginx:stable-alpine
                COPY --from=builder /app/dist /usr/share/nginx/html
                EXPOSE 80
                CMD ["nginx", "-g", "daemon off;"]
            """)
        if self.framework == 'flutter':
            return textwrap.dedent("""\
                FROM google/dart:stable AS build
                WORKDIR /app
                COPY pubspec.* ./
                RUN dart pub get
                COPY . .
                RUN dart pub get

                FROM google/dart-runtime:stable
                WORKDIR /app
                COPY --from=build /app .
                CMD ["dart", "run"]
            """)
        return ""

    def _docker_compose(self) -> str:
        if self.framework in {'django', 'fastapi'}:
            service_name = 'web'
            web_port = '8000'
            db_service = ''
            db_volumes = ''
            environment = '      - DJANGO_USE_POSTGRES=True\n      - POSTGRES_DB=orix_db\n      - POSTGRES_USER=orix_user\n      - POSTGRES_PASSWORD=orix_pass\n      - POSTGRES_HOST=db\n      - POSTGRES_PORT=5432\n' if self.database == 'postgres' else ''
            depends_on = '      - db\n' if self.database == 'postgres' else ''
            db_service = textwrap.dedent("""\
                db:
                  image: postgres:15
                  restart: unless-stopped
                  environment:
                    POSTGRES_DB: orix_db
                    POSTGRES_USER: orix_user
                    POSTGRES_PASSWORD: orix_pass
                  volumes:
                    - postgres_data:/var/lib/postgresql/data
            """) if self.database == 'postgres' else ''
            db_volumes = 'volumes:\n  postgres_data:' if self.database == 'postgres' else ''
            return textwrap.dedent(f"""\
                version: '3.9'
                services:
                  {service_name}:
                    build: .
                    ports:
                      - '{web_port}:{web_port}'
                    environment:
{environment if environment else '      - PYTHONUNBUFFERED=1\n'}
{depends_on if depends_on else ''}
                    volumes:
                      - .:/app
{db_service if db_service else ''}
                {db_volumes}
            """)
        if self.framework == 'nextjs':
            return textwrap.dedent("""\
                version: '3.9'
                services:
                  app:
                    build: .
                    ports:
                      - '3000:3000'
                    environment:
                      - NODE_ENV=production
            """)
        if self.framework == 'react':
            return textwrap.dedent("""\
                version: '3.9'
                services:
                  frontend:
                    build: .
                    ports:
                      - '80:80'
            """)
        if self.framework == 'flutter':
            return textwrap.dedent("""\
                version: '3.9'
                services:
                  flutter:
                    build: .
                    ports:
                      - '8080:8080'
            """)
        return ''
