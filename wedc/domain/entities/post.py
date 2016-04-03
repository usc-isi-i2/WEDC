
from nltk.tokenize import sent_tokenize
from wedc.domain.core.common import str_helper


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
            sentences.extend([sentence for sentence in sent_tokenize(content) if not str_helper.hasHTMLTag(sentence)])
        
        return sentences
            

# post = Post('url', 'title', ['body','body'])

# print post.body



