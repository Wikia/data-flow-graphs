"""
This script will generate a data-flow-graph for Solr search engine
and clients that communicate with it either to make a search query or update a Solr document
"""
from __future__ import print_function

from data_flow_graph import format_tsv_lines, format_graphviz_lines, logs_map_and_reduce
from wikia_common_kibana import Kibana

from .utils import get_solr_parameters, get_solr_core_name


def get_solr_flow_graph(limit, period):
    """
    :type limit int
    :type period int
    :rtype: list[dict]
    """
    rows = Kibana(period=period, index_prefix='logstash-solr').query_by_string(
        query='@source_host.keyword: /search-s.*/ AND @message: "webapp"',
        fields=[
            '@message',
        ],
        limit=limit
    )

    # extract required fields only
    # core name and method name
    rows = [
        (
            get_solr_core_name(row.get('@message')),
            str(get_solr_parameters(row.get('@message')).get('path', '')).strip('/'),
        )
        for row in rows
    ]

    # process the logs
    def _map(item):
        return '{}'.join(item)

    def _reduce(items):
        first = items[0]
        index = first[0]
        method = first[1]
        client = 'client'  # add a user agent to the logs and identify the client based on it

        return {
            'source': 'solr:{}'.format(index) if method == 'select' else 'indexer',
            'edge': 'http',
            'target': 'solr:{}'.format(index) if method != 'select' else client,
            # the following is optional
            'metadata': '{:.3f} reqs per sec'.format(1. * len(items) / period)
        }

    return logs_map_and_reduce(rows, _map, _reduce)


def main():
    """
    Generate the files
    """
    solr = get_solr_flow_graph(limit=10000, period=3600)

    # generate TSV files
    with open('output/solr.tsv', 'wt') as handler:
        handler.write('# Solr requests\n')
        handler.writelines(format_tsv_lines(solr))

    # generate GraphViz file
    with open('output/solr.gv', 'wt') as handler:
        handler.writelines(format_graphviz_lines(solr))
