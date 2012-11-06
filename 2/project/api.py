import shelve
import random
import copy
from .document import Document

def naive_bayes(input_path="./data/train.csv", output_path="./data/naive_bayes_model"):
    """
    input_path: file contains raw_data (.csv)
    output_path: model info after trainning
    """
    d_with_stopwords = Document(input_path)
    d_without_stopwords = Document(input_path,"train",True)
    shelf = shelve.open(output_path)
    shelf["classifier"] = "NaiveBayes"
    # shelf["models"] = [naive_bayes_train_model(d.model,0.8) for i in range(7)]
    shelf["models"] = [naive_bayes_train_model(d_with_stopwords.model,1.0),
                       naive_bayes_train_model(d_with_stopwords.model,0.8),
                       naive_bayes_train_model(d_without_stopwords.model,1.0)]
    print len(shelf["models"])
    shelf.close()
    

def naive_bayes_train_model(all_docs,ratio):
    select = generate_select(len(all_docs),ratio)
    docs = [all_docs[docid] for docid in select]
    num_doc = len(docs)
    num_labels = 2 # hard coded
    num_pos = 0 # num of document that has label 1
    num_neg = 0 # num of doucment that has label 0
    num_words_in_pos = 0 # total number of words in label 1
    num_words_in_neg = 0 # total number of words in label 0
    word_freq_pos = {} # word frequency in labeled 1 documents
    word_freq_neg = {} # word frequency in labeled 0 documents
    for doc in docs:
        if doc["label"] == '1':
            num_pos += 1
            for feature in doc["features"]:
                num_words_in_pos += 1
                if feature in word_freq_pos:
                    word_freq_pos[feature] += 1
                else:
                    word_freq_pos[feature] = 1
        else:
            num_neg += 1
            for feature in doc["features"]:
                num_words_in_neg += 1
                if feature in word_freq_neg:
                    word_freq_neg[feature] += 1
                else:
                    word_freq_neg[feature] = 1

    model = {}
    model["num_doc"] = num_doc
    model["num_pos"] = num_pos
    model["num_neg"] = num_neg
    model["num_words_in_pos"] = num_words_in_pos
    model["num_words_in_neg"] = num_words_in_neg
    model["word_freq_pos"] = word_freq_pos
    model["word_freq_neg"] = word_freq_neg
    
    return model
    
def generate_select(n,r):
    if int(n*r) > 1:
        l = [i for i in range(n)]
        random.shuffle(l)
        l = l[0:(int(n*r)-1)]
        return l
    else:
        return []
        
