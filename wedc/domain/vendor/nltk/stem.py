"""
Credits:
NodeBox::Linguistics: https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation

"""


from nltk import stem
from nltk.stem.wordnet import WordNetLemmatizer
import re
import inflection
import enchant

def stemming(word):

    be_words = ['am', 'is', 'are', 'was', 'were', 'been']

    if word in be_words:
        return 'be'

    if re.search(r'\d+[k$]+[/(hr|hour)]*', word):
        return '401k'

    lmtzr = WordNetLemmatizer()
    word = lmtzr.lemmatize(word, 'v') 
    word = inflection.singularize(word)

    return word


    # porter = stem.porter.PorterStemmer()
    # lancaster = stem.lancaster.LancasterStemmer()
    # snowball = stem.snowball.EnglishStemmer()
    # return snowball.stem(word)
    
    


    # return snowball.stem(word)

    # stemmer = Stemmer.Stemmer('english')
    # return stemmer.stemWord(word)
    
    
    
    # word = stem.snowball.SnowballStemmer("english", ignore_stopwords=False).stem(word)


    



    
