""" 
Views for maksense.
"""
from makesense.utils import template
from makesense.models import Chapter, Page, Term, TermAlternative, Book
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_control

book_title = 'How To Make Sense of Any Mess'

@template('makesense/home.html')
def home(request):
    """ 
    Home page.
    """
    chapters = Chapter.objects.all()
    return {'chapters':chapters}

@template('makesense/lexicon.html')
def lexicon(request):
    """
    Lexicon.
    """
    return {'groups':Term.objects.get_alpha_groups()}

@template('makesense/chapter.html')
def chapter(request,chapter_num,slug):
    """ 
    Chapter page.
    """
    chapter_model = get_object_or_404(Chapter,book__title=book_title,order=chapter_num)
    return {'chapter':chapter_model}

@template('makesense/page.html')
def page(request,chapter_num,page_num,slug):
    """ 
    The 'page' page.
    """
    chapter_model = get_object_or_404(Chapter,book__title=book_title,order=chapter_num)
    page_model = chapter_model.pages.get(slug=slug)
    return {'page':page_model}

def page_redirect(request,page_num,slug):
    """
    Redirects to canonical page URL.
    """
    ordering = int(page_num) - 1
    page_model = get_object_or_404(Page,ordering=ordering,slug=slug)
    return HttpResponseRedirect('/chapter/%d/page/%d/%s/' % (page_model.chapter.order,page_model.ordering,page_model.slug))

@template('makesense/term.html')
def term(request,word_type_slug,term_slug):
    """ 
    A term.
    """
    term_model = get_object_or_404(Term,term_slug=term_slug,word_type_slug=word_type_slug)
    return {'term':term_model}

@cache_control(private=True) # don't cache search results
@template('makesense/search.html')
def search(request):
    """
    Searches the site.;
    """
    query = request.GET.get('q',None)
    if not query:
        return {'results':None,'query':None}
    
    # if the search query matches a term, redirect to the term page
    term = None
    try:
        term = Term.objects.get(term__iexact=query)
    except Term.DoesNotExist:
        try:
            term_alt = TermAlternative.objects.get(alternative_term__iexact=query)
            term = term_alt.term
        except TermAlternative.DoesNotExist:
            pass
    
    if term:
        return HttpResponseRedirect('/term/%s/%s/' % (term.word_type_slug,term.term_slug))
        
        
    results = Page.objects.search(query)
    return {'results':results,'query':query}

@template('makesense/dedication.html')
def dedication(request):
    """ 
    Book dedication.
    """
    book = Book.objects.get(title=book_title)
    return {'book':book}

@template('makesense/introduction.html')
def introduction(request):
    """ 
    Book introduction.
    """
    book = Book.objects.get(title=book_title)
    return {'book':book}

@template('makesense/about.html')
def about(request):
    """ 
    About the book.
    """
    book = Book.objects.get(title=book_title)
    return {'book':book}

@template('makesense/acknowledgements.html')
def acknowledgements(request):
    """ 
    Acknowledgements.
    """
    book = Book.objects.get(title=book_title)
    return {'book':book}

@template('makesense/resources.html')
def resources(request):
    """
    IA Resources.
    """
    book = Book.objects.get(title=book_title)
    return {'book':book}
