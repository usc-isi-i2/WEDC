import os
from wedc.domain.conf.storage import __res_dir__

# from wedc.domain.vendor.word2vec import w2v
from wedc.domain.vendor.nltk import stem

############################################################
#   Seed Words
############################################################

def get_seed_files():
    file_paths = {}
    path = os.path.join(__res_dir__, 'seed_words')
    for subdir, dirs, files in os.walk(path):
        for fname in files:
            if fname[0] != '.':
                file_path = os.path.join(subdir, fname)
                cate_name = subdir.split('/')[-1]
                file_paths.setdefault(cate_name, [])
                file_paths[cate_name].append(file_path)
    return file_paths

def load_seed_words(category=None):
    files_dict = get_seed_files()
    if category:
        paths = files_dict[category]
    else:        
        paths = [path for _ in files_dict.values() for path in _]

    seeds = []
    for path in paths:
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                seeds.append(line.strip().lower())
    return seeds

def load_seed_words_with_category():
    files_dict = get_seed_files()
    seeds = {}
    for (cate, paths) in files_dict.items():
        seeds.setdefault(cate, [])
        for path in paths:
            with open(path) as f:
                lines = f.readlines()
                for line in lines:
                    seeds[cate].append(line.strip().lower())
    return seeds

""" 
#comment for spark

############################################################
#   Similar Words of Seed Words
############################################################

def load_seed_similar_words(seed_words=None, level=1, n=10):
    # seed_words = [stem.stemming(_) for _ in load_seed_words()]
    if not seed_words:
        seed_words = [_ for _ in load_seed_words()]

    ans = {}
    [ans.setdefault(_, 1) for _ in seed_words]

    current_level_seed_words = list(seed_words)
    for _ in range(level):
        next_level_seed_words = {}
        for seed_word in current_level_seed_words:
            similar_words_dict = w2v.get_similars_by_word(seed_word, n=n)
            if not similar_words_dict:
                continue
            for (similar_word, sw_similarity) in similar_words_dict.items():
                ans.setdefault(similar_word, 0)
                ans[similar_word] = max(ans[similar_word], sw_similarity)

                next_level_seed_words.setdefault(similar_word, 0)
                next_level_seed_words[similar_word] += 1
        current_level_seed_words = next_level_seed_words.keys()
    # ans = ans.keys()
    # ans.sort()
    return ans


############################################################
#   Build Weighted Seed Dict from Word2Vec Model
############################################################

def generate_seed_dict(seed_words=None, w2v_model_path=None, level=1, n=10):
    if not seed_words:
        seed_words = [str(_) for _ in load_seed_words()]

    if not w2v_model_path:
        return {_:1. for _ in seed_words}

    w2v.word2vec_model = w2v.load_model(w2v_model_path)
    model = w2v.word2vec_model
    num_words, num_vectors = model.vectors.shape

    seed_dict = {}
    for seed_word in seed_words:
        try:
            indexes, metrics = model.cosine(seed_word, n=num_words)
        except Exception as e: # seed_word is not in w2v model
            seed_dict.setdefault(seed_word, 1.) 
            continue

        similar_words = w2v.get_level_similars(seed_word, level=level, n=n)
        similars = model.generate_response(indexes, metrics).tolist()
        similar_words = [_ for _ in similars if _[0] in similar_words]

        for sw in similar_words:
            seed_dict.setdefault(sw[0], 0.)
            seed_dict[sw[0]] = max(seed_dict[sw[0]], float(sw[1]))
        
    return seed_dict

#comment for spark
"""
        

""" Seed Words that doesn't find its simialrs
NO FOUND SIMILAR WORDS:  gel
NO FOUND SIMILAR WORDS:  shiatsu
NO FOUND SIMILAR WORDS:  jacuzzi
NO FOUND SIMILAR WORDS:  gigolo
NO FOUND SIMILAR WORDS:  hunk
NO FOUND SIMILAR WORDS:  transvestite
NO FOUND SIMILAR WORDS:  tranny
NO FOUND SIMILAR WORDS:  she-male
NO FOUND SIMILAR WORDS:  ladyboy
# similar_words_from_model = [str(_.encode('ascii', 'ignore')) for _ in list(model.vocab[indexes])]   # similar words in desc order by similarity
# idx = similar_words_from_model.index(sw)
# seed_dict.setdefault(sw, 0.)
# seed_dict[sw] = max(seed_dict[sw], float(metrics[idx]))
"""
