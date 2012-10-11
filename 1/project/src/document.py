# -*- coding: utf-8 -*-

import nltk
from nltk.stem.lancaster import LancasterStemmer
from bs4 import BeautifulSoup as bs

class Document():
    """
    Document class:

    """
    
    def __init__(self, filename="cranfield0001", lowercase=False, stem=False, stopwords=False):
        self._f      = open(filename,'r')
        self._tree   = bs(self._f.read())

        self._id     = int(self._tree.docno.string)
        self._title  = self._tree.title.string
        self._biblio = self._tree.biblio.string
        self._text   = self._tree.text.lower()
        st = LancasterStemmer()
        self._tokens = [st.stem(x) for x in  nltk.tokenize.word_tokenize(self._text)]
        self._f.close()
        
    def text(self):
        return self._text
