
from wedc.domain.service.data.loaders import es_loader

def load_by_path(path):
    return es_loader.load(path)


def load_by_memex(path):
    pass
