""" 
Links usage of a specific term.
"""
from makesense.models import Term, Page
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ 
    Command class.
    """
    def add_arguments(self,parser):
        parser.add_argument('term')
    
    def execute(self,*args,**kwargs):
        """ 
        Execute method.
        """
        term_name = kwargs['term']
        try:
            term = Term.objects.get(term=term_name)
            for page in Page.objects.all():
                if (term.term in page.body) or (term.term.lower() in page.body):
                    term.usage.add(page)
                    term.total_usage += 1
                
                for alt in term.alternatives.all():
                    if (alt.alternative_term in page.body) or (alt.alternative_term.lower() in page.body):
                        term.usage.add(page)
                        term.total_usage += 1
            
            term.save()
        except Term.DoesNotExist:
            print 'No such term',term_name
