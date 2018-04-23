import json
import gzip
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import linalg as LA
import json
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
import nltk.stem
from nltk.corpus import stopwords




def tokenize(text):
    """Returns a list of words that make up the text.
    
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    
    Params: {text: String}
    Returns: Array
    """
    lowertext = text.lower()
    
    tokens = re.findall(r'[a-z]+', lowertext)
    return tokens



def unpickle(fileNames):
 	file = open(fileNames[0],'rb')
	index_to_vocab = pickle.load(file)
	file.close()
	file = open(fileNames[1],'rb')
	vocab_to_index = pickle.load(file)
	file.close()
	file = open(fileNames[2],'rb')
	ind_to_title = pickle.load(file)
	file.close()
	file = open(fileNames[3],'rb')
	ind_to_price = pickle.load(file)
	file.close()
	file = open(fileNames[4],'rb')
	ind_to_rating = pickle.load(file)
	file.close()
	file = open(fileNames[5],'rb')
	doc_by_vocab = pickle.load(file)
	file.close()
	return index_to_vocab, vocab_to_index,ind_to_title,ind_to_price,ind_to_rating,doc_by_vocab
n_feats = 5000

index_to_vocab, vocab_to_index,ind_to_title,ind_to_price, ind_to_rating, doc_by_vocab = unpickle(['/Users/claire/Desktop/final/cs4300sp2018-crl95-cfz8-jp884-kl769-yt338/ind_to_vocab.pickle','/Users/claire/Desktop/final/cs4300sp2018-crl95-cfz8-jp884-kl769-yt338/vocab_to_indx.pickle','/Users/claire/Desktop/final/cs4300sp2018-crl95-cfz8-jp884-kl769-yt338/ind_to_title.pickle',
                           '/Users/claire/Desktop/final/cs4300sp2018-crl95-cfz8-jp884-kl769-yt338/ind_to_price.pickle', '/Users/claire/Desktop/final/cs4300sp2018-crl95-cfz8-jp884-kl769-yt338/ind_to_rating.pickle','/Users/claire/Desktop/final/cs4300sp2018-crl95-cfz8-jp884-kl769-yt338/doc_by_vocab.pickle'])


def vectorize_query(query):
    vector = np.empty(n_feats)
    ss = SnowballStemmer('english')
    tokens = nltk.word_tokenize(query)
    tokens = [ss.stem(i) for i  in tokens]
    stop_words = set(stopwords.words('english'))
    for i in tokens:
        if i in stop_words:
            continue
        elif i in vocab_to_index:
            index = vocab_to_index[i]
            vector[index] += 1

    return vector




def get_sim(query, vec):
    return np.dot(query, vec )/(LA.norm(query)*LA.norm(vec))
def calc_sort (matrix,query ):
    try :
        vector = vectorize_query(query)
        res = cosine_similarity(vector, matrix).reshape(-1)


        arg_sort_array = np.argsort(res)[::-1][:5]
        return [ind_to_title[i] for i in arg_sort_array] , [ind_to_price[i] for i in arg_sort_array], [ind_to_rating[i] for i in arg_sort_array]
    except ValueError:
        return [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]