from nltk.corpus import stopwords
import string


def get_stopwords():
    
    stop = stopwords.words('english') + list(string.punctuation)
    return stop
