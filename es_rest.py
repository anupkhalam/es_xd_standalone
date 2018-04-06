#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 10:25:36 2018

@author: anup
"""

from flask import Flask, jsonify, request
from html_indexer import *
import uuid
from pymongo import MongoClient
global corp_output


# initialize Mongo Client
mongoclient = MongoClient('localhost', 27017)
db = mongoclient.esdatabase
esdocs = db.posts


# initialize flask
app = Flask(__name__)
corp_output = ['Welcome!']


@app.route('/espush')
def get_incomes():
    return corp_output[-1]


@app.route('/espush', methods=['POST'])
def es_push():
    es_input_json = request.get_json()
    corpus_status = es_input_json['corpus_status']
    process_output = eval(corpus_status + '_corpus_process')(es_input_json)
    corp_output.append(process_output)
    return '', 204


def new_corpus_process(new_corpus_json):
    corpus_key = uuid.uuid4().hex
    new_corpus_json['_id'] = corpus_key
    corpus_key_loaded = esdocs.insert_one(new_corpus_json).inserted_id
    es_index_create(new_corpus_json['files_location'], 
                    new_corpus_json['index_1_names'],
                    new_corpus_json['pre_processor'])
    return "Successful"

    
def upd_corpus_process(upd_corpus_json):
    upd_corpus_dict = {key:upd_corpus_json[key] for key in upd_corpus_json if key != "_id"}
    esdocs.update_one({"_id": upd_corpus_json["_id"]},{"$set": upd_corpus_dict}, upsert=False)
    return "Successful"


if __name__ == '__main__':
    app.run(debug=True)


