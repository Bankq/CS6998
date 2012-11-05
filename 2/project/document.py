# -*- coding: utf-8 -*-
import csv
from nltk import word_tokenize
from nltk.corpus import PlaintextCorpusReader

data_root = "./data"
stop_set = PlaintextCorpusReader(data_root,'.*').words('english')

class Document():
	"""Read information from a csv file"""
	def __init__(self, file_path="./data/train.csv",data_catagory="train"):
		self.file_path = file_path
		self.data_catagory = data_catagory
                self.model = []
                if data_catagory == "train":
                        with open(file_path,"rb") as self.file:
                                self.reader = csv.reader(self.file)
                                self.coln = len(self.reader.next())
                                self.model = [{"label":row[0],"features":self.tokenize(row[1])} for row in self.reader]
                else:
                        with open(file_path,"rb") as self.file:
                                self.reader = csv.reader(self.file)
                                self.coln = len(self.reader.next())
                                self.model = [self.tokenize(row[0]) for row in self.reader]
                                

        def tokenize(self, sentence, do_stopwords=False, do_stemming=False,do_chisquare=False):
                words = word_tokenize(sentence)
                words = [w for w in words if len(w) > 2]
                if do_stopwords:
                        words = [w.lower().strip() for w in words if w not in stop_set and len(w.strip()) > 2]
                return words

        def output(self):
                for row in self.model:
                        print row
