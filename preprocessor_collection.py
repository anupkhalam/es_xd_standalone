#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 10:31:44 2018

@author: anup
"""

pre_processor_01 = {'preprocessor': [
    {'name':'tokenizer','param':[{'tokenizer':'word_tokenize'}]},
    {'name':'stemmer','param':[{'stemmer':'PorterStemmer'}]},
    {'name':'joiner','param':[{'joiner':'&&&&'}]},
    {'name':'replacer','param':[{'replacer':['the','$$$']},
    {'replacer':['assumption','asssssssssumption']}]}]}


pre_processor_02 = {'preprocessor': [
    {'name':'splitjoiner','param':[{'splitjoiner':None}]}]}


pre_processor_03 = {'preprocessor': [
    {'name':'splitjoiner','param':[{'splitjoiner':None}]},
    {'name':'caseconverter','param':[{'type':'lower'}]}
    ]}


pre_processor_04 = {'preprocessor': [
    {'name':'splitjoiner','param':[{'splitjoiner':None}]},
    {'name':'caseconverter','param':[{'type':'upper'}]}
    ]}
