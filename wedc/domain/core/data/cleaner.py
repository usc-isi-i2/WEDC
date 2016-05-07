
import re
import string
import enchant


from wedc.domain.vendor.nltk import stem
from wedc.domain.core.common import stopword_helper
from wedc.domain.core.common import str_helper

enchant_dict = enchant.Dict("en_US")
stopset = stopword_helper.get_stopword_set()


############################################################
#   Posts
############################################################

def remove_dups(posts):
    import hashlib
    hs = set()
    no_dups = []
    for post in posts:
        hashobj = hashlib.sha256()
        hashobj.update(post.strip())
        hash_value = hashobj.hexdigest().lower()
        if hash_value not in hs:
            hs.add(hash_value)
            no_dups.append(post)
    return no_dups

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

def clean_token(token):

    # camelcase to space
    if not enchant_dict.check(token.lower()):
        tokens = re.sub("([a-z])([A-Z])","\g<1> \g<2>", token).split()
        if len(tokens) > 1:
            splited = []
            for t in tokens:
                if clean_token(t):
                    splited.append(t)
            if splited:
                token = ' '.join(splited)
            else:
                return None

    if re.search(r'(\d+[k$]+[/(hr|hour)]*|401[\w\d]*)', token.lower()):
        return '401k'

    if re.search(r'^[xoXO]*((?=xo)|(?=ox))[xoXO]*$', token.lower()):
        return 'xo'

    if re.search(r'^(hrs)$', token.lower()):
        return 'hour'

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


