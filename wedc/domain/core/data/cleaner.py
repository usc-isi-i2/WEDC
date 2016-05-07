
import re
import enchant

def clean_token(token):

    if re.search(r'(\d+[k$]+[/(hr|hour)]*|401[\w\d]*)', token.lower()):
        return '401k'

    if re.search(r'^[xoXO]*((?=xo)|(?=ox))[xoXO]*$', token.lower()):
        return 'xo'

    if re.search(r'^(hrs)$', token.lower()):
        return 'hour'

    # camelcase to space
    if not enchant.Dict("en_US").check(token.lower()):
        token = re.sub("([a-z])([A-Z])","\g<1> \g<2>", token)



    return token.lower()


