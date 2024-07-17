www = ~/working/object-publish/detective

.PHONY: local serve clean sync
local: $(www)/favicon.ico
	python3 web.py

serve:
	@serve $(www)

$(www)/favicon.ico: data/microscope.png
	convert data/microscope.png -define icon:auto-resize=16,32,48 favicon.ico

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
