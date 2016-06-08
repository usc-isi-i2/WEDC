import re

from wedc.domain.core.data import cleaner
from wedc.domain.vendor.crf.crf_tokenizer import CrfTokenizer

def parse(text):
    text = text_preprocessing(text) 
    t = CrfTokenizer()
    t.setRecognizeHtmlEntities(True)
    t.setRecognizeHtmlTags(True)
    t.setSkipHtmlTags(True)
    tokens = t.tokenize(text)
    tokens = [token_preprocessing(token) for token in tokens]

    tokens = [_ for _ in tokens if _]
    return str(' '.join(set(tokens)))

def text_preprocessing(text):
    return cleaner.clean_text(text)

def token_preprocessing(token):
    return cleaner.clean_token(token)
