""" Post to Seed Vector
"""

from wedc.domain.service.keyword_extraction.seeds import seed_word



def post2sv(input, output):
    seeds = seed_word.load_seed_similar_words(level=2).keys()
    seeds_size = len(seeds)
    output = open(output, 'wb')
    with open(input, 'rb') as f:
        for line in f:
            if not line:
                continue
            vector = ['0'] * seeds_size
            # print line
            # print seeds[1:10]
            for i in range(seeds_size):
                if seeds[i] in line.split(' '):
                    vector[i] = '1'
            output.write(' '.join(vector) + '\n')
    output.close()


def post2sv_weighted(input, output, seeds):
    seed_words = seeds.keys()
    seeds_size = len(seed_words)
    seed_words.sort()

    output = open(output, 'wb')
    with open(input, 'rb') as f:
        for line in f:
            vector = ['0'] * seeds_size

            for i in range(seeds_size):
                if seed_words[i] in line:
                    vector[i] = 1.0 * float(seeds[seed_words[i]])
            output.write(' '.join(vector) + '\n')
    output.close()

    return seed_words



