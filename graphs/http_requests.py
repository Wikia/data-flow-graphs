"""
Generate data-flow graph with HTTP requests sent by MediaWiki

https://github.com/Wikia/app/blob/d10c323c028406321dabe568132726cb4af7504b/includes/HttpFunctions.php#L83-L112

https://macbre.github.io/data-flow-graph/gist.html#3ac2c20a4e059ab263c4c92507d18e26
"""
from wikia.common.kibana import Kibana
from .utils import format_tsv_entry

PERIOD = 3600


def main():
    # outbound traffic
    stats = Kibana(period=PERIOD, index_prefix='logstash-mediawiki').get_aggregations(
        query='"Http request" AND severity: "debug" AND @fields.datacenter: "SJC" and @field.environment: "prod"',
        group_by='@context.caller.keyword',
        stats_field='@context.requestTimeMS'
    )
    max_count = max([item['count'] for item in stats.values()])
    sum_count = sum([item['count'] for item in stats.values()])

    print '# HTTP requests sent by MediaWiki grouped by caller ({} requests analyzed)'.format(sum_count)

    for caller, metrics in stats.iteritems():
        # Wikia\\Search\\Services\\ESFandomSearchService:select
        # template-classification-storage
        caller = caller.replace('{closure}', '').strip('\\')
        caller = caller.split('\\')[-1]

        qps = 1. * metrics['count'] / PERIOD

        # this request is not frequent enough
        if qps < 0.1:
            continue

        metadata = '{:.2f} qps, resp. times: p50 = {:.2f} ms / p95 = {:.2f} ms / p99 = {:.2f} ms'.format(
            qps,
            metrics['50.0'],
            metrics['95.0'],
            metrics['99.0'],
        )

        weight = 1. * metrics['count'] / max_count

        print format_tsv_entry(source='mediawiki-app', edge=caller, dest=caller, weight=weight, metadata=metadata)

    # inbound traffic
    stats = Kibana(period=PERIOD, index_prefix='logstash-mediawiki').get_aggregations(
        query='"Wikia internal request" AND @fields.datacenter: "SJC" and @field.environment: "prod"',
        group_by='@context.source.keyword',
        stats_field=''  # we're not interested in percentile data, we just want the bucket size
    )
    max_count = max([item['count'] for item in stats.values()])
    sum_count = sum([item['count'] for item in stats.values()])

    print '# Internal HTTP requests received by MediaWiki grouped by caller ({} requests analyzed)'.format(sum_count)

    for source, metrics in stats.iteritems():
        qps = 1. * metrics['count'] / PERIOD

        # this request is not frequent enough
        if qps < 0.1 or source == '1':
            continue

        metadata = '{:.2f} qps'.format(
            qps,
        )

        weight = 1. * metrics['count'] / max_count

        print format_tsv_entry(source=source, edge=source, dest='mediawiki-app', weight=weight, metadata=metadata)


if __name__ == '__main__':
    main()
