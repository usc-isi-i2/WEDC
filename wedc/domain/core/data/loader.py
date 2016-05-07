

from wedc.domain.core.data.loaders import es_loader
from wedc.domain.core.data import cleaner

def load_data(path, no_dups=False):
    data = es_loader.load(path)
    if no_dups:
        data = cleaner.remove_dups(data)
    return data

def load_data_by_post_id(path, post_id):
    return es_loader.load_post(path, post_id)

