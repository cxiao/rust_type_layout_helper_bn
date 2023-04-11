import nox


@nox.session
def format(session):
    session.install("-r", "dev-requirements.txt")
    session.run("black", ".")


@nox.session
def lint(session):
    session.install("-r", "dev-requirements.txt")
    session.install("-r", "requirements.txt")

    session.run("ruff", ".")
    session.run("mypy", ".")
