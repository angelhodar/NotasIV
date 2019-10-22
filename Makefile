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
	pipenv run pm2 start "uwsgi --http 127.0.0.1:5000 --module app:app --master --processes 4 --threads 2" --name app
	@if [ $$? -eq 0 ]; then\
		$(MAKE) delete;\
	fi
stop:
	pipenv run pm2 stop app
delete:
	pipenv run pm2 delete app
restart:
	pipenv run pm2 restart app
clean:
	rm coverage.xml .coverage
	cd docs && make clean