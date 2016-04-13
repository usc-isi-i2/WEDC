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






        
