
import re
import string

from nltk.tokenize import sent_tokenize
from wedc.domain.core.common import str_helper
from nltk.tokenize import word_tokenize
from wedc.domain.vendor.nltk import stopword
from wedc.domain.vendor.nltk import stem
from wedc.domain.core.http import domain



def remove_tags(text):
    tag_re = re.compile(r'<[^>]+>')
    return tag_re.sub('', text)

def remove_url(text):
    domain_ext_list = domain.get_domain_ext_list()
    text = text.lower()
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    text = re.sub(r'^[a-z0-9\-\.]+\.('+'|'.join(domain_ext_list)+')$', '', text)
    return text

def has_url(text):
    domain_ext_list = domain.get_domain_ext_list()
    text = text.lower()
    if re.search(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', text):
        return True
    if re.search(r'[a-z0-9\-\.]+\.('+'|'.join(domain_ext_list)+')', text):
        return True
    return False

def valid_digit(text):
    """ judge if the token is valid with digit

 
    """
    if re.search(r'^/d*$', text):
        return False
    return True


class Post(object):

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = self.parse_body_word(body)

    def initialize(self):
        """ initialize main conent of doc
        """
        pass

    def parse_body_word(self,body):
        contents = []
        if isinstance(body, basestring):
            contents.append(body)
        else:
            contents = body

        sentences = []
        for content in contents:
            sentences.extend([self.sentence_operation(sentence) for sentence in sent_tokenize(content)])
        # print sentences
        sentences = ' '.join(sentences)


        stop = stopword.get_stopwords()
        tokens = []
        for token in word_tokenize(sentences):
            if token not in stop and not str_helper.hasPunctuation(token) and not has_url(token):
                # and not str_helper.hasNumbers(token) 
                token = token.encode('ascii', 'ignore')
                token = stem.stemming(token)
                token = str(token)
                tokens.append(token)

        # tokens = [str(stem.stemming(token.encode('ascii', 'ignore'))) for token in word_tokenize(sentences) if token not in stop and not str_helper.hasNumbers(token) and not str_helper.hasPunctuation(token)]

        ans = ' '.join(tokens).lower()
        return ans.strip()


    def parse_body_sentence(self, body):
        contents = []
        if isinstance(body, basestring):
            contents.append(body)
        else:
            contents = body

        sentences = []
        for content in contents:
            sentences.extend([self.sentence_operation(sentence) for sentence in sent_tokenize(content)])

        # if not str_helper.hasHTMLTag(sentence)
        # encode('utf-8').splitlines()
        return ' '.join(sentences) + '\n'

    def sentence_operation(self, sentence):
        sentence = remove_tags(sentence)
        sentence = remove_url(sentence)
        sentence = re.sub(r'[\t\n\r]', ' ', sentence)
        # sentence = ' '.join(sentence.encode('utf-8').splitlines())
        return sentence



            

# post = Post('url', 'title', ['body','body'])

# print post.body
# text ='</p><p> JO-1408-61357<p><br> Contact: Neal Fenster<br> Email: ...@enterprisemed.com<br> Phone: 1-800-###-####<br> Web: www.enterprisemed.com</p>'
# print remove_tags(text)


