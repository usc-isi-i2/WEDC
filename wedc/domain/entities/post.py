from wedc.domain.core.data import parser

class Post(object):

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = self.parse_body_word(body)

    def parse_body_word(self,body):
        contents = []
        if isinstance(body, basestring):
            contents.append(body)
        else:
            contents = body
        return parser.parse(' '.join(contents))
