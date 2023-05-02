isort model

for file in model/*.py; do black "$file"; done

mypy model

for file in model/*.py; do pylint "$file"; done

bandit -c pyproject.toml -r model
