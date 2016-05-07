

from wedc.domain.core.data.seed import seed_word


def post2sv(input, output, seeds):
    seed_words = seeds.keys()
    seeds_size = len(seed_words)
    seed_words.sort()

    output = open(output, 'wb')
    with open(input, 'rb') as f:
        for line in f:
            line = line.strip()
            flag = False
            vector = ['0'] * seeds_size
            for i in range(seeds_size):
                if seed_words[i] in line:
                    vector[i] = str(1.0 * float(seeds[seed_words[i]]))
            output.write(' '.join(vector) + '\n')
    output.close()
    return seed_words


def post2seed(input, output, seeds):
    seed_words = seeds.keys()
    seeds_size = len(seed_words)
    seed_words.sort()

    output = open(output, 'wb')
    output.write('\n====================\n')
    output.write(str(seed_words))
    output.write('\n====================\n')

    with open(input, 'rb') as f:
        idx = 1
        for line in f:
            tmp = []
            for i in range(seeds_size):
                if seed_words[i] in line.split(' '):
                    flag = True
                    tmp.append(str((seed_words[i], str(1.0 * float(seeds[seed_words[i]])))))
            output.write('post:'+ str(idx) + '    ' +','.join(tmp) + '\n')
            idx += 1
    output.close()