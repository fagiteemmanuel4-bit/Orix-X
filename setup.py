from setuptools import find_packages, setup

from pathlib import Path

here = Path(__file__).resolve().parent
long_description = (here / "README.md").read_text(encoding="utf-8") if (here / "README.md").exists() else "Orix is a lightweight scaffolder for modern full-stack projects."

setup(
    name="orix",
    version="0.1.0",
    description="Orix CLI scaffolder for Django, FastAPI, Next.js, React, and Flutter.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kryonara",
    author_email="support@kryonara.com",
    python_requires=">=3.10",
    packages=find_packages(include=["core", "core.*"]),
    py_modules=["orix"],
    install_requires=[
        "click>=8.1.0",
        "questionary>=1.12.0",
        "rich>=13.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "orix=orix:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
