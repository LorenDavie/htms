"""
Scans pages for lexicon terms, updates usage..
"""
from makesense.models import Term, TermAlternative, Page
from django.core.management.base import BaseCommand
from django.utils.text import slugify

class Command(BaseCommand):
    """
    Command class.
    """
    def execute(self,*args,**kwargs):
        """
        Execute method.
        """
        for page in Page.objects.all():
            print 'Linking page',page.title
            body_list = page.body.split(' ')
            for body_word in body_list:
                term = None
                if "/term/" in body_word:
                    prefix, href, postfix = body_word.split('\"')
                    print 'unpacking href:',href
                    term_literal, word_type, term_name = href.strip('/').split('/')
                    try:
                        term = Term.objects.get(term__iexact=term_name)
                    except Term.DoesNotExist:
                        pass
                
                if term:
                    print 'updating usage of',term,'by page',page.title
                    term.usage.add(page)
                    term.total_usage += 1
                    term.save()
            
