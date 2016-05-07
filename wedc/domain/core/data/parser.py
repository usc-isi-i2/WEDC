import re

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from wedc.domain.core.data import cleaner

def parse(text):
    text = text_preprocessing(text) 
    tokens = [token_preprocessing(token) for token in word_tokenize(text)]
    tokens = [_ for _ in tokens if _]
    return str(' '.join(set(tokens)))

def text_preprocessing(text):
    return cleaner.clean_text(text)

def token_preprocessing(token):
    return cleaner.clean_token(token)


"""
# for more domain ext
# domain_ext_list = domain.get_domain_ext_list()
# text = re.sub(r'^[a-z0-9\-\.]+\.('+'|'.join(domain_ext_list)+')$', '', text)

# for sentence processing
# sentences = [sentence for sentence in sent_tokenize(text)]
# sentences = [nltk.word_tokenize(sent) for sent in sentences]

"""