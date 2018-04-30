"""
A set of helper functions
"""
try:
    # Py3
    from urllib import parse as urlparse, parse_qs
except ImportError:
    # Py2.7
    from urlparse import urlparse, parse_qs


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
            type=query_params.get('list', query_params.get('prop', ['n/a']))[0]
        )
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
