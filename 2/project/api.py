import math
import shelve
import random
import copy

from .document import Document

def naive_bayes(input_path="./data/train.csv", output_path="./data/naive_bayes_model"):
    """
    input_path: file contains raw_data (.csv)
    output_path: model info after trainning
    """

    shelf = shelve.open(output_path)
    shelf["classifier"] = "NaiveBayes"

    # d = Document(input_path,"train",do_stopwords=False,do_stemming=True,use_bigrams=False)
    d1 = Document(input_path,"train",do_stopwords=False,do_stemming=False,use_bigrams=False)
    d2 = Document(input_path,"train",do_stopwords=False,do_stemming=True,use_bigrams=False)
    d3 = Document(input_path,"train",do_stopwords=True,do_stemming=True,use_bigrams=False)
    d4 = Document(input_path,"train",do_stopwords=False,do_stemming=False,use_bigrams=False) 
    d5 = Document(input_path,"train",do_stopwords=False,do_stemming=True,use_bigrams=False) 
    # shelf["models"] = [naive_bayes_train_model(d.model,1.0,1.0) for i in range(1)]
    shelf["models"] = [naive_bayes_train_model(d1.model,0.9,1.0),
                       naive_bayes_train_model(d2.model,0.9,1.0),
                       naive_bayes_train_model(d3.model,1.0,1.0),
                       naive_bayes_train_model(d4.model,0.9,0.0),
                       naive_bayes_train_model(d5.model,0.9,0.9)]
    print len(shelf["models"])
    shelf.close()

def naive_bayes_train_model(all_docs,ratio,chi_square_ratio):
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

    result_model = chi_square_test(model,chi_square_ratio) # do chi-square test to select features
    return result_model
    
def chi_square_test(model,ratio=1):
    word_freq_pos = model["word_freq_pos"]
    word_freq_neg = model["word_freq_neg"]
    pos_words = set([w for w in word_freq_pos.keys()])
    neg_words = set([w for w in word_freq_neg.keys()])
    words = pos_words.union(neg_words) # words set
    chi_square = {}
    for word in words:
        A = word_freq_pos[word] if word in word_freq_pos else 1
        B = word_freq_neg[word] if word in word_freq_neg else 1
        C = model["num_pos"] - A
        D = model["num_neg"] - B
        chi_square[word] = ((A*D - B*C)*(A*D - B*C))/float((A+B)*(C+D))
    
    select_words = list((sorted(chi_square,key=chi_square.__getitem__)))
    
    max_diff = 0.0
    split = 0
    for i in range(1,len(select_words)):
        diff = (chi_square[select_words[i]]-chi_square[select_words[i-1]])/chi_square[select_words[i-1]]
        if diff > max_diff:
            max_diff = diff
            split = i
        
    if ratio != 0.0:
        split = int(len(words)*(1-ratio))
    
    for i in range(split):
        if select_words[i] in word_freq_pos:
            model["num_words_in_pos"] -= word_freq_pos[select_words[i]]
        if select_words[i] in word_freq_neg:
            model["num_words_in_neg"] -= word_freq_neg[select_words[i]]

    model["select_words"] = select_words[split:]
    return model
        
                       

def generate_select(n,r):
    if int(n*r) > 1:
        l = [i for i in range(n)]
        random.shuffle(l)
        l = l[0:(int(n*r)-1)]
        return l
    else:
        return []
        

def bayes_bagging(models,instance):
    pos_count = 0
    neg_count = 0
    for model in models:
        if bayes_classify(model,instance) == '1':
            pos_count += 1
        else: 
            neg_count += 1
    # threshold = float(pos_count/(pos_count + neg_count)) # with some randomness (turn out to be not working well)
    # return '1' if random.random() < threshold else '0'
    return '1' if pos_count > neg_count else '0'


def bayes_classify(model,instance):
    p_pos = math.log(model["num_pos"]/float(model["num_doc"]))
    p_neg = math.log(model["num_neg"]/float(model["num_doc"]))
    p_word_pos = 0.0
    p_word_neg = 0.0
    total_words_pos = model["num_words_in_pos"]
    total_words_neg = model["num_words_in_neg"]
    total_different_words_pos = len(model["word_freq_pos"])
    total_different_words_neg = len(model["word_freq_neg"])
    for word in instance:
        if word in model["select_words"]:
            if word in model["word_freq_pos"]:
                p_word_pos += math.log((1.0+model["word_freq_pos"][word])/float(total_words_pos+total_different_words_pos))
            else:
                p_word_pos += math.log(1.0/(total_words_pos + total_different_words_pos))
                
            if word in model["word_freq_neg"]:
                p_word_neg += math.log((1.0+model["word_freq_neg"][word])/float(total_words_neg+total_different_words_neg))
            else:
                p_word_neg += math.log(1.0/(total_words_neg + total_different_words_neg))

    return '1' if (p_pos + p_word_pos) > (p_neg + p_word_neg) else '0'
