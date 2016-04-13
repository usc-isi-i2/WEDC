""" Post to Seed Vector


"""

from wedc.domain.service.keyword_extraction.seeds import seed_word

seeds = seed_word.load_seed_similar_words(level=2)
seeds_size = len(seeds)

def post2sv(input, output):
    


    output = open(output, 'wb')

    doc_id = 0
    with open(input, 'rb') as f:
        for line in f:
            vector = ['0'] * seeds_size

            for i in range(seeds_size):
                if seeds[i] in line:
                    vector[i] = '1'

            # print vector
            output.write(str(doc_id) + '\t' + ' '.join(vector) + '\n')
            
        doc_id += 1


    output.close()
