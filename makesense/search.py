""" 
Self-hosted search.
"""
from pyelasticsearch import ElasticSearch
from makesense.models import Page
from django.conf import settings

es = ElasticSearch(settings.ELASTICSEARCH_URL)

def index_page(page):
    """ 
    Indexes the page.
    """
    es.index('pages','page',{
        'content':page.body,
        'pk':page.pk,
    },id=page.pk)
    
def index_all_pages():
    """ 
    Indexes all the pages.
    """
    for page in Page.objects.all():
        index_page(page)

def search_pages(query):
    """ 
    Searches for pages.
    """
    result = es.search(query,index='pages')
    hits = result['hits']['hits']
    pks = [hit['_source']['pk'] for hit in hits]
    return Page.objects.filter(pk__in=pks)
