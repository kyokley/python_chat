.PHONY: build shell tests

build:
	docker build -t kyokley/python_chat .

shell:
	docker run --rm -it -v $(pwd):/workspace kyokley/python_chat /bin/bash

tests:
	docker run --rm -it -v $(pwd):/workspace kyokley/python_chat /bin/bash -c "pytest"
