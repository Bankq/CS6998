# -*- coding: utf-8 -*-

import shelve
import nose
from .document import Document
from .index import Index

def test_index():
    # shelf = shelve.open("./shelve")
    # shelf["index_obj"] = Index()
    # shelf.close()
    # shelf = shelve.open("./shelve")
    # index = shelf["index_obj"]
    # num = index.number_of_docs()
    # shelf.close()
    # assert len(index._filenames) == num
    index = Index("./raw_data_test/")
    # index= Index()
    index.setup()
    print float(len(index.get_token("is")))/index._num_of_docs
    



        
