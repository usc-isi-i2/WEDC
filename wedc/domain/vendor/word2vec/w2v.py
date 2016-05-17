
import sys
import os
import word2vec

word2vec_model = None


############################################################
#   Basic
############################################################

def setup_model(input, 
                output, 
                binary=1, 
                cbow=0, 
                size=300, 
                window=10, 
                negative=5, 
                hs=0, 
                threads=12, 
                iter_=5, 
                min_count=5, 
                verbose=False):
    """ setup default value here for word2vec parameters
    """
    return word2vec.word2vec(input, output, binary=binary, cbow=cbow, size=size, window=window, negative=negative, hs=hs, threads=threads, iter_=iter_, min_count=min_count, verbose=verbose)

def load_model(model_path):
    if not os.path.exists(model_path):
        return None
    return word2vec.load(model_path)


############################################################
#   Similar Words
############################################################

def get_similars_by_word(word, n=10):
    from wedc.domain.vendor.nltk import stem

    if not word2vec_model:
        print 'NOT FOUND WORD2VEC MODEL'
        return None

    target_word = stem.stemming(word)
    try:
        indexes, metrics = word2vec_model.cosine(target_word, n=n)
        similar_words = [str(_) for _ in list(word2vec_model.vocab[indexes])]    # similar words
        
        # print 'similar words\n', similar_words
        # print 'similarity matrix\n', metrics

        # word:similarity pair
        pairs = {similar_words[i]: metrics[i] for i in range(len(similar_words))}
        # print 'word:similarity pairs\n', pairs
        
        return pairs
    except Exception:
        print 'NO FOUND SIMILAR WORDS: ', target_word
        return None














