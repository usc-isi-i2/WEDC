
import sys
import time
import os
import word2vec

from wedc.domain.vendor.nltk import stem


def get_similar_words(model_path, target_word, n=10):
    """ get similar words
    
    return n similar words for specific target word, already sorted

    Arguments:
        model_path {string} -- model file path
        target_word {string} -- return similar words for this target word
    
    Keyword Arguments:
        n {number} -- number of similar words (default: {10})
    """
    target_word = stem.stemming(target_word)
    model = word2vec.load(model_path)
    similar_words = []
    try:
        indexes, metrics = model.cosine(target_word, n=n)
        similar_words = [str(_) for _ in list(model.vocab[indexes])]    # similar words
        return similar_words
    except Exception as e: 
        return similar_words
    
    # print 'similar words\n', similar_words
    # print 'similarity matrix\n', metrics

    # word:similarity pair
    # pairs = [(similar_words[i], metrics[i]) for i in range(len(similar_words))]
    # print 'word:similarity pairs\n', pairs
    
    return similar_words

