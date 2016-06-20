"""
Credits:
NodeBox::Linguistics: https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation
https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation
"""

import en
be_words = ['am', 'is', 'are', 'was', 'were', 'been']

def stemming(word):

    if word in be_words:
        return 'be'

    try:
        if en.is_noun(word):
            word = en.noun.singular(word)
        elif en.is_adjective(word) or en.is_adverb(word):
            return word
        else:
            word = en.verb.present(word)
    except Exception:
        pass
        
    return en.spelling.correct(word)





