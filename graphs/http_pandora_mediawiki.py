"""
This script will generate a data-flow-graph of HTTP communication reaching MediaWiki and Pandora (Kubernetes)

https://kibana.wikia-inc.com/goto/3aef04fa1f9e55df5cc4c3031671ecab - k8s
"""
from __future__ import print_function

from data_flow_graph import format_tsv_line, logs_map_and_reduce
from wikia.common.kibana import Kibana

from .utils import normalize_mediawiki_url, normalize_pandora_url


def get_flow_graph(limit, period):
    """
    :type limit int
    :type period int
    :rtype: list[str]
    """
    lines = list()

    # first get MediaWiki logs
    # https://kibana5.wikia-inc.com/goto/e6ab16f694b625d5b87833ae794f5989
    # goreplay is running in RES (check SJC logs only)
    rows = Kibana(period=period, index_prefix='logstash-mediawiki').query_by_string(
        query='"Wikia internal request" AND @fields.environment: "prod" AND @fields.datacenter: "sjc" '
              'AND @fields.http_url_path: *',
        limit=limit
    )

    lines.append('# Internal requests to MediaWiki (from {} entries)'.format(len(rows)))

    # extract required fields only
    # (u'user-permissions', 'api:query::users')
    # (u'1', 'nirvana:EmailControllerDiscussionReply::handle')
    rows = [
        (
            row.get('@context').get('source'),
            normalize_mediawiki_url(row.get('@fields').get('http_url_path'))
        )
        for row in rows
    ]

    # process the logs
    def _map(item):
        return '{}-{}'.format(item[0], item[1])

    def _reduce(items):
        first = items[0]
        source = first[0]
        target = first[1]

        return {
            'source': source if source != '1' else 'internal',
            'edge': 'http',
            'target': target,
            # the following is optional
            'metadata': '{} requests'.format(len(items))
        }

    entries = logs_map_and_reduce(rows, _map, _reduce)
    lines += [format_tsv_line(**entry) for entry in entries]

    return lines


def main():
    print('\n'.join(get_flow_graph(limit=5000, period=3600)))
