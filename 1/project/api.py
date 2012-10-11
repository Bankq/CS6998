# -*- coding: utf-8 -*-

#==================================
# api.py
#     Providing a high level api
#     for outer callings(index,query
#     etc.).
#==================================

import os
import nltk

from src.index import Index
from src.document import Document


def setup_index(index_dir="./raw_data/cranfieldDocs/"):
    """ Setup index """
    index = Index(index_dir)
    return index

def get(terms,index):
    doc_list = []

    for term in terms:
        if is_phrase_term(term):
            tmp_list = get_phrase_term_doc_list(term,index)
        elif is_negated_term(term):
            tmp_list = get_negated_term_doc_list(term,index)
        else:
            tmp_list = get_plain_term_doc_list(term,index)
        for tmp_item in tmp_list:
            flag = True
            for item in doc_list:
                if item['docid'] == tmp_item['docid']:
                    item['score'] += tmp_item['score']
                    item['snippet'] += tmp_item['snippet']
                    flag = False
                    break
            if flag:
                # not add to doc_list yet
                doc_list.append({'docid':tmp_item['docid'],'snippet':tmp_item['snippet'],'score':tmp_item['score']})

    if len(doc_list) == 0:
        return "Nothing..."

    result_list = sorted(doc_list,key=lambda k: k['score'],reverse=True)
    result = ''
    for item in result_list:
        result += str(item['docid']) + '\t'+ item['snippet'] + '\n'

    return result
        
def get_plain_term_doc_list(term,index):
    tmp_list = []
    d = index.get_token(term)
    for i in d:
        tmp_list.append({'docid':i['docid'],'snippet':get_snippet(i['docid'],term,index),'score':i['freq']})
    return tmp_list
        
def get_negated_term_doc_list(term,index):
    term = term[1:]
    tmp_list = []
    d = index.get_token(term)
    id_list = [item['docid'] for item in d]
    for i in range(1,index.number_of_docs()+1):
        if not i in id_list:
            tmp_list.append({'docid':i,'snippet':"...",'score':0})
    return tmp_list

def get_phrase_term_doc_list(term,index):
    term = term[1:-1]
    tmp_list = []
    cnt = len(term.split())
    for i in range(1,index.number_of_docs()+1):
        freq = index._doc_contents[i].count(term)
        if freq > 0:
            tmp_list.append({'docid':i,'snippet':get_snippet(i,term,index),'score':cnt*freq})
    return tmp_list
        

def get_title(docid,index):
    if docid in index._titles:
        return index._titles[docid]
    return "Not Found"

def get_doc(docid,index):
    if docid in index._doc_contents:
        return index._doc_contents[docid]
    return "Not Found"

def get_similar_list(term,index):
    doc_list = index.get_token(term)
    result = []
    for item in doc_list:
        text = nltk.text.ContextIndex(nltk.word_tokenize(index._doc_contents[item['docid']]))
        simi_list = text.similar_words(term)
        if len(simi_list) > 0:
            for i in simi_list:
                result.append(i)

    return result
        
                                   
        
def get_tf(docid,term,index):
    if is_phrase_term(term):
        return "Not valid term"
    else:
        if docid in index._doc_contents:
            doc = nltk.Text(nltk.word_tokenize(index._doc_contents[docid]))
            col = nltk.TextCollection([doc])
            return col.tf(term,doc)
        else:
            return "Not Found"

def get_df(term,index):
    if is_phrase_term(term):
        return get_df_phrase_term(term,index)
    else:
        return len(index.get_token(term))

def get_df_phrase_term(term,index):
    return len(filter(lambda x:term[1:-1] in x,[doc for doc in index._doc_contents.values()]))

def get_freq(term,index):
    if is_phrase_term(term):
        return get_freq_phrase_term(term,index)
    else:
        return sum([x["freq"] for x in index.get_token(term)])

def get_freq_phrase_term(term,index):
    return sum([doc.count(term[1:-1]) for doc in index._doc_contents.values()])

def get_snippet(docid,term,index):
    text = index._doc_contents[docid]
    length = len(text)
    pos = text.find(term)
    if pos == -1:
        return '.'
    if pos > 10:
        start = pos - 10
    else:
        start = 0
    if pos + 10 < length:
        end = pos + 10
    else:
        end = length
    return "..."+' '.join(text[start:end].split('\n'))+"..."


def is_phrase_term(term):
    return term[0] == '\"' and term[-1] == '\"'

def is_negated_term(term):
    return term[0] == '!'
