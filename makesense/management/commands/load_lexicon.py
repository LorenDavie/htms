"""
Loads the lexicon terms into ACE.
"""
from makesense.models import Term, TermAlternative
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
                if not role.endswith('.'):
                    role = role + '.'
                word_type = word_type_map[role]
                term, term_created = Term.objects.get_or_create(term=term_name,
                                                                term_slug=slugify(term_name),
                                                                word_type=word_type,
                                                                word_type_slug=slugify(word_type),
                                                                description=definition)
                print 'created term',term.term
                if term_created:
                    for alt in alts.split(','):
                        if alt:
                            alt_term, alt_term_type_str = alt.rsplit(' ',1)
                            alt_term_type_str = alt_term_type_str[1:-1] # trip parens
                            if not alt_term_type_str.endswith('.'):
                                alt_term_type_str = alt_term_type_str + '.'
                            print 'alt term',alt_term
                            print 'alt term word type',word_type_map[alt_term_type_str]
                            TermAlternative.objects.create(term=term,
                                                           alternative_term=alt_term,
                                                           word_type=word_type_map[alt_term_type_str])
                    
                    term.push_to_library() # send to ACE
                
                print '\t'.join(row)
