"""
Loads the lexicon terms into ACE.
"""
from makesense.models import Term
from django.core.management.base import BaseCommand
import csv
from django.utils.text import slugify

word_type_map = {
    'n.':'Noun',
    'v.':'Verb',
    'adj.':'Adjective',
    'adv.':'Adverb',
    'pro.':'Pronoun',
}

class Command(BaseCommand):
    """
    Command class.
    """
    def add_arguments(self,parser):
        parser.add_argument('filename')
    
    def execute(self,*args,**kwargs):
        """
        Execute method.
        """
        filename = kwargs['filename']
        with open(filename,'rb') as csvfile:
            termreader = csv.reader(csvfile)
            for row in termreader:
                term_name, role, definition, alts, related = row
                # print 'term:',term_name
                # print 'related:',related
                # print '--------------------'
                try:
                    root_term = Term.objects.get(term=term_name)
                    print 'looking for related terms for root term:',root_term
                    for related_term_raw in related.split(','):
                        related_term_name = related_term_raw.strip()
                        try:
                            related_term = Term.objects.get(term=related_term_name)
                            root_term.related.add(related_term)
                            print 'relating term',related_term,'to root',root_term
                        except Term.DoesNotExist:
                            print 'cannot find term:',related_term_name
                    
                    root_term.save()
                except Term.DoesNotExist:
                    print 'cannot find root term:',term_name
                
                print '--------------------'

