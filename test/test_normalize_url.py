from graphs.utils import normalize_mediawiki_url, normalize_pandora_url


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
    assert normalize_mediawiki_url('/api.php?action=query&format=json&meta=siteinfo') == \
        'api:query::siteinfo'
    assert normalize_mediawiki_url('/api.php?action=query&format=json&list=allpages&apnamespace=10&apfilterredir=nonredirects&aplimit=500') == \
        'api:query::allpages'
    assert normalize_mediawiki_url('/api.php?action=query&format=json&titles=Template%3ADocumentation%7CTemplate%3ACC-BY-SA%7CTemplate%3ASelf%7CTemplate%3ACC-BY-SA%2Fdoc%7CTemplate%3AInfobox+event%2Fdoc%7CTemplate%3AOther+free%7CTemplate%3AInfobox+character%7CTemplate%3AInfobox+episode%2Fdoc%7CTemplate%3AInfobox+item%2Fdoc%7CTemplate%3AT%2Fpiece%2Fdoc%7CTemplate%3APermission%2Fdoc%7CTemplate%3AInfobox+episode%7CTemplate%3A%21%21%2Fdoc%7CTemplate%3ANavbox%2Fdoc%7CTemplate%3AFairuse%2Fdoc%7CTemplate%3AQuote%2Fdoc%7CTemplate%3AInfobox+location%7CTemplate%3AInfobox+quest%2Fdoc%7CTemplate%3AInfobox+quest%7CTemplate%3ACc-by-sa-3.0%7CTemplate%3ASelf%2Fdoc%7CTemplate%3ANavbox%7CTemplate%3AOther+free%2Fdoc%7CTemplate%3ADelete%7CTemplate%3APD%7CTemplate%3AFrom+Wikimedia%2Fdoc%7CTemplate%3AInfobox+book%2Fdoc%7CTemplate%3A%21%2Fdoc%7CTemplate%3AT%2Fpiece%7CTemplate%3AT%2Fdoc%7CTemplate%3APermission%7CTemplate%3ADelete%2Fdoc%7CTemplate%3AFrom+Wikimedia%7CTemplate%3AInfobox+book%7CTemplate%3ADocumentation%2Fdoc%7CTemplate%3A%21%7CTemplate%3AInfobox+location%2Fdoc%7CTemplate%3APD%2Fdoc%7CTemplate%3AInfobox+character%2Fdoc%7CTemplate%3AInfobox+event%7CTemplate%3AInfobox+album%2Fdoc%7CTemplate%3AInfobox+album%7CTemplate%3ADisambig%2Fdoc%7CTemplate%3A%21%21%7CTemplate%3AInfobox+item%7CTemplate%3AFairuse%7CTemplate%3AQuote%7CTemplate%3ADisambig%7CTemplate%3ACc-by-sa-3.0%2Fdoc%7CTemplate%3AT') == \
        'api:query'

    # Nirvana API
    assert normalize_mediawiki_url('/wikia.php?controller=MercuryApi&method=getWikiVariables') == \
        'nirvana:MercuryApi::getWikiVariables'
    assert normalize_mediawiki_url('/wikia.php/?method=handle&controller=Email%5CController%5CDiscussionReply') == \
        'nirvana:EmailControllerDiscussionReply::handle'

    # other MediaWiki URLs
    assert normalize_mediawiki_url('/wiki/Special:HealthCheck') == \
        'mediawiki:Special:HealthCheck'

    # language path
    assert normalize_mediawiki_url('/szl/api.php?action=query&format=json&list=users&usids=11536%7C25314808&usprop=groups%7Crights%7Cblockinfo') == \
        'api:query::users'

    assert normalize_mediawiki_url('/is/wiki/Special:HealthCheck') == \
        'mediawiki:Special:HealthCheck'

    assert normalize_mediawiki_url('/pt-br/wikia.php/?method=handle&controller=Email%5CController%5CDiscussionReply') == \
        'nirvana:EmailControllerDiscussionReply::handle'


def test_normalize_pandora_url():
    # service URLs
    assert normalize_pandora_url('/user-attribute/user/3131641') == \
        'pandora:user-attribute::user'
    assert normalize_pandora_url('/helios/info?code=dXuXSqjbQQqndeUPQ8EURA&noblockcheck=1') == \
        'pandora:helios::info'
    assert normalize_pandora_url('/discussion/1233832/threads?limit=10&sortKey=creation_date&sortDirection=descending&viewableOnly=1') == \
        'pandora:discussion::threads'
    assert normalize_pandora_url('/user-preference/25350887') == \
        'pandora:user-preference'
    assert normalize_pandora_url('/cache/c087d8b857cfdc9c7309e35a0c8d4cf7') == \
        'pandora:cache'
    assert normalize_pandora_url('/static-assets/image/31b2956a-f594-4b81-93a4-1ff6791819ac') == \
        'pandora:static-assets::image'
    assert normalize_pandora_url('/discussion/997342/threads?page=0&limit=1&viewableOnly=true') == \
        'pandora:discussion::threads'
    assert normalize_pandora_url('/template-classification-storage/40245/15504') == \
        'pandora:template-classification-storage'
    assert normalize_pandora_url('/api/v1/status') == \
        'pandora:api::v1'
