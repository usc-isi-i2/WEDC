import os

from wedc.domain.conf.storage import __res_dir__
from wedc.domain.service.keyword_extraction.seeds import seed_word
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

def build_sd_with_similar_seeds(level=1):
    from wedc.domain.service.keyword_extraction.word2vec import similarity
    from wedc.domain.vendor.nltk import stem

    seed_dict = build_seed_dict()

    seeds = seed_word.load_seed_words()
    for (cate, words) in seeds.items():
        current_level_seed_words = list(words)
        for _ in range(level):
            next_level_seed_words = {}
            for sw in current_level_seed_words:
                similar_words = similarity.get_similar_words(sw)
                if not similar_words:
                    continue

                for similar_word in similar_words:
                    seed_dict.setdefault(similar_word, [])
                    if cate not in seed_dict[similar_word]:
                        seed_dict[similar_word].append(cate)
                    next_level_seed_words.setdefault(similar_word, 0)
                    next_level_seed_words[similar_word] += 1
            current_level_seed_words = next_level_seed_words.keys()

    return seed_dict








    # for (cate, words) in seeds.items():
    #     for word in words:
    #         similar_words = similarity.get_similar_words(word)
    #         # print similar_words
    #         for w in [word] + similar_words:
    #             seed_dict.setdefault(w, [])
    #             if cate not in seed_dict[w]:
    #                 seed_dict[w].append(cate)

    # return seed_dict





        
