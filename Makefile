.PHONY: local serve clean
local:
	python3 web.py

serve:
	@serve ~/working/object-publish/detective

clean:
	rm ~/working/object-publish/detective/large/*
	rm ~/working/object-publish/detective/small/*

sync:
	@rsync \
		--human-readable \
		--exclude .DS_Store \
		--archive --delete \
		--info=progress2 \
		~/working/object-publish/detective/ \
		aspen:/mnt/ssd/hosts/web/detective/


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
