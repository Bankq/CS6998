import shelve
from .src.document import Document

def naive_bayes(input_path="./data/train.csv", output_path="./data/naive_bayes_model"):
    """
    input_path: file contains raw_data (.csv)
    output_path: model info after trainning
    """
    d = Document(input_path)

    num_doc = len(d.model)
    num_labels = 2 # hard coded
    num_pos = 0 # num of document that has label 1
    num_neg = 0 # num of doucment that has label 0
    num_words_in_pos = 0 # total number of words in label 1
    num_words_in_neg = 0 # total number of words in label 0
    word_freq_pos = {} # word frequency in labeled 1 documents
    word_freq_neg = {} # word frequency in labeled 0 documents
    for doc in d.model:
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
        

    shelf = shelve.open(output_path)
    shelf["classifier"] = "NaiveBayes"
    shelf["model"] = model
    shelf.close()
    
    
