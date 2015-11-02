"""
Links 2-word terms into ACE
"""
from makesense.models import Term, Page
from django.core.management.base import BaseCommand
from django.utils.text import slugify
import re

class Command(BaseCommand):
    """
    Command class.
    """
    def execute(self,*args,**kwargs):
        """
        Execute method.
        """
        for term in Term.objects.all():
            if term.term and len(term.term.split()) > 1:
                print 'linking multi word term',term.term
                termlist = term.term.split()
                term_pattern = r'\s'.join(termlist)
                split_pattern = '(%s)' % term_pattern
                print 'matching pattern:',term_pattern
                for page in Page.objects.all():
                    matches = re.findall(term_pattern,page.body,re.IGNORECASE)
                    if matches:
                        num_matches = len(matches)
                        term.total_usage += num_matches
                        term.usage.add(page)
                        body_list = re.split(split_pattern,page.body,flags=re.IGNORECASE)
                        new_body = ''
                        for token in body_list:
                            if term.term.lower() == token.lower():
                                replace_term = '<a href="/term/%s/%s/" class="term-link">%s</a>' % (term.word_type_slug,term.term_slug,token)
                                new_body += replace_term
                            else:
                                new_body += token
                        
                        page.body = new_body
                        page.save()
                        page.push_to_library()
                
                term.save()
                
