
# from nltk.tokenize import sent_tokenize
# from wedc.domain.core.common import str_helper


class Post(object):

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = self.parse_body(body)

    def initialize(self):
        """ initialize main conent of doc
        """
        pass


    def parse_body(self, body):
        contents = []
        if isinstance(body, basestring):
            contents.append(body)
        else:
            contents = body

        sentences = []
        for content in contents:
            sentences.extend([sentence.encode('utf-8').splitlines() for sentence in sent_tokenize(content)])

        # if not str_helper.hasHTMLTag(sentence)
        # encode('utf-8').splitlines()
        
        return sentences

    def sentence_operation(sentence):
        sentence = remove_tags(sentence)
        

import re
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)
            

# post = Post('url', 'title', ['body','body'])

# print post.body
# text ='</p><p> JO-1408-61357<p><br> Contact: Neal Fenster<br> Email: ...@enterprisemed.com<br> Phone: 1-800-###-####<br> Web: www.enterprisemed.com</p>'
# print remove_tags(text)


