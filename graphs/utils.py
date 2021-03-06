"""
A set of helper functions
"""
try:
    # Py3
    from urllib.parse import urlparse, parse_qs
except ImportError:
    # Py2.7
    from urlparse import urlparse, parse_qs

import re
from collections import OrderedDict

from sql_metadata import get_query_tables


def normalize_mediawiki_url(url):
    """
    :type url str
    :rtype: str
    :raise: ValueError
    """
    # remove language path
    if not url.startswith('/wiki/'):
        url = re.sub(r'^/[a-z\-]{2,14}/', '/', url)

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    try:
        if url.startswith('/api.php'):
            return 'api:{action}::{type}'.format(
                action=query_params['action'][0],
                type=query_params.get('list',
                                      query_params.get('meta', query_params.get('prop', [''])))[0]
            ).rstrip(':')
        if url.startswith('/wikia.php'):
            return 'nirvana:{controller}::{method}'.format(
                controller=str(query_params['controller'][0]).replace('\\', ''),
                method=query_params.get('method', ['index'])[0]
            )
        if url.startswith('/wiki/'):
            return 'mediawiki:{page}'.format(
                page=str(parsed.path).replace('/wiki/', '')
            )
        if url.startswith('/v1/'):
            return 'api:{controller}'.format(
                controller=url.split('/')[2]
            )
    except KeyError:
        raise ValueError('Provided URL <%s> is not a valid one' % url)

    # print(url, parsed, query_params)
    raise ValueError('Provided URL <%s> has not been matched' % url)


def normalize_pandora_url(url):
    """
    :type url str
    :rtype: str
    :raise: ValueError
    """
    # user-attribute/user/3131641
    # discussion/1233832/threads
    path = str(urlparse(url).path).lstrip('/')
    path = re.sub(r'/\d+(/|$)', '/', path)

    try:
        (service, method) = path.split('/')[:2]
    except ValueError:
        service = path.split('/').pop()
        method = ''

    # /cache/c087d8b857cfdc9c7309e35a0c8d4cf7
    # /template-classification-storage/40245/15504
    if service in ['cache', 'template-classification-storage']:
        method = ''

    # print(url, path, service, method)
    return 'pandora:{}::{}'.format(service, method).rstrip(':')


def is_mobile_app_user_agent(user_agent):
    """
    :type user_agent str
    :rtype: bool
    """
    # starwars/2.9.6 (Android: 24)
    if 'Android' in user_agent and re.match(r'[\w\s\d]+/[\d.]+ \(Android: \d+\)', user_agent):
        return True

    # FandomEnterpriseApp/1.5.5 (iPhone; iOS 11.2; Scale/2.00)
    if user_agent.startswith('FandomEnterpriseApp/'):
        return True

    # foobar/2.9 (iPhone; iOS 11.4; Scale/2.00)'
    if 'iPhone' in user_agent and re.match(r'[\w\s\d]+/[\d.]+ \(iPhone; iOS \d+', user_agent):
        return True

    return False


def get_solr_core_name(logline):
    """
    :type logline str
    :rtype: str|None
    """
    matches = re.search(r'\[([^\]]+)\] webapp', logline)
    return matches.group(1) if matches else None


def get_solr_parameters(logline):
    """
    :type logline str
    :rtype: OrderedDict
    """
    params = OrderedDict()
    matches = re.findall(r'\s(\w+)=([^\s]+)', logline)

    for match in matches:
        params[match[0]] = match[1]

    return params


def get_portability_metrics_query(logline, job_name):
    """
    :type logline str
    :type job_name str
    :rtype: list[str, str, str]
    """
    # extract SQL query
    try:
        sql = str(re.search(r'INFO (.*)$', logline).group(1).strip())
    except AttributeError:
        return

    # remove "SQL: " prefix
    sql = sql.replace('SQL:', '').lstrip()

    # script name
    # portability-metric-metric-article-provider-py-1548232800
    script_name = str(re.match(r'portability-metric-([a-z-]+)-\d+', job_name).group(1))
    script_name = script_name.replace('-py', '.py')

    # SELECT, UPDATE, ...
    query_type = sql.split(' ')[0].upper()

    # get query metadata
    for table in get_query_tables(sql):
        # ignore one letter table aliases
        if len(table) == 1:
            continue

        yield script_name, query_type, table
