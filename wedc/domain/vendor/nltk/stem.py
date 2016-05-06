"""
Credits:
NodeBox::Linguistics: https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation

"""


from nltk import stem
# import Stemmer
from nltk.stem.wordnet import WordNetLemmatizer
import re
import inflection
# from wedc.domain.vendor import en

def stemming(word):
    # porter = stem.porter.PorterStemmer()
    # lancaster = stem.lancaster.LancasterStemmer()
    # snowball = stem.snowball.EnglishStemmer()
    # return snowball.stem(word)
    
    be_words = ['am', 'is', 'are', 'was', 'were', 'been']
    if word in be_words:
        return 'be'
    if re.search(r'\d+[k$]+[/(hr|hour)]*', word):
        return '401k'


    # return snowball.stem(word)

    # stemmer = Stemmer.Stemmer('english')
    # return stemmer.stemWord(word)
    
    
    lmtzr = WordNetLemmatizer()
    word = lmtzr.lemmatize(word, 'v') 
    
    word = inflection.singularize(word)
    # word = stem.snowball.SnowballStemmer("english", ignore_stopwords=False).stem(word)


    return word



    
