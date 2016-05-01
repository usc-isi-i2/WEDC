import os
from wedc.domain.conf.storage import __res_dir__

def get_stopword_from_file(file_path):
    names_list = []
    with open(file_path) as f:
        lines = f.readlines()
        for line in lines:

            names_list.append(line.strip().lower())
    return names_list

def get_male_names():
    path = os.path.join(__res_dir__, 'stop_words', 'male.txt')
    return get_stopword_from_file(path)

def get_female_names():
    path = os.path.join(__res_dir__, 'stop_words', 'female.txt')
    return get_stopword_from_file(path)

def get_names():
    result = []
    result.extend(get_male_names())
    result.extend(get_female_names())
    return result


def get_countries():
    path = os.path.join(__res_dir__, 'stop_words', 'country.txt')
    country_list = []
    country_abbr_list = []
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            abbr, country = line.strip().lower().split('|')
            country_list.append(country)
            country_abbr_list.append(abbr)
    return country_list, country_abbr_list


