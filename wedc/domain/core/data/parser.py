import re
import string
from sets import Set

import nltk
import enchant
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from wedc.domain.core.common import str_helper
from wedc.domain.vendor.nltk import stopword
from wedc.domain.vendor.nltk import stem
from wedc.domain.core.http import domain
from wedc.domain.core.common import stopword_helper
from wedc.domain.core.data import cleaner

trantab = string.maketrans(string.punctuation,' '*(len(string.punctuation)))

class DataParser():
    def __init__(self):
        self.stopset = self.load_stopset()
        self.enchant_dict = enchant.Dict("en_US")

    def load_stopset(self):
        stops = stopword.get_stopwords()
        names = stopword_helper.get_person_names()
        # country, country_abbr = stopword_helper.get_country_names()
        nationality = stopword_helper.get_nationality_names()
        stop_set = Set(stops) | Set(names) | Set(nationality) # | Set(country) # | Set(country_abbr) 
        # stop_set = [str(stem.stemming(_).strip()) for _ in stop_set]
        return stop_set

    def parse(self, text):
        text = self.text_preprocessing(text) 
        tokens = [self.token_preprocessing(token) for token in word_tokenize(text)]
        tokens = [_ for _ in tokens if _]

        return str(' '.join(set(tokens)))
        
        # print tokens
    
        # self.sentence_operation(sentence)
        # sentences = self.sentence_operation(' '.join(sentences).lower())

        # tokens = [self.token_operation(token) for token in word_tokenize(sentences) if token not in stop and not has_url(token)]
        # tokens = [_ for _ in tokens if _ and _ != ' ' and _ not in stop_set]
        # ans = ' '.join(list(set(tokens)))
        # return str(ans)

    def text_preprocessing(self, text):

        # convert html code
        text = unescape(text)

        try:
            text = text.encode('ascii', 'ignore')
        except Exception as e:
            print text

        

        # remove tags
        text = re.sub(r'<[^>]+>', ' ', text)

        # remove url
        text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
        # text = re.sub(r'^[a-z0-9\-\.]+\.(com|org|net|me|cn|biz|us)$', '', text)

        # remove space
        text = re.sub(r'([\t\n\r]|\\+)', ' ', text)

        # remove ' as well as followings
        text = re.sub(r"'\w+", '', text)

        # remove punctuation
        text = re.sub(r'[' + string.punctuation +']+', ' ', text)

        # text = text.translate(trantab)
        return ' '.join(text.split())  

    def token_preprocessing(self, token):
        token = cleaner.clean_token(token)

        if re.search(r'\d', token): # only contain digits
            return None
        if len(token) == 1 or re.search(r'^(.)\1*$', token): 
            # only contain one character or repeat character
            return None
        if len(token) > 15 and not self.enchant_dict.check(token):
            return None
        if token in self.stopset:
            return None
        token = stem.stemming(token).strip()
        if token in self.stopset:   # double check for unexpected text form, like 'marias'
            return None

        return token


def unescape(text):
    import re, htmlentitydefs
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

"""
# for more domain ext
# domain_ext_list = domain.get_domain_ext_list()
# text = re.sub(r'^[a-z0-9\-\.]+\.('+'|'.join(domain_ext_list)+')$', '', text)

# for sentence processing
# sentences = [sentence for sentence in sent_tokenize(text)]
# sentences = [nltk.word_tokenize(sent) for sent in sentences]

"""