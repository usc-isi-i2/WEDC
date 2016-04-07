import os

from wedc.domain.conf.storage import __res_dir__
from wedc.domain.service.keyword_extraction.seed_directory import seed_word
from wedc.domain.service.keyword_extraction.word2vec import similarity

def build_seed_dict():
    seed_dict = {}
    seeds = seed_word.load_seed_words()
    for (cate, words) in seeds.items():
        for word in words:
            similar_words = similarity.get_similar_words(word)
            # print similar_words
            for w in [word] + similar_words:
                seed_dict.setdefault(w, [])
                if cate not in seed_dict[w]:
                    seed_dict[w].append(cate)

    return seed_dict





        
