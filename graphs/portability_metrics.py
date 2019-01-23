"""
This script will generate a data-flow-graph for queries made by Python and Java code
responsible for generating portability metrics.
"""
from __future__ import print_function

from data_flow_graph import format_tsv_lines, format_graphviz_lines, logs_map_and_reduce
from elasticsearch_query import ElasticsearchQuery

from .utils import get_portability_metrics_query

from . import ELASTICSEARCH_HOST


def get_portability_metrics_flow_graph(limit, period):
    """
    :type limit int
    :type period int
    :rtype: list[dict]
    """
    rows = ElasticsearchQuery(
        es_host=ELASTICSEARCH_HOST,
        period=period,
        index_prefix='logstash-other'
    ).query_by_string(
        query='kubernetes.container_name: "portability-metric" AND ("SELECT" OR "UPDATE")',
        fields=[
            'log',
        ],
        limit=limit
    )

    rows = [get_portability_metrics_query(row['log']) for row in rows]
    # print(rows)

    # process the logs
    def _map(item):
        return '{}'.join(item)

    def _reduce(items):
        #  ('MetricArticleProvider.py', 'UPDATE', 'articledata')
        first = items[0]

        script = first[0]
        query_type = first[1]
        table_name = 'db:{}'.format(first[2])

        return {
            'source': table_name if query_type == 'SELECT' else script,
            'edge': query_type,
            'target': table_name if query_type != 'SELECT' else script,
        }

    return logs_map_and_reduce(rows, _map, _reduce)


def main():
    """
    Generate the files
    """
    portability_metrics = get_portability_metrics_flow_graph(limit=1000, period=86400)

    # generate TSV files
    with open('output/portability_metrics.tsv', 'wt') as handler:
        handler.write('# Portability metrics\n')
        handler.writelines(format_tsv_lines(portability_metrics))

    # generate GraphViz file
    with open('output/portability_metrics.gv', 'wt') as handler:
        handler.writelines(format_graphviz_lines(portability_metrics))
