# data-flow-graphs
An open repository with scripts used to generate data-flow-graphs

![](https://raw.githubusercontent.com/macbre/data-flow-graph/master/docs/data-flow-example.png)

A set of Python scripts used to generate TSV files that we use to [visualize how data flows at Wikia](https://github.com/macbre/data-flow-graph). It uses [`data_flow_graph` Python module](https://pypi.python.org/pypi/data_flow_graph).

## Install

* Clone the repository
* Set up virtualenv
* `make install`

## Data flow graphs

* [HTTP requests sent by MediaWiki grouped by caller](https://macbre.github.io/data-flow-graph/gist.html#3ac2c20a4e059ab263c4c92507d18e26) (`http_requests_graph`)
* [Internal HTTP requests to MediaWiki and Pandora services](https://github.com/Wikia/data-flow-graphs/blob/master/output/http_mediawiki_pandora.svg) (`http_pandora_mediawiki`, powered by GraphViz)
