.PHONY: lint shellcheck mypy ruff format
lint: mypy ruff

mypy:
	mypy .

ruff:
	ruff check --fix .

format:
	isort --jobs -1 *.py
	ruff format *.py


.PHONY: test unittest serve
test: unittest

unittest:
	python3 -m unittest

serve:
	@serve ~/working/object-publish/detective
