import os
from wedc.domain.entities.post import Post

# from wedc.domain.core.data.loaders import es_loader
from wedc.domain.core.data import cleaner

mapping = None


def load_input(input):
    # data from intermediate data
    # data[0]: source id
    # data[1]: content, original content of data, \t\n\r should be removed
    imd_dataset = load_intermediate_data(input)

    dataset = []
    for i, data in enumerate(imd_dataset):
        # build data
        # data[0]: pid, used inside program
        # data[1]: sid, unique id for original data
        # data[2]: label, 0 if unknown 
        # data[3]: extraction (tokens), split by space, extracted from original content
        
        pid = i + 1
        sid = data[0]
        extraction = generate_extraction(data[1])
        dataset.append([pid, sid, 0, extraction])
    return dataset    

def load_db(start_pid=1):
    from wedc.infrastructure.model.labelled_data import LabelledData
    # load dataset from database
    labelled_dataset = LabelledData.load_data()

    dataset = []
    for idx, ld in enumerate(labelled_dataset):

        # data[0]: pid, used inside program
        # data[1]: sid, unique id for original data
        # data[2]: label, 0 if unknown 
        # data[3]: extraction (tokens), split by space, extracted from original content
        data = [start_pid+idx, '', int(ld.label), str(ld.extraction)]
        dataset.append(data)

    return dataset

def generate_compressed_data(input=None):
    start_pid = 1
    dataset = []
    if input:
        dataset = load_input(input)
        start_pid += len(dataset)
    dataset.extend(load_db(start_pid=start_pid))
    print dataset

#######################################################
#   Common
#######################################################

def generate_extraction(content):
    try:
        post = Post('', '', content)
    except Exception as e:
        print e
        return ''
    else:
        return post.body

#######################################################
#   Intermediate Data
#######################################################

def load_intermediate_data(path):
    import csv
    dataset = []
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dataset.append(row)
    return dataset


def generate_intermediate_data(dataset, output_path):
    import csv
    with open(output_path, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)
        for data in dataset:
            spamwriter.writerow(data)


#######################################################
#   Load with pid
#######################################################

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

        target_file.write('#'*40 + '\n')
        target_file.write(' '*6 + 'Post id: ' + str(post_id_set[i]) + ' & ' + str(target_id_set[i]) + '    Label: ' +' \n')
        target_file.write('#'*40 + '\n')
        target_file.write(text + '\n')
        target_file.write('#'*40 + '\n')
        target_file.write(posts[i])
        target_file.write('#'*40 + '\n'*3)
    target_file.close()

def load_nodups2dups_mapping(path):
    mapping = {}
    with open(path, 'rb') as f:
        for line in f:
            line = line.strip().split('\t')
            mapping[int(line[0])] = int(line[1])
    return mapping


