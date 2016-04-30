
from nltk import stem
# import Stemmer
from nltk.stem.wordnet import WordNetLemmatizer
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

    


    # return snowball.stem(word)

    # stemmer = Stemmer.Stemmer('english')
    # return stemmer.stemWord(word)
    return stem.snowball.SnowballStemmer("english", ignore_stopwords=False).stem(word)
    
    # lmtzr = WordNetLemmatizer()
    # return lmtzr.lemmatize(word) 
    
