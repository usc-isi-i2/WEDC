

from wedc.domain.core.data.loaders import es_loader
from wedc.domain.core.data import cleaner

mapping = None

def load_data(input, output, no_dups=False):
    data = es_loader.load(input)

    if no_dups:
        origin_backup_file = open(output+'_with_dups', 'wb')
        origin_backup_file.writelines(data)
        origin_backup_file.close()
        data = cleaner.remove_dups(data, output+'_mapping')

    target_file = open(output, 'wb')
    target_file.writelines(data)
    target_file.close()
    return data

def load_data_by_post_id(path, post_id, no_dups=False):
    target_id = post_id
    if no_dups and mapping:
        target_id = mapping[post_id]
    return es_loader.load_post(path, target_id)

def load_data_by_post_id_set(path, post_id_set, output, no_dups=False):
    import re
    target_id_set = post_id_set
    if no_dups and mapping:
        target_id_set = [mapping[post_id] for post_id in post_id_set]
    raw_posts, posts = es_loader.load_post_by_id_set(path, target_id_set)

    target_file = open(output, 'wb')
    for i in range(len(raw_posts)):
        text = re.sub(r"([\t\n\r]|\\+)", " ", raw_posts[i])
        text = text.encode('ascii', 'ignore')

        target_file.write('#'*70 + '\n')
        target_file.write(' '*6 + 'Post id: ' + str(post_id_set[i]) + '|' + str(target_id_set[i]) + '\n')
        target_file.write('#'*70 + '\n')
        target_file.write(text + '\n')
        target_file.write('#'*70 + '\n'*3)
    target_file.close()
    # return raw_posts, posts

def load_nodups2dups_mapping(path):
    mapping = {}
    with open(path, 'rb') as f:
        for line in f:
            line = line.strip().split('\t')
            mapping[int(line[0])] = int(line[1])
    return mapping


