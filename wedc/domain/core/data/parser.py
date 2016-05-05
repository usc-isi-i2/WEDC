import re
import string
from sets import Set

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from wedc.domain.core.common import str_helper
from wedc.domain.vendor.nltk import stopword
from wedc.domain.vendor.nltk import stem
from wedc.domain.core.http import domain
from wedc.domain.core.common import stopword_helper




trantab = string.maketrans(string.punctuation,' '*(len(string.punctuation)))

class DataParser():
    def __init__(self):
        self.stopset = self.load_stopset()

    def load_stopset(self):
        stops = stopword.get_stopwords()
        names = stopword_helper.get_person_names()
        # country, country_abbr = stopword_helper.get_country_names()
        nationality = stopword_helper.get_nationality_names()
        stop_set = Set(stops) | Set(names) | Set(nationality) # | Set(country) # | Set(country_abbr) 
        stop_set = [str(stem.stemming(_).strip()) for _ in stop_set]
        return stop_set

    def parse(self, text):
        text = self.text_preprocessing(text)
        
        sentences = [sentence for sentence in sent_tokenize(text)]
        # sentences = [nltk.word_tokenize(sent) for sent in sentences]


        print sentences
        # self.sentence_operation(sentence)
        # sentences = self.sentence_operation(' '.join(sentences).lower())

        # tokens = [self.token_operation(token) for token in word_tokenize(sentences) if token not in stop and not has_url(token)]
        # tokens = [_ for _ in tokens if _ and _ != ' ' and _ not in stop_set]
        # ans = ' '.join(list(set(tokens)))
        # return str(ans)
        # 

    def text_preprocessing(self, text):

        text = text.encode('ascii', 'ignore')

        # remove tags
        text = re.sub(r'<[^>]+>', ' ', text)

        # remove url
        text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
        text = re.sub(r'^[a-z0-9\-\.]+\.(com|org|net|me|cn|biz|us)$', '', text.lower())

        # remove space
        text = re.sub(r'([\t\n\r]|\\+)', ' ', text)

        # text = text.translate(trantab)
        return ' '.join(text.split())  
    



"""
# for more domain ext
# domain_ext_list = domain.get_domain_ext_list()
# text = re.sub(r'^[a-z0-9\-\.]+\.('+'|'.join(domain_ext_list)+')$', '', text)

"""