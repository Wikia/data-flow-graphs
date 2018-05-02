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


def normalize_mediawiki_url(url):
    """
    :type url str
    :rtype: str
    :raise: ValueError
    """
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    if url.startswith('/api.php'):
        return 'api:{action}::{type}'.format(
            action=query_params['action'][0],
            type=query_params.get('list', query_params.get('meta', query_params.get('prop', [''])))[0]
        ).rstrip(':')
    elif url.startswith('/wikia.php'):
        return 'nirvana:{controller}::{method}'.format(
            controller=str(query_params['controller'][0]).replace('\\', ''),
            method=query_params['method'][0]
        )
    elif url.startswith('/wiki/'):
        return 'mediawiki:{page}'.format(
            page=str(parsed.path).replace('/wiki/', '')
        )

    # print(url, parsed, query_params)
    raise ValueError('Provided URL has not been matched')


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
