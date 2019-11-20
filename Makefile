.PHONY: tests docs clean
init:
	pip install pipenv
	pipenv install --dev
pm2:
	sudo apt update
	sudo apt install -y nodejs
	sudo apt install -y npm
	sudo npm install -g pm2
tests:
	pipenv run python -m pytest -p no:warnings --cov-report=xml --cov=notas tests/
coverage:
	pipenv run codecov
docs:
	cd docs && pipenv run make html
start:
	pipenv run pm2 start "gunicorn -b 127.0.0.1:$(PORT) app:app" --name app
start-no-pm2:
	pipenv run gunicorn -b 0.0.0.0:$(PORT) app:app
stop:
	pipenv run pm2 stop app
delete:
	pipenv run pm2 delete app
restart:
	pipenv run pm2 restart app
heroku:
	sudo snap install heroku --classic
	heroku login
	heroku create notas-iv --buildpack heroku/python
	git push heroku master
clean:
	rm -f coverage.xml .coverage
	cd docs && make clean
