all:
	dot http_mediawiki_pandora.gv -T svg > http_mediawiki_pandora.svg
	dot http_mediawiki_pandora.gv -T png > http_mediawiki_pandora.png

	dot solr.gv -T svg > solr.svg
	dot solr.gv -T png > solr.png

publish:
	s3cmd -c /etc/s3cmd/amazon_prod.cfg put *.tsv s3://wikia-data-flow-graphs/ --acl-public
	s3cmd -c /etc/s3cmd/amazon_prod.cfg put *.png s3://wikia-data-flow-graphs/ --acl-public
