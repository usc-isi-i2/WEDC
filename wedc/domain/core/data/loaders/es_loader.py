
import json
import os
import re


# from wedc.domain.entities.post import Post
from wedc.domain.core.data import loader
 


ES_POST_ID = '_id'
ES_POST_SOURCE = '_source'
ES_POST_URL = 'url'
ES_POST_TITLE = 'hasTitlePart'
ES_POST_BODY = 'hasBodyPart'
ES_POST_TEXT = 'text'

def load(path):
    if not path or not os.path.exists(path):
        print 'FILE IS NOT EXIST'
        return None

    pn_file = open(path, 'rU')
    raw = json.load(pn_file)
    pn_file.close()
    hits = raw['hits']['hits']

    # data in dataset
    # data[0]: source id
    # data[1]: content
    dataset = []

    for hit in hits[:10]:
        try:
            sid = str(hit[ES_POST_ID])
            source = hit[ES_POST_SOURCE]
            post_url, post_title, post_body = None, None, None

            if ES_POST_BODY not in source:
                dataset.append([sid, ''])
                continue

            post_url = source[ES_POST_URL]
            post_title = source[ES_POST_TITLE][ES_POST_TEXT]
            post_body = extract_content_from_post_body(source[ES_POST_BODY][ES_POST_TEXT])

            dataset.append([sid, post_body])

        except Exception as e: 
            print "ERROR: " + str(e)

    drive, path_and_file = os.path.splitdrive(path)
    path_, file_ = os.path.split(path_and_file)
    loader.generate_intermediate_data(dataset, 'imd_'+file_)
    return dataset


#######################################################
#   Common
#######################################################

def extract_content_from_post_body(post_body):
    content = []
    if isinstance(post_body, basestring):
        content.append(post_body)
    else:
        content = post_body
    content = ' '.join(content)
    content = content.encode('ascii', 'ignore')
    content = re.sub(r'([\t\n\r]|\\+)', ' ', content)
    return str(content)

#######################################################
#   Old API
#######################################################

def load_post(path, post_id):
    post_id = post_id-1
    if not path:
        return None
    pn_file = open(path, 'rU')
    raw = json.load(pn_file)
    pn_file.close()
    
    hits = raw['hits']['hits']
    size = len(hits)

    if post_id >= size:
        return None    

    source = hits[post_id]['_source']
    if 'hasBodyPart' not in source:
        return None
    text = source['hasBodyPart']['text']

    contents = []
    if isinstance(text, basestring):
        contents.append(text)
    else:
        contents = text
    text = ' '.join(contents) 

    post = Post('', '', text)
    return text, post

def load_post_by_id_set(path, post_id_set):
    
    if not path:
        return None

    post_id_set = [post_id-1 for post_id in post_id_set]
    pn_file = open(path, 'rU')
    raw = json.load(pn_file)
    pn_file.close()
    hits = raw['hits']['hits']
    posts = []

    hits = [hits[idx] for idx in range(len(hits)) if idx in post_id_set]
    raw_posts = []
    for hit in hits: # [:100]:
        try:
            source = hit[ES_POST_SOURCE]
            post_url, post_title, post_body = None, None, None

            if ES_POST_BODY not in source:
                posts.append('\n')
                raw_posts.append('\n')
                continue

            post_url = source[ES_POST_URL]
            post_title = source[ES_POST_TITLE][ES_POST_TEXT]
            post_body = source[ES_POST_BODY][ES_POST_TEXT]

            contents = []
            if isinstance(post_body, basestring):
                contents.append(post_body)
            else:
                contents = post_body
            contents = ' '.join(contents)
            raw_posts.append(contents + '\n')

            try:
                post = Post(post_url, post_title, post_body)
            except Exception as e:
                print e
                print post_body
            if post:
                posts.append(post.body + '\n')
            else:
                posts.append('\n')

        except Exception as e: 
            print "ERROR: " + str(e)
    return raw_posts, posts


"""
def load(path):

    if not path:
        return None

    pn_file = open(path, 'rU')
    raw = json.load(pn_file)
    pn_file.close()
    hits = raw['hits']['hits']

    # data[0]: pid, used inside program
    # data[1]: sid, unique id for original data
    # data[2]: content, original content of data, \t\n\r should be removed
    # data[3]: extraction (tokens), split by space, extracted from original content
    # data[4]: checksum? dup data?
    dataset = []

    for i, hit in enumerate(hits[:10]):
        pid = i + 1
        try:
            sid = hit[ES_POST_ID]
            source = hit[ES_POST_SOURCE]
            post_url, post_title, post_body = None, None, None

            if ES_POST_BODY not in source:
                dataset.append('\n')
                continue

            post_url = source[ES_POST_URL]
            post_title = source[ES_POST_TITLE][ES_POST_TEXT]
            post_body = extract_content_from_post_body(source[ES_POST_BODY][ES_POST_TEXT])

            try:
                post = Post(post_url, post_title, post_body)
            except Exception as e:
                print e
                print post_body

            if post:
                dataset.append(post.body + '\n') # + '\n'
            else:
                dataset.append('\n')
        except Exception as e: 
            print "ERROR: " + str(e)
            # print hit
            # print 'hasBodyPart' in source
    return dataset
"""

"""
# if ES_POST_SOURCE not in hit:
#     # this hit contains nothing
#     posts.append('\n')
#     continue

# if ES_POST_URL not in source:
#     continue

# if ES_POST_TITLE not in source:
#     continue

"""
