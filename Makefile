.PHONY: tests
init:
	pip install pipenv
	pipenv install --dev
tests:
	pipenv run python -m pytest --cov-report=xml --cov=notas tests/
coverage:
	codecov