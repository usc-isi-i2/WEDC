

from wedc.domain.core.data.loaders import es_loader
from wedc.domain.core.data import cleaner

def load_data(path, no_dups=False):
    data = es_loader.load(path)
    if no_dups:
        data = cleaner.remove_dups(data)
    return data

def load_data_by_post_id(path, post_id):
    return es_loader.load_post(path, post_id)


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

