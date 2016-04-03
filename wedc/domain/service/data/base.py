
from wedc.domain.service.data.loaders import es_loader

def load_by_path(path):
    data = es_loader.load(path)
    return data