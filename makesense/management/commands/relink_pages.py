""" 
Rebuilds page term usage and totals.
"""
from makesense.models import Term, TermAlternative, Page
from django.core.management.base import BaseCommand
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
            # Clearing usage
            print 'Rebuilding usage for',term.term
            term.total_usage = 0
            term.usage.clear()
            term.save()
            
            # Rebuild usage
            term_path = '/term/%s/%s/' % (term.word_type_slug,term.term_slug)
            
            for page in Page.objects.all():
                matches = re.findall(term_path,page.body,re.IGNORECASE|re.MULTILINE)
                if matches:
                    term.usage.add(page)
                    term.total_usage += len(matches)
            
            term.save()
            print term.term,'is used',term.total_usage,'across',term.usage.count(),'pages.'
            
            