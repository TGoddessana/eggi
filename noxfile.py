import nox
from nox_poetry import Session, session

package = "eggi"
python_versions = [
    "3.12",
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


@session(name="mkdocs-build", python=python_versions[0])
def mkdocs_build(_session: Session) -> None:
    """Build the documentation."""
    _session.install(".")
    _session.run("pip", "install", "-r", "requirements/docs.txt")
    mkdocs_args = _session.posargs or ["build"]

    _session.run("mkdocs", *mkdocs_args)


@session(name="mkdocs-serve", python=python_versions[0])
def mkdocs_serve(_session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    _session.install(".")
    _session.run("pip", "install", "-r", "requirements/docs.txt")
    mkdocs_args = _session.posargs or ["serve"]

    _session.run("mkdocs", *mkdocs_args)
