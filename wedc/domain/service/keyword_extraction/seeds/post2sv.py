""" Post to Seed Vector


"""

from wedc.domain.service.keyword_extraction.seeds import seed_word

seeds = seed_word.load_seed_similar_words(level=2)

def post2sv(input, output):
    with open(input, rb) as f:
        for line in f:
            print line
