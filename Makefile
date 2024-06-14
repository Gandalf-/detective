www = ~/working/object-publish/detective

.PHONY: local serve clean sync
local:
	python3 web.py

serve:
	@serve $(www)

clean:
	rm $(www)/{large,small}/*

sync:
	@rsync \
		--human-readable \
		--exclude .DS_Store \
		--archive \
		--delete \
		--info=progress2 \
		$(www)/ \
		aspen:/mnt/ssd/hosts/web/detective/


.PHONY: lint python html format
lint: python html

python:
	mypy .
	ruff check --fix .

html:
	tidy -q -e $(www)/index.html

format:
	isort --jobs -1 *.py */*.py
	ruff format *.py */*.py


.PHONY: test
test:
	python3 -m unittest
