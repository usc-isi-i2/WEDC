
import re
import enchant

enchant_dict = enchant.Dict("en_US")

############################################################
#   Post
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
#   Sentence
############################################################

# Leave Blank

############################################################
#   Token
############################################################

def clean_token(token):

    if re.search(r'(\d+[k$]+[/(hr|hour)]*|401[\w\d]*)', token.lower()):
        return '401k'

    if re.search(r'^[xoXO]*((?=xo)|(?=ox))[xoXO]*$', token.lower()):
        return 'xo'

    if re.search(r'^(hrs)$', token.lower()):
        return 'hour'

    # camelcase to space
    if not enchant_dict.check(token.lower()):
        token = re.sub("([a-z])([A-Z])","\g<1> \g<2>", token)

    return token.lower()


