#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 13:23:43 2018

@author: anup
"""
from preprocess_methods import *


class EsPreProcessor(object):
    def __init__(self, es_corpus_data = None, es_preprocessor = None):
        self.es_corpus_data = es_corpus_data
        self.preprocessed_corpus = es_corpus_data
        self.es_preprocessor = es_preprocessor
        self.es_pre_processed_corpus = self.assemble_preprocessor()
        
    
    @classmethod
    def es_preprocessor_manager(cls, es_corpus_data, es_preprocessor):
        es_corpus_data, es_preprocessor = es_corpus_data, es_preprocessor['preprocessor']
        es_preprocessor_instance = cls(es_corpus_data, es_preprocessor)
        return es_preprocessor_instance
    
    
    def assemble_preprocessor(self):
        for preprocessor in self.es_preprocessor:
            self.preprocessed_corpus = self.get_preprocessed_corpus(preprocessor)
        return self.preprocessed_corpus


    def get_preprocessed_corpus(self, preprocessor):
        preprocessor_name = preprocessor['name']
        preprocessor_parameter = preprocessor['param']
        self.preprocessed_corpus = eval(preprocessor_name)(self.preprocessed_corpus,preprocessor_parameter)
        return self.preprocessed_corpus
        
    