import os
# from wedc.domain.conf.storage import __res_dir__
from wedc.domain.res import *

############################################################
#   Seed Words
############################################################

"""
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
"""


def load_seed_words(category=None):
    # files_dict = get_seed_files()
    # if category:
    #     paths = files_dict[category]
    # else:        
    #     paths = [path for _ in files_dict.values() for path in _]

    # seeds = []
    # for path in paths:
    #     with open(path) as f:
    #         lines = f.readlines()
    #         for line in lines:
    #             seeds.append(line.strip().lower())
    # return seeds
    if category:
        if category == 'escort':
            return RES_ESCORT
        elif category == 'job_ads':
            return RES_JOB_ADS
        elif category == 'massage':
            return RES_MASSAGE
    else:
        return RES_SEED_WORDS

def load_seed_words_with_category():
    # files_dict = get_seed_files()
    # seeds = {}
    # for (cate, paths) in files_dict.items():
    #     seeds.setdefault(cate, [])
    #     for path in paths:
    #         with open(path) as f:
    #             lines = f.readlines()
    #             for line in lines:
    #                 seeds[cate].append(line.strip().lower())
    # return seeds

    seeds = {}
    seeds['escort'] = RES_ESCORT
    seeds['job_ads'] = RES_JOB_ADS
    seeds['massage'] = RES_MASSAGE






