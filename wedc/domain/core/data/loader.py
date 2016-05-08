

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
    # print 'target_id', target_id
    return es_loader.load_post(path, target_id)

def load_nodups2dups_mapping(path):
    mapping = {}
    with open(path, 'rb') as f:
        for line in f:
            line = line.strip().split('\t')
            mapping[int(line[0])] = int(line[1])
    return mapping


