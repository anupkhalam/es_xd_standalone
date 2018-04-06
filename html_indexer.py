#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:27:48 2018

@author: anup
"""


from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup as BS
import glob
from preprocess_class import EsPreProcessor
import warnings
from html_processing import *
warnings.filterwarnings('ignore')
from preprocessor_collection import *


def es_index_create(files_location,                                 # location of html files
                    index_1_params,                                 # name of index 1
                    pre_processor):                                 # preprocessor
    file_list = glob.glob(files_location + '/*.html')
    file_names = [filename.split("/")[-1][:-5] for filename in file_list]
    # this should come as an argument or from db
    headers_list = ['h1','h2']


    # create index in elasticsearch with necessary field limit
    es = Elasticsearch()                                            # initialize elasticsearch
    doc = {"settings": {"index.mapping.total_fields.limit": 10000}} # setting the field limit
    es.indices.create(index = index_1_params[0], body = doc)

    es_doc_id = 0
    for file_no in range(len(file_list)):
        with open(file_list[file_no]) as f:
            temp_html_file = [line.rstrip() for line in f]
            html_file = ''
            html_strip_file = ''
            for line in temp_html_file:
                html_file += (line + '\n')
                html_strip_file += (line)
            html = html_strip_file

        # extract whole html
        section_dict_full_html = html_extraction(html_file)

        # extract whole text from html
        section_dict_full_text = text_extraction(BS(html))
        
        # extract contents under the headers
        section_dict_headers_contents = header_content_extraction(html,headers_list,file_names[file_no])

        # assembling contents for the index
        section_dict_1 = {**section_dict_full_text, **section_dict_headers_contents}

        for key, value in section_dict_1.items():
            section_dict_1[key] = EsPreProcessor.es_preprocessor_manager(value, pre_processor).es_pre_processed_corpus

        for key, value in section_dict_1.items():
            es_doc_id += 1
            es_update_dict = {}
            es_update_dict[key] = value
            es.index(index=index_1_params[0], doc_type=index_1_params[1], id=es_doc_id, body = es_update_dict)


def es_search_processor(es_sch_doctype, 
                        es_searcearch_index, 
                        es_searh_body):
    es_search = Elasticsearch()
    es_user_query_search_result = es_search.search(index = es_search_index,
                                            doc_type = es_search_doctype,
                                            body = es_search_body)
    return es_user_query_search_result


