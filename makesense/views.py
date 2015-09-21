""" 
Views for maksense.
"""
from makesense.utils import template
from makesense.models import Chapter, Page, Term
from django.shortcuts import get_object_or_404

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
def page(request,page_num,slug):
    """ 
    The 'page' page.
    """
    ordering = int(page_num) - 1
    page_model = get_object_or_404(Page,ordering=ordering,slug=slug)
    return {'page':page_model}

@template('makesense/term.html')
def term(request,word_type_slug,term_slug):
    """ 
    A term.
    """
    term_model = get_object_or_404(Term,term_slug=term_slug,word_type_slug=word_type_slug)
    return {'term':term_model}

@template('makesense/search.html')
def search(request):
    """
    Searches the site.;
    """
    query = request.GET.get('q',None)
    results = Page.objects.search(query)
    return {'results':results,'query':query}

@template('makesense/resources.html')
def resources(request):
    """
    IA Resources.
    """
    return {}