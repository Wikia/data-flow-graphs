# -*- coding: utf-8 -*-
from graphs.utils import get_solr_core_name, get_solr_parameters


def test_get_solr_core_name():
    # write
    assert get_solr_core_name('136874497 [qtp1518864111-53636] INFO  org.apache.solr.update.processor.LogUpdateProcessor  – [xwiki] webapp=/solr path=/update params={commit=true} {add=[663 (1603805561233604608)],commit=} 0 30') == \
        'xwiki'

    # read
    assert get_solr_core_name('136809715 [qtp1518864111-2582] INFO  org.apache.solr.core.SolrCore  – [main] webapp=/solr path=/select params={q=(id:175043_4003)&fl=score,id,pageid,wikiarticles,wikititle_en,url,wid,canonical,host,ns,indexed,backlinks,title_en,created,views,categories_mv_en,hub,lang,html_en,article_quality_i,recommendations_ss,snippet_s,article_type_s&start=0&timeAllowed=5000&sort=score+desc&rows=1&wt=json} hits=1 status=0 QTime=1') == \
        'main'

    # long, trimmed log line
    assert get_solr_core_name('654324409 [qtp1837760739-8822] INFO  org.apache.solr.core.SolrCore  – [main] webapp=/solr path=/select params={mm=80%25&ps=3&fl=score,id,pageid,wikiarticles,wikititle_en,url,wid,canonical,host,ns,indexed,backlinks,title_en,created,views,categories_mv_en,hub,lang,article_quality_i,article_type_s&start=0&sort=score+desc&rows=8&bq=&q=%2B((%2B(wid:43339)+AND+(ns:6)+AND+(is_video:true)))+AND+%2B(Fausti+Fei+Leit+Gin+Zu+Fouss)&tie=0.01&defType=edismax&qf=title_en^100+html_en^5+redirect_titles_mv_en^50+categories_mv_en^25+nolang_txt^10+backlinks_txt^25+title_en^100+html_en^5+redirect_titles_mv_en^50+video_actors_txt^100+video_genres_txt^50+html_media_extras_txt^20+video_description_txt^100+video_keywords_txt^60+video_tags_txt^40&pf=title_en^100+html_en^5+redirect_titles_mv_en^50+categories_mv_en^25+nolang_txt^10+backlinks_txt^25+title_en^100+html_en^5+redirect_titles_mv_en^50+video_actors_txt^100+video_genres_txt^50+html_media_extras_txt^20+video_description_txt^100+video_keywords_txt^60+video_tags_txt^40&timeAllo') == \
        'main'

    assert get_solr_core_name('foo') is None


def test_get_solr_parameters():
    params = get_solr_parameters('136874497 [qtp1518864111-53636] INFO  org.apache.solr.update.processor.LogUpdateProcessor  – [xwiki] webapp=/solr path=/update params={commit=true} {add=[663 (1603805561233604608)],commit=} 0 30')

    assert params['webapp'] == '/solr'
    assert params['path'] == '/update'
    assert params['params'] == '{commit=true}'

    params = get_solr_parameters('136809715 [qtp1518864111-2582] INFO  org.apache.solr.core.SolrCore  – [main] webapp=/solr path=/select params={q=(id:175043_4003)&fl=score,id,pageid,wikiarticles,wikititle_en,url,wid,canonical,host,ns,indexed,backlinks,title_en,created,views,categories_mv_en,hub,lang,html_en,article_quality_i,recommendations_ss,snippet_s,article_type_s&start=0&timeAllowed=5000&sort=score+desc&rows=1&wt=json} hits=1 status=0 QTime=1 ')

    assert params['webapp'] == '/solr'
    assert params['path'] == '/select'
    assert params['QTime'] == '1'
