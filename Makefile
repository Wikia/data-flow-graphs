tests:
	py.test

lint:
	pylint graphs/

install:
	pip install -e .[dev]

generate:
	http_pandora_mediawiki
	solr
