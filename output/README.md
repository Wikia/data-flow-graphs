Output
======

Here are the files generated using Python script registered in `setup.py` file.

### Http traffic to MediaWiki and Pandora services

```
http_pandora_mediawiki
```

### GraphViz

> See [`data-flow-graph` repository](https://github.com/macbre/data-flow-graph/tree/master/examples#gv-file) for more examples

`apt-get install graphviz` and then run:

```
dot http_mediawiki_pandora.gv -T svg > http_mediawiki_pandora.svg
```

![](https://raw.githubusercontent.com/Wikia/data-flow-graphs/master/output/http_mediawiki_pandora.png)
