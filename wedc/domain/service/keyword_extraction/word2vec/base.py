
import word2vec

word2vec_model = None



def load_word2vec_model(model_path):
    global word2vec_model
    word2vec_model = word2vec.load(model_path)

