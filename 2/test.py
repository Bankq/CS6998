#!/usr/bin/env python

import sys
import csv
import shelve
import math

from project.src.document import Document

def main(model_file_path,test_file_path,prediction_file_path):
    with open(prediction_file_path,"w") as prediction_file:
        test_list = Document(test_file_path, "test").model
        shelf = shelve.open(model_file_path)
        if shelf["classifier"] == "NaiveBayes":
            for instance in test_list:
                label = bayes_classify(shelf["model"],instance)
                prediction_file.write(label+"\n")
        shelf.close()


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
        if word in model["word_freq_pos"]:
            p_word_pos += math.log((1.0 + model["word_freq_pos"][word])/(total_words_pos + total_different_words_pos))
        else:
            p_word_pos += math.log(1.0/(total_words_pos + total_different_words_pos))

        if word in model["word_freq_neg"]:
            p_word_neg += math.log((1.0 + model["word_freq_neg"][word])/(total_words_neg + total_different_words_neg))
        else:
            p_word_neg += math.log(1.0/(total_words_neg + total_different_words_neg))

    return '1' if (p_pos + p_word_pos) > (p_neg + p_word_neg) else '0'


if __name__ == '__main__':
    model_file_path = sys.argv[1]
    test_file_path = sys.argv[2]
    prediction_file_path = sys.argv[3]
    main(model_file_path, test_file_path, prediction_file_path)
        
