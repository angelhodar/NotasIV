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
start:
	touch tmp.pid
	pipenv run uwsgi --http 127.0.0.1:5000 --module app:app --master --processes 4 --threads 2 --safe-pidfile tmp.pid
stop:
	pipenv run uwsgi --stop tmp.pid
reload:
	pipenv run uwsgi --reload tmp.pid
clean:
	rm coverage.xml .coverage
	cd docs && make clean