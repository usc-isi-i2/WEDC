
from wedc.domain.core.data.seed import seed_word



def generate_post_vector(extraction_list, seeds, output=None):
    seed_words = seeds.keys()
    seeds_size = len(seed_words)
    seed_words.sort()

    
    vectors = []
    for line in extraction_list:
        vector = ['0'] * seeds_size
        tokens = line.split(' ')
        for i in range(seeds_size):
            if seed_words[i] in tokens:
                vector[i] = str(1.0 * float(seeds[seed_words[i]]))
        vector = ' '.join(vector)
        vectors.append(vector)

    if output:
        output = open(output, 'wb')
        for vector in vectors:
            output.write(vector+'\n')
        output.close()

    return vectors

def post2sv(input, output, seeds):
    with open(input, 'rb') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return generate_post_vector(lines, seeds, output)

"""
def post2sv(input, output, seeds):
    seed_words = seeds.keys()
    seeds_size = len(seed_words)
    seed_words.sort()

    output = open(output, 'wb')
    with open(input, 'rb') as f:
        for line in f:
            line = line.strip()
            vector = ['0'] * seeds_size
            tokens = line.split(' ')
            for i in range(seeds_size):
                if seed_words[i] in tokens:
                    vector[i] = str(1.0 * float(seeds[seed_words[i]]))
            output.write(' '.join(vector) + '\n')
    output.close()
    return seed_words
"""
def generate_post_vector_seed(extraction_list, output=None, seeds=None):
    seed_words = seeds.keys()
    seeds_size = len(seed_words)
    seed_words.sort()

    idx = 1
    vectors = []
    for line in extraction_list:
        line = line.strip()
        tmp = {}
        tokens = line.split(' ')
        for sw in seed_words:
            if sw in tokens:
                tmp.setdefault(str((sw, str(1.0 * float(seeds[sw])))), 0)
        vector = 'post_id:'+ str(idx) + '    ' +','.join(tmp.keys()) + '\n'
        vectors.append(vector)
        idx += 1 

    if output:
        output = open(output, 'wb')
        for vector in vectors:
            output.write(vector)
        output.close()

    return vectors

def post2seed(input, output=None, seeds=None):
    with open(input, 'rb') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return generate_post_vector_seed(lines, seeds, output)

"""
def post2seed(input, output, seeds):
    seed_words = seeds.keys()
    seeds_size = len(seed_words)
    seed_words.sort()

    output = open(output, 'wb')
    # sep_line_width = 70
    # output.write('\n\n\n' + '#'*sep_line_width +'\n')
    # output.write('#\t\t Features (' + str(len(seed_words)) + ')')
    # output.write('\n' + '#'*sep_line_width +'\n')
    # output.write(str(seed_words))
    # output.write('\n\n\n' + '#'*sep_line_width +'\n')
    # output.write('#\t\t Post Feature Words')
    # output.write('\n' + '#'*sep_line_width +'\n')

    with open(input, 'rb') as f:
        idx = 1
        for line in f:
            line = line.strip()
            tmp = {}
            tokens = line.split(' ')
            for sw in seed_words:
                if sw in tokens:
                    tmp.setdefault(str((sw, str(1.0 * float(seeds[sw])))), 0)
            output.write('post:'+ str(idx) + '    ' +','.join(tmp.keys()) + '\n')
            idx += 1

    output.close()
"""