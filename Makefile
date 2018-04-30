tests:
	py.test

install:
	pip install -e .[dev] --index-url https://artifactory.wikia-inc.com/artifactory/api/pypi/pypi/simple
