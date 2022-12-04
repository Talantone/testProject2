.PHONY: runserver

requirements:
	pip3 install -r requirements.txt
runserver:
	python3 manage.py runserver
run_tests:
	python3 manage.py test .
tests_report:
	coverage run --source='.' ./manage.py test .
	coverage report

.DEFAULT_GOAL := runserver

