# -*- coding: utf-8 -*-
from graphs.utils import get_portability_metrics_query


def test_get_portability_metrics_query():
    assert get_portability_metrics_query('2019-01-23 08:40:06 MetricArticleProvider     INFO     SELECT /* portability-metric MetricArticleProvider.py */ sum(processed), count(*) FROM articledata') == \
           ('MetricArticleProvider.py', 'SELECT', 'articledata')

    assert get_portability_metrics_query('2019-01-23 05:20:11 MetricArticleProvider     INFO     UPDATE /* portability-metric MetricArticleProvider.py */ articledata SET processed = 1 WHERE namespace_id = 0 AND processed = 0 ORDER BY pageviews desc LIMIT 10000') == \
           ('MetricArticleProvider.py', 'UPDATE', 'articledata')

    assert get_portability_metrics_query('2019-01-23 00:00:20 PortabilityData           INFO     SQL: SELECT date_id,navboxes_metric FROM `metricseries` ORDER BY date_id desc LIMIT 0, 52') == \
           ('PortabilityData', 'SELECT', 'metricseries')

    assert get_portability_metrics_query('2019-01-22 11:30:12 root                      INFO     SELECT /* portability-metric calculation.py */ sum(pageviews) AS pageviews FROM articlestats s INNER JOIN articledata d WHERE d.wiki_id = s.wiki_id AND d.page_id = s.page_id AND (portable_b = 1 OR curatedcontent_b = 1)') == \
           ('calculation.py', 'SELECT', 'articlestats')

    assert get_portability_metrics_query('2019-01-22 11:30:45 root                      INFO     SELECT /* portability-metric calculation.py */ count(*) AS sample, sum(pageviews) AS pageviews, SUM(portableinfoboxfilter_b * pageviews) AS infoboxes, SUM(curatedcontent_b * pageviews) AS curatedcontent, SUM(portableflagsfilter_b * pageviews) AS flags, SUM(customquotefilter_b * pageviews) AS quotes, SUM(navboxfilter_b * pageviews) AS navboxes, SUM(curatedcontent_b) AS curatedcontent_count FROM articlestats s INNER JOIN articledata d WHERE d.wiki_id = s.wiki_id AND d.page_id = s.page_id') == \
           ('calculation.py', 'SELECT', 'articlestats')

    assert get_portability_metrics_query('2019-01-22 11:30:45 foo') is None
