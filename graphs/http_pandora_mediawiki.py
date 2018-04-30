"""
This script will generate a data-flow-graph of HTTP communication reaching MediaWiki and Pandora (Kubernetes)
"""
from __future__ import print_function

from data_flow_graph import format_tsv_line, logs_map_and_reduce
from wikia.common.kibana import Kibana

from .utils import normalize_mediawiki_url, normalize_pandora_url


def get_mediawiki_flow_graph(limit, period):
    """
    :type limit int
    :type period int
    :rtype: list[str]
    """
    lines = list()

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


def get_pandora_flow_graph(limit, period):
    """
    :type limit int
    :type period int
    :rtype: list[str]
    """
    lines = list()

    # https://kibana.wikia-inc.com/goto/3aef04fa1f9e55df5cc4c3031671ecab
    # k8s-ingress access logs, internal traffic
    rows = Kibana(period=period, index_prefix='logstash-k8s-ingress-controller').query_by_string(
        query='NOT request_Fastly-Client-Ip: * AND request_User-Agent: * AND RequestHost: "prod.sjc.k8s.wikia.net"',
        limit=limit
    )

    lines.append('# Kubernetes internal requests to Pandora services (from {} entries)'.format(len(rows)))

    # extract required fields only
    # ('mediawiki', 'pandora:helios::info')
    # ('swagger-codegen', 'pandora:user-attribute::user')
    # ('node-fetch', 'pandora:discussion::threads')
    rows = [
        (
            str(row.get('request_User-Agent')).split('/')[0].lower(),
            normalize_pandora_url(row.get('RequestPath')),
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

        # normalize the source
        if source == 'swagger-codegen':
            source = 'mediawiki'
        elif source == 'node-fetch':
            source = 'mobile-wiki'

        return {
            'source': source,
            'edge': 'http',
            'target': target,
            # the following is optional
            'metadata': '{} requests'.format(len(items))
        }

    entries = logs_map_and_reduce(rows, _map, _reduce)
    lines += [format_tsv_line(**entry) for entry in entries]

    return lines


def main():
    print('\n'.join(get_mediawiki_flow_graph(limit=10000, period=3600)))
    print('\n')
    print('\n'.join(get_pandora_flow_graph(limit=10000, period=3600)))
