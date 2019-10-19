.PHONY: tests docs clean
init:
	pip install pipenv
	pipenv install --dev
tests:
	pipenv run python -m pytest -p no:warnings --cov-report=xml --cov=notas tests/
coverage:
	codecov
docs:
	cd docs && make html
clean:
	rm coverage.xml .coverage
	cd docs && make clean