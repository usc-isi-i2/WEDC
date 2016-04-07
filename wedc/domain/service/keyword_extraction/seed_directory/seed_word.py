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



        
