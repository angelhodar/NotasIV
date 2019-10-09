.PHONY: tests clean
init:
	pip install pipenv
	pipenv install --dev
tests:
	pipenv run python -m pytest --cov-report=xml --cov=notas tests/
coverage:
	codecov
clean:
	rm coverage.xml .coverage