import shutil
from pathlib import Path

import nox

DIR = Path(__file__).parent.resolve()


@nox.session(python=["python3.11"])
def build(session: nox.Session) -> None:
    """Build the dist."""
    dist_path = DIR.joinpath("dist")
    if dist_path.exists():
        shutil.rmtree(dist_path)

    build_path = DIR.joinpath("build")
    if build_path.exists():
        shutil.rmtree(build_path)

    session.install("poetry")
    session.run("poetry", "build")

    # # publish pip package
    # session.install("twine")
    # session.run("twine", "upload", "dist/*")


@nox.session(python=["python3.11"])
def tests(session: nox.Session) -> None:
    """Run the tests."""
    session.install("-r", "requirements.txt")
    session.install('pytest')
    session.install("pytest-cov")
    session.run("pytest", "--cov=uuidtoimage")


@nox.session(python=["python3.11"])
def lint(session: nox.Session) -> None:
    """Run the linter checks."""
    session.install('flake8')
    session.install("-r", "requirements.txt")

    # lint the source code
    session.run(
        'flake8', 'uuidtoimage',
        '--docstring-convention', 'google',
        '--ignore=D100,D104',
    )

    # lint the tests
    session.run(
        'flake8', 'tests',
        '--docstring-convention', 'google',
        '--ignore=D100,D104'
    )
