import nox


@nox.session
def format(session):
    session.install("-r", "dev-requirements.txt")
    session.run("black", ".")


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def lint(session):
    session.install("-r", "dev-requirements.txt")
    session.install("-r", "requirements.txt")

    session.run("ruff", ".")
    session.run("mypy", ".")


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def test(session):
    session.install("-r", "dev-requirements.txt")
    session.install("-r", "requirements.txt")

    session.run("pytest", "-vv", ".")
