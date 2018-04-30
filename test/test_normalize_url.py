from graphs.utils import normalize_mediawiki_url


def test_normalize_mediawiki_url():
    # MediaWiki's api.php
    assert normalize_mediawiki_url('/api.php?action=query&format=json&list=users&usids=26653902%7C25608263&usprop=groups%7Crights%7Cblockinfo') == \
        'api:query::users'
    assert normalize_mediawiki_url('/api.php?action=query&format=json&list=users&usids=31473370%7C30990543%7C29953564%7C35015642%7C33406774%7C31015099%7C30134270%7C32218688%7C29994120&usprop=groups%7Crights%7Cblockinfo') == \
        'api:query::users'

    assert normalize_mediawiki_url('/api.php?action=parse&format=json&pageid=4450&prop=text') == \
        'api:parse::text'
    assert normalize_mediawiki_url('/api.php?action=query&format=json&list=wkdomains&wkwikia=79848') == \
        'api:query::wkdomains'
    assert normalize_mediawiki_url('/api.php?action=query&format=json&prop=imageinfo&revids=36290&iiprop=userid%7Csize%7Cdimensions') == \
        'api:query::imageinfo'

    # Nirvana API
    assert normalize_mediawiki_url('/wikia.php?controller=MercuryApi&method=getWikiVariables') == \
        'nirvana:MercuryApi::getWikiVariables'
    assert normalize_mediawiki_url('/wikia.php/?method=handle&controller=Email%5CController%5CDiscussionReply') == \
        'nirvana:EmailControllerDiscussionReply::handle'

    # other MediaWiki URLs
    assert normalize_mediawiki_url('/wiki/Special:HealthCheck') == \
        'mediawiki:Special:HealthCheck'
