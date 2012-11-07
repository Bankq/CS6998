# -*- coding: utf-8 -*-
import csv
from nltk import word_tokenize
from nltk import PorterStemmer
from nltk.util import bigrams
from nltk.corpus import PlaintextCorpusReader

data_root = "./data"
stop_set = PlaintextCorpusReader(data_root,'.*').words('english')

class Document():
	"""Read information from a csv file"""
	def __init__(self, file_path="./data/train.csv",data_catagory="train",do_stopwords=False,do_stemming=True,use_bigrams=False):
		self.file_path = file_path
		self.data_catagory = data_catagory
                self.model = []
                if data_catagory == "train":
                        with open(file_path,"rb") as self.file:
                                self.reader = csv.reader(self.file)
                                self.coln = len(self.reader.next())
                                self.model = [{"label":row[0],"features":self.tokenize(row[1],do_stopwords,do_stemming,use_bigrams)} for row in self.reader]
                else:
                        with open(file_path,"rb") as self.file:
                                self.reader = csv.reader(self.file)
                                self.coln = len(self.reader.next())
                                self.model = [self.tokenize(row[0],do_stopwords,do_stemming,use_bigrams) for row in self.reader]
                                

        def tokenize(self, sentence, do_stopwords, do_stemming,use_bigrams):
                words = word_tokenize(sentence)
                words = [w.lower() for w in words if len(w) > 2]
                if do_stopwords:
                        words = [w for w in words if w not in stop_set]
                if do_stemming:
                        stemmer = PorterStemmer()
                        words = [stemmer.stem(w) for w in words]
                if use_bigrams:
                        words = bigrams(words)
                return words

        def output(self):
                for row in self.model:
                        print row
