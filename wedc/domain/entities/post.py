import re
import string
from sets import Set

from nltk.tokenize import sent_tokenize
from wedc.domain.core.common import str_helper
from nltk.tokenize import word_tokenize
from wedc.domain.vendor.nltk import stopword
from wedc.domain.vendor.nltk import stem
from wedc.domain.core.http import domain
from wedc.domain.core.common import stopword_helper

from wedc.domain.core.data.parser import DataParser

domain_ext_list = domain.get_domain_ext_list()
stop = stopword.get_stopwords()
names = stopword_helper.get_person_names()
country, country_abbr = stopword_helper.get_country_names()
nationality = stopword_helper.get_nationality_names()
stop_set = Set(names) | Set(country) | Set(country_abbr) | Set(nationality)
stop_set = [stem.stemming(_).strip() for _ in stop_set]
trantab = string.maketrans(string.punctuation,' '*(len(string.punctuation)))

def remove_tags(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub(' ', text)

def remove_url(text):
    text = text.lower()
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    text = re.sub(r'^[a-z0-9\-\.]+\.('+'|'.join(domain_ext_list)+')$', '', text)
    return text

def has_url(text):
    text = text.lower()
    if re.search(r'[a-z0-9\-\.]+\.(com|net|org|me)', text):
        return True
    return False

def valid_digit(text):
    """ judge if the token is valid with digit
    valid: 401k
    """
    if re.search(r'^/d*$', text):
        return False
    return True

class Post(object):

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = self.parse_body_word(body)

    def initialize(self):
        """ initialize main conent of doc
        """
        pass

    def parse_body_word(self,body):
        contents = []
        if isinstance(body, basestring):
            contents.append(body)
        else:
            contents = body

        dp = DataParser()
        return dp.parse(' '.join(contents))

        
    def token_operation(self, token):
        if re.search(r'\d+[k$]+[/(hr|hour)]*', token):
            return '#/h'
        if re.search(r'\d', token):
            return None
        if len(token) == 1:
            return None
        return stem.stemming(token).strip()

    def sentence_operation(self, sentence):
        sentence = remove_tags(sentence)
        sentence = remove_url(sentence)
        sentence = re.sub(r'([\t\n\r]|\\+)', ' ', sentence)
        sentence = sentence.encode('ascii', 'ignore')
        sentence = sentence.translate(trantab)

        # Substitute multiple whitespace with single whitespace
        return ' '.join(sentence.split())   
