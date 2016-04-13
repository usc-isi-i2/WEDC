
import sys
import time
import os
import word2vec

from wedc.domain.vendor.nltk import stem
from wedc.domain.service.keyword_extraction.word2vec import base



def get_similar_words(target_word, n=10):
    """ get similar words
    
    return n similar words for specific target word, already sorted

    Arguments:
        model_path {string} -- model file path
        target_word {string} -- return similar words for this target word
    
    Keyword Arguments:
        n {number} -- number of similar words (default: {10})
    """
    # print base.word2vec_model.vectors.shape
    target_word = stem.stemming(target_word)
    model = base.word2vec_model #word2vec.load(model_path)
    similar_words = []
    try:
        indexes, metrics = model.cosine(target_word, n=n)
        similar_words = [str(_) for _ in list(model.vocab[indexes])]    # similar words
        return similar_words
    except Exception as e: 
        return "NO FOUND"
    
    # print 'similar words\n', similar_words
    # print 'similarity matrix\n', metrics

    # word:similarity pair
    # pairs = [(similar_words[i], metrics[i]) for i in range(len(similar_words))]
    # print 'word:similarity pairs\n', pairs
    
    return similar_words

