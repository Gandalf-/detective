.PHONY: lint shellcheck mypy ruff format
lint: mypy ruff

mypy:
	mypy .

ruff:
	ruff check --fix .

format:
	isort --jobs -1 *.py */*.py
	ruff format *.py */*.py


.PHONY: test unittest
test: unittest

unittest:
	python3 -m unittest