"""
Credits:
NodeBox::Linguistics: https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation

"""


from nltk import stem
from nltk.stem.wordnet import WordNetLemmatizer
from pattern.en import singularize
import re
import inflection
import enchant

enchant_dict = enchant.Dict("en_US")
snowball = stem.snowball.EnglishStemmer()

def stemming(word):

    be_words = ['am', 'is', 'are', 'was', 'were', 'been']

    if word in be_words:
        return 'be'

    if re.search(r'\d+[k$]+[/(hr|hour)]*', word):
        return '401k'

    lmtzr = WordNetLemmatizer()
    word = lmtzr.lemmatize(word, 'v') 

    # tmp = singularize(word)

    tmp = valid_stemming(snowball.stem(word))
    if tmp: return tmp
    tmp = valid_stemming(inflection.singularize(word))
    if tmp: return tmp
    
    return word
    
def valid_stemming(word):
    if len(word) > 1 and enchant_dict.check(word):
        return word
    return None


    # porter = stem.porter.PorterStemmer()
    # lancaster = stem.lancaster.LancasterStemmer()
    # 
    # return snowball.stem(word)
    
    


    # return snowball.stem(word)

    # stemmer = Stemmer.Stemmer('english')
    # return stemmer.stemWord(word)
    
    
    
    # word = stem.snowball.SnowballStemmer("english", ignore_stopwords=False).stem(word)


    



    
