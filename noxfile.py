import os
import nox

PYTHON_FILES = [
    "pelican_gemini_capsule.py",
    "noxfile.py",
]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("-e", ".[dev]")
    session.run("flake8", *PYTHON_FILES)
    session.run("black", "--check", "--diff", "--color", *PYTHON_FILES)
    session.run("validate-pyproject", "pyproject.toml")


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("black")
    session.run("black", *PYTHON_FILES)


@nox.session(reuse_venv=True)
def test(session):
    session.install("pelican")
    session.install("-e", ".")
    with session.chdir("./test/pelican-site/"):
        session.run(
            "pelican", "./content/", "-o", "./output/", "-s", "./pelicanconf.py"
        )
    with session.chdir("./test/pelican-site/output"):
        assert os.path.isfile("article-1.html")
        assert os.path.isfile("article-1.gmi")
