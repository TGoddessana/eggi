from pathlib import Path

import nox
from nox_poetry import Session, session

package = "eggi"
python_versions = [
    "3.11",
    "3.10",
    "3.9",
    "3.8",
]
nox.options.sessions = (
    "pre-commit",
    "mypy",
    "mkdocs-build",
)


@session(name="pre-commit", python=python_versions[0])
def pre_commit(_session: Session) -> None:
    """Lint using pre-commit."""
    _session.install(".")
    _session.install("pre-commit")

    pre_commit_args = _session.posargs or [
        "run",
        "--all-files",
        "--hook-stage=manual",
        "--show-diff-on-failure",
    ]

    _session.run("pre-commit", *pre_commit_args)


@session(python=python_versions)
def mypy(_session: Session) -> None:
    """Type-check using mypy."""
    _session.install(".")
    _session.install("mypy")

    mypy_args = _session.posargs or [
        "eggi",
    ]

    _session.run("mypy", *mypy_args)


@session(name="tests", python=python_versions)
def tests(_session: Session) -> None:
    """Run the test suite."""
    _session.install(".")
    _session.install("pytest")
    _session.install("coverage[toml]")

    pytest_args = _session.posargs or [
        ".",
    ]
    try:
        _session.run("coverage", "run", "--parallel", "-m", "pytest", *pytest_args)
    finally:
        if _session.interactive:
            _session.notify("coverage", posargs=[])


@session(python=python_versions[0])
def coverage(_session: Session) -> None:
    """Produce the coverage report."""
    args = _session.posargs or ["report"]
    _session.install("coverage[toml]")

    if not _session.posargs and any(Path().glob(".coverage.*")):
        _session.run("coverage", "combine")

    _session.run("coverage", *args)


@session(name="mkdocs-build", python=python_versions[0])
def mkdocs_build(_session: Session) -> None:
    """Build the documentation."""
    _session.install(".")
    _session.install("mkdocs", "mkdocs-material", "mkdocstrings[crystal,python]")
    mkdocs_args = _session.posargs or ["build"]

    _session.run("mkdocs", *mkdocs_args)


@session(name="mkdocs-serve", python=python_versions[0])
def mkdocs_serve(_session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    _session.install(".")
    _session.install("mkdocs", "mkdocs-material", "mkdocstrings[crystal,python]")
    mkdocs_args = _session.posargs or ["serve"]

    _session.run("mkdocs", *mkdocs_args)
