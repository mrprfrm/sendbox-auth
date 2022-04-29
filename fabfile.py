from fabric.api import local


def run():
    local(
        "export FLASK_ENV=development FLASK_APP=app/; poetry run flask run"
    )


def lint(path="."):
    local(f"poetry run isort {path}")
    local(f"poetry run black {path}")
    local(f"poetry run flake8 {path}")


def test(path="."):
    local(f"export AUTH_DATABASE_NAME=test; poetry run pytest -s {path}")


def initdb():
    local('poetry run flask db init')


def migrate():
    local('poetry run flask db migrate')


def upgrade():
    local('poetry run flask db upgrade')


def createdb():
    local(f'export AUTH_DATABASE_NAME=test; poetry run flask createdb')
