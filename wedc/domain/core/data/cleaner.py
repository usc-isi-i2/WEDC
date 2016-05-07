import os
import sys
import re
import string
import enchant


from wedc.domain.vendor.nltk import stem
from wedc.domain.core.common import stopword_helper
from wedc.domain.core.common import str_helper
from wedc.domain.core.data.seed import seed_word

enchant_dict = enchant.Dict("en_US")
stopset = stopword_helper.get_stopword_set()

token_mapping = {
    'hrs': 'hour',
    'luv': 'love'
}

seed_words = seed_word.load_seed_words()


############################################################
#   Posts
############################################################

def remove_dups(posts, mapping_path=None):
    import hashlib
    hs = set()
    size = len(posts)
    no_dups = []
    new_pid = 0
    mapping_file = None
    if mapping_path:
        mapping_file = open(mapping_path, 'w')

    for pid in xrange(1, size+1):
        post = posts[pid-1] # pid start from 1
        hashobj = hashlib.sha256()
        hashobj.update(post.strip())
        hash_value = hashobj.hexdigest().lower()
        if hash_value not in hs:
            hs.add(hash_value)
            no_dups.append(post)
            new_pid += 1
            if mapping_file:
                mapping_file.write(str(new_pid)+'\t'+str(pid)+'\n')
    if mapping_file:
        mapping_file.close()
    return no_dups

"""
def remove_dups_from_file(input, output):
    import hashlib
    hs = set()
    output = open(output, 'wb')
    with open(input, 'rb') as f:
        for line in f:
            hashobj = hashlib.sha256()
            hashobj.update(line.strip())
            hash_value = hashobj.hexdigest().lower()
            if hash_value not in hs:
                hs.add(hash_value)
                output.write(line)
"""

############################################################
#   Text
############################################################

def clean_text(text):
    # convert html code
    text = unescape(text)
    text = text.encode('ascii', 'ignore')

    # remove tags
    text = re.sub(r'<[^>]+>', ' ', text)

    # remove url
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    # text = re.sub(r'^[a-z0-9\-\.]+\.(com|org|net|me|cn|biz|us)$', '', text)

    # remove space
    text = re.sub(r'([\t\n\r]|\\+)', ' ', text)

    # remove ' as well as followings
    text = re.sub(r"'\w+", '', text)

    # remove punctuation
    text = re.sub(r'[' + string.punctuation +']+', ' ', text)
    # text = text.translate(string.maketrans('', ''), string.punctuation)
    
    return ' '.join(text.split())  

############################################################
#   Sentence
############################################################

# Leave Blank

############################################################
#   Token
############################################################

def split_token(token):
    def camel_case(word): 
        if re.search(r'([a-z])([A-Z])', word):
            tokens = re.sub("([a-z])([A-Z])","\g<1> \g<2>", word).split()
            return splited_handler(tokens)
        return None

    def first_cap_case(word):
        if re.search(r'([A-Z])([A-Z])([a-z])', word):
            tokens = re.sub("([A-Z])([A-Z])([a-z])","\g<1> \g<2>\g<3>", word).split()
            return splited_handler(tokens)
        return None

        
    def splited_handler(splited_list):
        word = None
        if len(splited_list) > 1:
            splited = []
            for t in splited_list:
                t = clean_token(t)
                if t and (enchant_dict.check(t) or t in seed_words):
                    splited.append(t)
            if splited:
                word = ' '.join(splited)
        return word

    if not enchant_dict.check(token.lower()):
        # print token
        tmp = first_cap_case(token)
        if tmp: return tmp
        tmp = camel_case(token)
        if tmp: return tmp
        
    return token

def mars2norm(token):
    # if re.search(r'^(hrs)$', token.lower()):
    #     return 'hour'
    if token.lower() in token_mapping:
        return token_mapping[token.lower()]
    return token

def clean_token(token):
    token = split_token(token)
    if not token:
        return None

    if re.search(r'(\d+[k$]+[/(hr|hour)]*|401[\w\d]*)', token.lower()):
        return '401k'

    if re.search(r'^[xoXO]*((?=xo)|(?=ox))[xoXO]*$', token.lower()):
        return 'xo'

    token = mars2norm(token)

    if re.search(r'\d', token): # only contain digits
        return None
    if len(token) == 1 or re.search(r'^(.)\1*$', token): 
        # only contain one character or repeat character
        return None
    if len(token) > 15 and not enchant_dict.check(token.lower()):
        return None

    if token in stopset:
        return None
    token = stem.stemming(token.lower()).strip()
    if token in stopset:   # double check for unexpected text form, like 'marias'
        return None

    return token.lower()

############################################################
#   Helper
############################################################

def unescape(text):
    import re, htmlentitydefs
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


