

import hashlib
from sets import Set

def remove_dup(input, output):
    hs = Set()
    output = open(output, 'wb')
    with open(input, 'rb') as f:
        for line in f:
            hashobj = hashlib.sha256()
            hashobj.update(line.strip())
            hash_value = hashobj.hexdigest().lower()
            if hash_value not in hs:
                hs.add(hash_value)
                output.write(line)

