import os
from wedc.domain.conf.storage import __res_dir__

from wedc.domain.vendor.nltk import stopword

def get_stopword_set():
    stops = stopword.get_stopwords()
    names = get_person_names()
    # country, country_abbr = stopword_helper.get_country_names()
    numbers = get_numbers()
    nationality = get_nationality_names()
    stop_set = set(stops) | set(numbers) | set(names) | set(nationality) | Set(country) | Set(country_abbr)
    # stop_set = [str(stem.stemming(_).strip()) for _ in stop_set]
    return stop_set

def get_numbers():
    numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 
                'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen',
                'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
                'hundred', 'thousand', 'million', 'billion']
    return numbers


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

def get_person_names():
    result = []
    result.extend(get_male_names())
    result.extend(get_female_names())
    return result


def get_country_names():
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


def get_nationality_names():
    path = os.path.join(__res_dir__, 'stop_words', 'nationality.txt')
    return get_stopword_from_file(path)



