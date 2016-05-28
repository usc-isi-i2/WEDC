from wedc.domain.core.data.loader import generate_extraction

def map_clean(data):
    key, text = data
    return (key, generate_extraction(text))



