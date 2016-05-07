
import json
from wedc.domain.entities.post import Post

ES_POST_SOURCE = '_source'
ES_POST_URL = 'url'
ES_POST_TITLE = 'hasTitlePart'
ES_POST_BODY = 'hasBodyPart'
ES_POST_TEXT = 'text'


def load(path):

    if not path:
        return None

    pn_file = open(path, 'rU')
    raw = json.load(pn_file)
    pn_file.close()
    hits = raw['hits']['hits']
    posts = []
    

    for hit in hits[:1000]:
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

            try:
                post = Post(post_url, post_title, post_body)
            except Exception as e:
                print e
                print post_body

            if post:
                posts.append(post.body + '\n') # + '\n'
            else:
                posts.append('\n')
        except Exception as e: 
            print "ERROR: " + str(e)
            # print hit
            # print 'hasBodyPart' in source
    return posts
    

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

    contents = []
    if isinstance(text, basestring):
        contents.append(text)
    else:
        contents = text
    text = ' '.join(contents) 

    post = Post('', '', text)
    return text, post


