# data-flow-graphs

[![Build Status](https://travis-ci.org/Wikia/data-flow-graphs.svg?branch=master)](https://travis-ci.org/Wikia/data-flow-graphs)

An open repository with scripts used to generate data-flow-graphs

![http_mediawiki_pandora svg](https://user-images.githubusercontent.com/1929317/39514518-af6bd5b2-4df7-11e8-95e8-def4ea279bb5.png)

A set of Python scripts used to generate TSV files that we use to [visualize how data flows at Wikia](https://github.com/macbre/data-flow-graph). It uses [`data_flow_graph` Python module](https://pypi.python.org/pypi/data_flow_graph).

## Install

* Clone the repository
* Set up virtualenv
* `make install`

## Data flow graphs

* [Internal HTTP requests to MediaWiki and Pandora services](https://github.com/Wikia/data-flow-graphs/blob/master/output/http_mediawiki_pandora.svg) (`http_pandora_mediawiki`, powered by GraphViz) / [PNG version](http://wikia-data-flow-graphs.s3.amazonaws.com/http_mediawiki_pandora.png)

These are refreshed daily via a cronjob and uploaded to a public Amazon's S3 bucket as both TSV and PNG files.
