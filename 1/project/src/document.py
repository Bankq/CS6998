# -*- coding: utf-8 -*-
##================================================
##             Document class
##   CS6998 - Search Engine Technology 
##   Columbia University
##   Author: Hang Qian
##  
##   A Document object takes a XML file and retrieve
##   the inside information.
##================================================
import nltk
from nltk.stem.lancaster import LancasterStemmer
from bs4 import BeautifulSoup as bs

class Document():
    """
    """
    
    def __init__(self, filename="cranfield0001", lowercase=False, stem=False, stopwords=False):
        self._f      = open(filename,'r')
        self._tree   = bs(self._f.read())

        self._id     = int(self._tree.docno.string)
        self._title  = self._tree.title.string
        self._biblio = self._tree.biblio.string
        self._text   = self._tree.text.lower()
        st = LancasterStemmer()
        # stem the token
        self._tokens = [st.stem(x) for x in  nltk.tokenize.word_tokenize(self._text)]
        self._f.close()
        
    def text(self):
        return self._text
