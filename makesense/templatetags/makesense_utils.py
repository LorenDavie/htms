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
    match_string = 'href="/term/%s/%s/" class="term-link">%s</a>' % (term.word_type_slug,term.term_slug,term.term_slug)
    match_2_string = 'href="/term/%s/%s/">%s</a>' % (term.word_type_slug,term.term_slug,term.term_slug)
    match_3_string = 'href="/term/%s/%s/"' % (term.word_type_slug,term.term_slug)
    replace_string = 'href="/term/%s/%s/" class="term-link active-term">%s</a>' % (term.word_type_slug,term.term_slug,term.term_slug)
    alt_match_prefix = 'href="/term/%s/%s/" class="term-link">' % (term.word_type_slug,term.term_slug)
    alt_match_2_prefix = 'href="/term/%s/%s/">' % (term.word_type_slug,term.term_slug)
    alt_match_3 = 'href="/term/%s/%s/"' % (term.word_type_slug,term.term_slug)
    
    match_3_replace = 'href="/term/%s/%s/" class="active-term term-link"' % (term.word_type_slug,term.term_slug)
    
    print 'match string:',match_string
    print 'match 2 string:',match_2_string
    print 'match 3 string',match_3_string
    
    alt_matches = []
    alt_replace_dict = {}
    for alt in term.alternatives.all():
        alt_match = '%s%s</a>' % (alt_match_prefix,alt.alternative_term)
        alt_match_2 = '%s%s</a>' % (alt_match_2_prefix,alt.alternative_term)
        alt_matches.append(alt_match)
        alt_matches.append(alt_match.lower())
        alt_matches.append(alt_match_2)
        alt_matches.append(alt_match_2.lower())
        alt_replace = 'href="/term/%s/%s/" class="active-term term-link">%s</a>' % (term.word_type_slug,term.term_slug,alt.alternative_term)
        alt_replace_dict[alt_match] = alt_replace
        alt_replace_dict[alt_match.lower()] = alt_replace.lower()
        alt_replace_dict[alt_match_2.lower()] = alt_replace.lower()
    
    alt_matches.append(alt_match_3)
    alt_replace_dict[alt_match_3] = match_3_replace
    alt_replace_dict[alt_match_3.lower()] = match_3_replace
    print 'alt match strings:',alt_matches
    
    for word in value.split(' '):
        if word.lower() == match_string or word.lower() == match_2_string or word.lower() == match_3_string:
            print 'word',word,'matches string',match_string,'or',match_2_string
            if word.lower() == match_3_string:
                new_term_words.append(match_3_replace)
            else:
                new_term_words.append(replace_string)
        elif word.lower() in alt_matches:
            print 'word',word,'in alt matches',alt_matches
            new_term_words.append(alt_replace_dict[word.lower()])
        else:
            print 'no match for word',word
            new_term_words.append(word)
    
    return u' '.join(new_term_words)


register.filter('active_term',active_term)