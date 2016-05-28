from wedc.domain.core.data.loader import generate_extraction


# first version, will be moved to a function later
def map_clean(data):
    key, text = data
    return (key, generate_extraction(text))



