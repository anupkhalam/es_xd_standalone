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
                    index_1_names,                                  # name of index 1
                    index_2_names,                                  # name of index 2
                    pre_processor):                                 # preprocessor
    file_list = glob.glob(files_location + '/*.html')
    # this should come as an argument or from db
    headers_list = ['h1','h2','h3','h4','h5']


    # create index in elasticsearch with necessary field limit
    es = Elasticsearch()                                            # initialize elasticsearch
    doc = {"settings": {"index.mapping.total_fields.limit": 10000}} # setting the field limit
    es.indices.create(index = index_1_names[0], body = doc)
    es.indices.create(index = index_2_names[0], body = doc)


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
        
        # extract user-specified header levels
        section_dict_headers = header_extraction(BS(html), headers_list)

        # extract contents under the headers
        section_dict_headers_contents = header_content_extraction(html, headers_list)

        # assembling contents for the first index
        section_dict_1 = {**section_dict_headers, **section_dict_full_html}

        # assembling contents for the second index
        section_dict_2 = {**section_dict_full_text, **section_dict_headers_contents}

        for key, value in section_dict_2.items():
            section_dict_2[key] = EsPreProcessor.es_preprocessor_manager(value, pre_processor).es_pre_processed_corpus

        es.index(index=index_1_names[0], doc_type=index_1_names[1], id=(file_no + 1), body = section_dict_1)
        es.index(index=index_2_names[0], doc_type=index_2_names[1], id=(file_no + 1), body = section_dict_2)


def es_search_processor(es_sch_doctype, 
                        es_searcearch_index, 
                        es_searh_body):
    es_search = Elasticsearch()
    es_user_query_search_result = es_search.search(index = es_search_index,
                                            doc_type = es_search_doctype,
                                            body = es_search_body)
    return es_user_query_search_result


