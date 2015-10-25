"""
Scans pages for lexicon terms, build links.
"""
from makesense.models import Term, TermAlternative, Page
from django.core.management.base import BaseCommand

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
            new_body_list = []
            for body_word in body_list:
                term = None
                try:
                    term = Term.objects.get(term__iexact=body_word)
                except Term.DoesNotExist:
                    if TermAlternative.objects.filter(alternative_term__iexact=body_word).exists():
                        alt = TermAlternative.objects.filter(alternative_term__iexact=body_word)[0]
                        term = alt.term
                
                if term:
                    print 'linking',body_word,'for page',page.title
                    new_body_list.append('<a href="/term/%s/%s/" class="term-link">%s</a>' % (term.word_type_slug,term.term_slug,body_word))
                else:
                    new_body_list.append(body_word)
            
            page.body = ' '.join(new_body_list)
            page.save()
            page.push_to_library()
