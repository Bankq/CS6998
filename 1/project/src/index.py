# -*- coding: utf-8 -*-

##================================================
##               Index class
##   CS6998 - Search Engine Technology 
##   Columbia University
##   Author: Hang Qian
##  
##
##   An Index object takes a collection of documents
##   then created a inverted index of words, and store
##   all the metadata we may need.
##================================================

import os
import sys
import shelve
from nltk.stem.lancaster import LancasterStemmer
from .document import Document


class Index():
    """
    Inverted Index
    """

    def __init__(self, filepath="./raw_data/cranfieldDocs/"):
        """
        Store all the meta data
        """

        self._filepath       = filepath
        self._filenames      = [f for f in os.listdir(self._filepath)]
        self._num_of_docs    = len(self._filenames)
        self._inverted_index = dict()
        self._titles         = dict()
        self._doc_contents   = dict()
        self._tokens         = []


        for i,filename in enumerate(self._filenames):
            # for all files in the given directory
            # we call Document class to handle the
            # standard XML representation and retrive
            # all the information we need
            d = Document(self._filepath+filename)
            docid = d._id
            self._titles[d._id] = d._title
            self._doc_contents[d._id] = d._text
            tokens = d._tokens
            for t in tokens:
                self._tokens.append(t)
            for token in tokens:
                self.add_token(token,docid)

            sys.stdout.write('\r['+str(i)+'/'+str(self._num_of_docs)+'] ')
            sys.stdout.flush()
            
    def add_token(self,token,docid):
        """
        Add a token to the inverted index
        """
        f = lambda x: x["docid"] == docid
        if token in self._inverted_index:
            doc_list = self._inverted_index[token]
            doc_items = filter(f,doc_list)
            if len(doc_items) != 0:
                # if already have a toke list
                # add the frequency
                doc_items[0]["freq"] += 1
            else:
                self._inverted_index[token].append(dict({"docid":docid,"freq":1}))
        else:
            self._inverted_index[token] = [dict({"docid":docid,"freq":1})]
    
    def get_token(self,token):
        """
        Get the document list of corresponding term
        """
        st = LancasterStemmer()
        token = st.stem(token)
        if token in self._inverted_index:
            return self._inverted_index[token]
        else:
            return {}
            
    def number_of_docs(self):
        return self._num_of_docs
    
