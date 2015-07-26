""" 
Views for maksense.
"""
from makesense.utils import template
from makesense.models import Chapter, Page, Term
from django.shortcuts import get_object_or_404

book_title = 'How To Make Sense Of Any Mess'

@template('makesense/home.html')
def home(request):
    """ 
    Home page.
    """
    return {}

@template('makesense/chapter.html')
def chapter(request,chapter_num,slug):
    """ 
    Chapter page.
    """
    chapter_model = get_object_or_404(Chapter,book__title=book_title,order=chapter_num)
    return {'chapter':chapter_model}

@template('makesense/page.html')
def page(request,page_id,slug):
    """ 
    The 'page' page.
    """
    page_model = get_object_or_404(Page,pk=page_id)
    return {'page':page_model}

@template('makesense/term.html')
def term(request,word_type_slug,term_slug):
    """ 
    A term.
    """
    term_model = get_object_or_404(Term,term_slug=term_slug,word_type_slug=word_type_slug)
    return {'term':term_model}
