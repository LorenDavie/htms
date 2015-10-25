""" 
Utility template tags for makesense.
"""
from django import template

register = template.Library()

def active_term(value,term):
    """ 
    Modifies links so only the active term is added to the active-term class.
    """
    new_term_words = []
    match_string = 'href="/term/%s/%s/">%s</a>' % (term.word_type_slug,term.term_slug,term.term_slug)
    replace_string = 'href="/term/%s/%s/" class="active-term">%s</a>' % (term.word_type_slug,term.term_slug,term.term_slug)
    alt_match_prefix = 'href="/term/%s/%s/">' % (term.word_type_slug,term.term_slug)
    
    alt_matches = []
    alt_replace_dict = {}
    for alt in term.alternatives.all():
        alt_match = '%s%s</a>' % (alt_match_prefix,alt.alternative_term)
        alt_matches.append(alt_match)
        alt_matches.append(alt_match.lower())
        alt_replace = 'href="/term/%s/%s/" class="active-term">%s</a>' % (term.word_type_slug,term.term_slug,alt.alternative_term)
        alt_replace_dict[alt_match] = alt_replace
        alt_replace_dict[alt_match.lower()] = alt_replace.lower()

    for word in value.split(' '):
        if word.lower() == match_string:
            new_term_words.append(replace_string)
        elif word.lower() in alt_matches:
            new_term_words.append(alt_replace_dict[word.lower()])
        else:
            new_term_words.append(word)
    
    return u' '.join(new_term_words)


register.filter('active_term',active_term)