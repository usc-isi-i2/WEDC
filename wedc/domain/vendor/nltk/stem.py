
from nltk import stem
# import Stemmer
import re

def stemming(word):
    # porter = stem.porter.PorterStemmer()
    # lancaster = stem.lancaster.LancasterStemmer()
    # snowball = stem.snowball.EnglishStemmer()
    # return snowball.stem(word)
    
    be_words = ['am', 'is', 'are', 'was', 'were', 'been']
    if word in be_words:
        return 'be'
    if re.search(r'\d+[k$]+[/(hr|hour)]*', word):
        return '#/h'

    # stemmer = Stemmer.Stemmer('english')
    # return stemmer.stemWord(word)
    return stem.snowball.SnowballStemmer("english", ignore_stopwords=False).stem(word)
