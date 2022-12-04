.PHONY: runserver

requirements:
	pip3 install -r requirements.txt
runserver:
	python3 manage.py runserver


.DEFAULT_GOAL := runserver

