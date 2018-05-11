tests:
	py.test

lint:
	pylint graphs/

install:
	pip install -e .[dev]
