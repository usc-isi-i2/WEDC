
import json
from wedc.domain.entities.post import Post

ES_POST_SOURCE = '_source'
ES_POST_URL = 'url'
ES_POST_TITLE = 'hasTitlePart'
ES_POST_BODY = 'hasBodyPart'
ES_POST_TEXT = 'text'


def load(path):
    posts = post_parser(path)
    # posts = [_.body for _ in posts]
    return posts
    # print posts
    

def load_post(path, post_id):
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
    post = Post('', '', text)

    contents = []
    if isinstance(text, basestring):
        contents.append(text)
    else:
        contents = text
    text = ' '.join(contents)

    
    # print 'original text:\n\n', text, '\n\n
    
    return text, post


def post_parser(path):
    if not path:
        return None
    # filename = 'san-francisco-maria.json'
    # path = os.path.join(__elastic_search_dir__, filename)
    pn_file = open(path, 'rU')
    raw = json.load(pn_file)
    pn_file.close()
    hits = raw['hits']['hits']
    posts = []
    # test = 0    # test
    # print len(hits)
    # post_id = 0
    for hit in hits:
        try:
            source = hit[ES_POST_SOURCE]
            post_url, post_title, post_body = None, None, None
            # if ES_POST_SOURCE not in hit:
            #     # this hit contains nothing
            #     posts.append('\n')
            #     continue

            # if ES_POST_URL not in source:
            #     continue

            # if ES_POST_TITLE not in source:
            #     continue

            if ES_POST_BODY not in source:
                posts.append('\n')
                continue

            post_url = source[ES_POST_URL]
            post_title = source[ES_POST_TITLE][ES_POST_TEXT]
            post_body = source[ES_POST_BODY][ES_POST_TEXT]

            post = Post(post_url, post_title, post_body)
            if post:
                posts.append(post.body + '\n') # + '\n'
            else:
                posts.append('\n')
                # post_id+=1 # str(post_id) + ' ' + 
            # break   # test one doc this time
            # test += 1
            # if test == 2000:
            # break

        except Exception as e: 
            print "ERROR: " + str(e)
            # print hit
            # print 'hasBodyPart' in source
    return posts