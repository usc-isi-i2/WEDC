import snowballstemmer
import inflection
import enchant

enchant_dict = enchant.Dict("en_US")
stemmer = snowballstemmer.stemmer('english');


def stemming(word):
    tmp = valid_stemming(inflection.singularize(word))
    if tmp: return tmp
    print 'enter stem'
    tmp = valid_stemming(stemmer.stemWord(word))
    if tmp: return tmp
    return word

def valid_stemming(word):
    if len(word) > 1 and enchant_dict.check(word):
        return word
    return None

print stemming('changed')