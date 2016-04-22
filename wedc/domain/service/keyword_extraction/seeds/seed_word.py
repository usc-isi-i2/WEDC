import os

from wedc.domain.conf.storage import __res_dir__


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


def load_seed_words():
    files_dict = get_seed_files()
    seeds = {}
    for (cate, paths) in files_dict.items():
        seeds.setdefault(cate, [])
        for path in paths:
            with open(path) as f:
                lines = f.readlines()
                for line in lines:
                    seeds[cate].append(line.strip())
    return seeds

def load_all_seed_words():
    files_dict = get_seed_files()
    seeds = []
    for (cate, paths) in files_dict.items():
        for path in paths:
            with open(path) as f:
                lines = f.readlines()
                for line in lines:
                    seeds.append(line.strip())
    return seeds





def load_seed_similar_words(level=1):
    from wedc.domain.service.keyword_extraction.word2vec import similarity
    from wedc.domain.vendor.nltk import stem
    seed_words = [stem.stemming(_) for _ in load_all_seed_words()]

    ans = {}
    [ans.setdefault(_, 1) for _ in seed_words]

    current_level_seed_words = list(seed_words)
    for _ in range(level):
        next_level_seed_words = {}
        for seed_word in current_level_seed_words:
            similar_words_dict = similarity.get_similar_words_with_similarity(seed_word)
            if not similar_words_dict:
                # print seed_word
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


def cache_seed_similar_words(model, seed_words=None, level=1, path=None):
    from wedc.domain.service.keyword_extraction.word2vec import similarity
    from wedc.domain.vendor.nltk import stem

    if not seed_words:
        seed_words = [str(stem.stemming(_)) for _ in load_all_seed_words()]
    
    num_words, num_vectors = model.vectors.shape

    with open(path, 'w') as f:
        for seed_word in seed_words:
            # similar_words_dict = similarity.get_similar_words_with_similarity(model, seed_word)
            # if not similar_words_dict:
            #     continue
            
            try:
                indexes, metrics = model.cosine(seed_word, n=num_words)
            except Exception as e:
                print seed_word
                continue
            similar_words_from_model = [str(_.encode('ascii', 'ignore')) for _ in list(model.vocab[indexes])]    # similar words

            similar_words = {}
            cur_sws = [seed_word]
            for _ in range(level):
                next_sws = {}
                for w in cur_sws:
                    tmp = similarity.get_similar_words(model, w)
                    [similar_words.setdefault(_, 0) for _ in tmp]
                    # [similar_words.setdefault[_]+=1 for _ in tmp]
                    [next_sws.setdefault(_, 0) for _ in tmp]
                cur_sws = next_sws.keys()
            
            sw_words, sw_similarity = [], []

            # print similar_words.keys()

            for sw in similar_words.keys():
                if sw == seed_word:
                    continue 
                idx = similar_words_from_model.index(sw)
                sw_words.append(sw)
                sw_similarity.append(str(metrics[idx]))

            f.write(seed_word + '\t')
            f.write(' '.join(sw_words) + '\t')
            f.write(' '.join(sw_similarity) + '\n')
            
    

def generate_weighted_seed_dict(ssw_cache_path, other_ssw_cache_path=None):

    seed_dict = {}
    with open(ssw_cache_path, 'r') as f:
        for line in f:
            line = line.split('\t')
            seed_word = line[0]
            similar_words = line[1].split()
            similarity = line[2].split()
            
            seed_dict.setdefault(seed_word, '1')

            for i in range(len(similar_words)):
                swk = similar_words[i]
                swv = similarity[i]

                seed_dict.setdefault(swk, 0)
                seed_dict[swk] = max(float(seed_dict[swk]), swv)

    if not other_ssw_cache_path:
        return seed_dict

    # weight with dect from other word2vec mdoel results

    sd_words = seed_dict.keys()

    with open(ssw_cache_path, 'r') as f:
        for line in f:
            line = line.split('\t')
            seed_word = line[0]
            similar_words = line[1].split()
            similarity = line[2].split()

            for i in range(len(similar_words)):
                swk = similar_words[i]
                swv = similarity[i]

                if swk in sd_words:
                    seed_dict[swk] = (float(seed_dict[swk]) + float(swv)) / 2.0
    return seed_dict







    



""" Departed

def load_seed_similar_words(level=1):
    from wedc.domain.service.keyword_extraction.word2vec import similarity
    from wedc.domain.vendor.nltk import stem
    seed_words = load_all_seed_words()
    # print similarity.get_similar_words('401k')

    ans = {}
    [ans.setdefault(stem.stemming(_), 1) for _ in seed_words]

    current_level_seed_words = list(seed_words)
    for _ in range(level):
        next_level_seed_words = {}
        for seed_word in current_level_seed_words:
            similar_words = similarity.get_similar_words(seed_word)
            for similar_word in similar_words:
                ans.setdefault(similar_word, 0)
                ans[similar_word] += 1
                next_level_seed_words.setdefault(similar_word, 0)
                next_level_seed_words[similar_word] += 1
        current_level_seed_words = next_level_seed_words.keys()
    ans = ans.keys()
    ans.sort()
    return ans

"""





        
