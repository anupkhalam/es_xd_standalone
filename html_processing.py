#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 16:00:08 2018

@author: anup
"""
from bs4 import BeautifulSoup as BS


def html_extraction(html):
    section_dict_full_html = {}
    section_dict_full_html['html_doc'] = html
    return section_dict_full_html



def text_extraction(soup):
    try:
        soup.find(lambda tag:tag.name == 'head' and tag.find(lambda t:t.name == 'style')).extract()
    except AttributeError:
        pass
    es_full_text = soup.get_text()
    section_dict_full_text = {}
    section_dict_full_text['Full Text'] = es_full_text
    return section_dict_full_text




def header_content_extraction(html,
                              headers_list,
                              file_name):

    section_dict = {}
    for header in range(len(headers_list)):
        soup = BS(html)
        header_tag = None
        header_tag = soup.find(headers_list[header])
        if header_tag is None:
            continue
        header_tag_list = []
        header_tag_list = header_tag.parent.findChildren(headers_list[header])
        if len(header_tag_list) == 0:
            continue
        for component_tag in header_tag_list:
            header_tag_siblings = component_tag.nextSiblingGenerator()
            header_tag_sibling_list = []
            header_tag_sibling_tag_list = []
            within_para_bold_tag_list = []
            for header_tag_sibling in header_tag_siblings:
                if header_tag_sibling.name in (headers_list[:(header + 1)]):
                    if header_tag_sibling_list:
                        section_dict['(' + 'File Name: ' + file_name + ')' + '***'+ '('  + 'File Section: ' + component_tag.get_text().replace('.','_') + ')'] = ' '.join(header_tag_sibling_list)
                    break
                try:
                    header_tag_sibling_tag_list.append(header_tag_sibling)
                    header_tag_sibling_list.append(header_tag_sibling.get_text())
                except AttributeError:
                    pass
            else:
                if header_tag_sibling_list:
                    section_dict['(' + 'File Name: ' + file_name + ')' + '***'+ '('  + 'File Section: ' + component_tag.get_text().replace('.','_') + ')'] = ' '.join(header_tag_sibling_list)
    
    return section_dict







    
    
        
        
    
            