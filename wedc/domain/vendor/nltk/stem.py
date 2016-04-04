
from nltk import stem

def stemming(word):
    # porter = stem.porter.PorterStemmer()
    # lancaster = stem.lancaster.LancasterStemmer()
    snowball = stem.snowball.EnglishStemmer()

    return snowball.stem(word)