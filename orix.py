import sys
from pathlib import Path

import click
import questionary
from rich.console import Console
from rich.panel import Panel

from core.engine import ProjectBuilder, SUPPORTED_DATABASES, SUPPORTED_FRAMEWORKS

console = Console()


def _prompt_project_name() -> str:
    return questionary.text("Project name", default="orix-project").ask() or "orix-project"


def _prompt_framework() -> str:
    return questionary.select(
        "Choose a framework",
        choices=[framework.title() for framework in SUPPORTED_FRAMEWORKS],
    ).ask().lower()


def _prompt_database() -> str:
    return questionary.select(
        "Choose a database",
        choices=[db.upper() for db in SUPPORTED_DATABASES],
    ).ask().lower()


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("project_name", required=False)
@click.option("--framework", type=click.Choice(SUPPORTED_FRAMEWORKS, case_sensitive=False), help="Choose the stack to scaffold.")
@click.option("--docker", is_flag=True, help="Generate Dockerfile and docker-compose.yml for the project.")
@click.option("--auth", is_flag=True, help="Include authentication scaffolding where appropriate.")
@click.option("--database", type=click.Choice(SUPPORTED_DATABASES, case_sensitive=False), default="sqlite", show_default=True, help="Database backend for server stacks.")
@click.option("--output-dir", type=click.Path(), default=".", help="Directory where the project will be generated.")
def main(project_name: str, framework: str, docker: bool, auth: bool, database: str, output_dir: str) -> None:
    """Orix is a lightweight, premium scaffolder for Django, FastAPI, Next.js, React, and Flutter."""
    console.clear()
    console.print(Panel.fit("[bold magenta]Orix[/bold magenta] - Kryonara scaffolding engine", subtitle="Create modern full-stack projects instantly", border_style="bright_magenta"))

    interactive = sys.stdin.isatty() and sys.stdout.isatty()
    if not project_name and interactive:
        project_name = _prompt_project_name()
    if not framework and interactive:
        framework = _prompt_framework()
    if interactive and framework in {"django", "fastapi"} and not database:
        database = _prompt_database()

    if not project_name or not framework:
        console.print("[bold red]Error:[/bold red] project name and framework are required when running non-interactively.")
        raise click.Abort()

    project_name = project_name.strip()
    framework = framework.lower().strip()
    database = database.lower().strip()
    if database not in SUPPORTED_DATABASES:
        console.print(f"[bold red]Error:[/bold red] unsupported database: {database}")
        raise click.Abort()

    builder = ProjectBuilder(
        project_name=project_name,
        framework=framework,
        target_dir=output_dir,
        docker=docker,
        auth=auth,
        database=database,
    )

    try:
        builder.build()
        console.print()
        console.print(f"[bold green]Success:[/bold green] {project_name} generated at [cyan]{Path(output_dir).resolve() / project_name}[/cyan].")
        console.print(f"Use [yellow]cd {project_name}[/yellow] and follow README instructions.")
    except FileExistsError as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise click.Abort()
    except Exception as exc:
        console.print(f"[bold red]Unexpected error:[/bold red] {exc}")
        raise click.Abort()


if __name__ == "__main__":
    main()
