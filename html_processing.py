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




def header_extraction(soup, headers_list):
    headers_indexing_list = []
    try:
        for headers_tag in headers_list:
            first_tag = soup.find(headers_tag)
            tag_list=first_tag.parent.findChildren(headers_tag)
            headers_indexing_list.extend(tag_list)
    except AttributeError:
        pass
    headers_indexing_list = [i.get_text() for i in headers_indexing_list if i is not None]
    section_dict_headers_list = {}
    section_dict_headers_list["headers"] = headers_indexing_list
    return section_dict_headers_list




def header_content_extraction(html, headers_list):

    section_dict = {}
    section_dict_bullets = {}
    section_dict_bold = {}
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
                        section_dict[component_tag.get_text().replace('.','_') + '[Full Contents]'] = ' '.join(header_tag_sibling_list)
                    if within_para_bold_tag_list:
                        section_dict_bold[component_tag.get_text().replace('.','_') + '[Bold Text]'] = ' '.join(within_para_bold_tag_list)
                    new_tag = BS('').new_tag('kghtmlextractiontag')
                    for bullet_tag in header_tag_sibling_tag_list:
                        new_tag.append(bullet_tag)
                    bundled_bullet_tag_list = []
                    bundled_bullet_tag_list = new_tag.find_all('p', class_ = 'list_Paragraph')
                    bundled_bullet_text_list = []
                    within_para_bold_tag_list = []
                    try:
                        bundled_bullet_text_list = [j.get_text() for j in bundled_bullet_tag_list]
                    except AttributeError:
                        pass
                    if bundled_bullet_text_list:
                        section_dict_bullets[component_tag.get_text().replace('.','_') + '[Bullets Only]'] = ' '.join(bundled_bullet_text_list)
                    del new_tag
                    break
                try:
                    header_tag_sibling_tag_list.append(header_tag_sibling)
                    header_tag_sibling_list.append(header_tag_sibling.get_text())
                    within_para_bold_tag_list += [bold_tag.get_text() for bold_tag in header_tag_sibling.find_all('b')]
                except AttributeError:
                    pass
            else:
                if header_tag_sibling_list:
                    section_dict[component_tag.get_text() + '[Full Contents]'] = ' '.join(header_tag_sibling_list)
                if within_para_bold_tag_list:
                    section_dict_bold[component_tag.get_text() + '[Bold Text]'] = ' '.join(within_para_bold_tag_list)
                new_tag = BS('').new_tag('kghtmlextractiontag')
                for bullet_tag in header_tag_sibling_tag_list:
                    new_tag.append(bullet_tag)
                bundled_bullet_tag_list = []
                bundled_bullet_tag_list = new_tag.find_all('p', class_ = 'list_Paragraph')
                bundled_bullet_text_list = []
                within_para_bold_tag_list = []
                try:
                    bundled_bullet_text_list = [j.get_text() for j in bundled_bullet_tag_list]
                except AttributeError:
                    pass
                if bundled_bullet_text_list:
                    section_dict_bullets[component_tag.get_text() + '[Bullets Only]'] = ' '.join(bundled_bullet_text_list)
                del new_tag
    
    full_content_dict = {**section_dict, **section_dict_bullets, **section_dict_bold}
    return full_content_dict







    
    
        
        
    
            