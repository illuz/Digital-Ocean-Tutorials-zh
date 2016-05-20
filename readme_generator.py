#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author:      illuz <iilluzen[at]gmail.com>
# File:        readme_generator.py
# Create Date: 2016-05-20 10:24:12
# Usage:       readme_generator.py 
# Descripton:  Generate readme for what I translate.


import os
import re

# Constant
SERIES_PATH = './series'
ARTICLES_PATH = './articles'
SAVE_FILE = './README.md'
README_TEMPLATE = '''
# Digital-Ocean-Tutorials-zh

Digital Ocean Tutorials 上一些文章的翻译，主要为运维相关。https://www.digitalocean.com/community/tutorials

如果有什么问题或错误可以提 Issue。欢迎一起翻译！

---

### 文章列表

这里共有 {total_articles} 篇文章，已经翻译了 {done_articles} 篇，还有 {doing_articles} 篇在翻译中。

{articles_table}

### 系列

这里共有 {total_series} 个系列，已经翻译了 {done_series} 个，还有 {doing_series} 个系列在翻译中。

*注：很多文章是单篇的，没有包含在系列文章中*

{series_table}

---

**仅用作学习翻译用**

'''

# Deal
articles = []
articles_info = { 'total': 0, 'done': 0 }
series = []
series_info = { 'total': 0, 'done': 0 }
origin_link_regex = re.compile(r'原文:(\[.+\]\(.+\))')

def get_origin_link_and_translate_status(file_path):
    origin_link, done = 'Not found', False
    with open(file_path) as f:
        for line in f:
            result = origin_link_regex.match(line)
            if result:
                origin_link = result.group(1)
            if '(已完)' in line:
                done = True
    return origin_link, done

def preprocess_article_and_series():
    def _preprocess(folder_path, container, info):
        for path, subdirs, files in os.walk(folder_path):
            for file_name in files:
                if '.md' not in file_name:
                    continue
                if file_name == 'README.md':
                    continue
                info['total'] = info['total'] + 1
                name = file_name[:-3]
                origin_link, finished = get_origin_link_and_translate_status(path + '/' + file_name)
                if finished:
                    info['done'] = info['done'] + 1
                container.append({'name': name, 'path': './' + path + '/' + file_name, 'origin_link': origin_link, 'done': finished})
    _preprocess(SERIES_PATH, series, series_info)
    _preprocess(ARTICLES_PATH, articles, articles_info)
    # print(series)
    # print(articles)
    
def get_articles_table():
    table = '| 译文 | 原文 | 状态 |\n|------|------|------|\n'
    for item in articles:
        table += '| [{}]({}) | {} | {} |'.format(item.get('name', 'FAILED'), item.get('path', 'FAILED'), item.get('origin_link', 'FAILED'), '翻译完成' if item.get('done', False) else '翻译中')
    return table

def get_series_table():
    table = '| 系列名 | 原链接 | 状态 |\n|------|------|------|\n'
    for item in series:
        table += '| [{}]({}) | {} | {} |'.format(item.get('name', 'FAILED'), item.get('path', 'FAILED'), item.get('origin_link', 'FAILED'), '翻译完成' if item.get('done', False) else '翻译中')
    return table

def print_readme():
    print(README_TEMPLATE.format(
        total_articles  = articles_info['total'],
        done_articles   = articles_info['done'],
        doing_articles  = articles_info['total'] - articles_info['done'],
        articles_table  = get_articles_table(),
        total_series    = series_info['total'],
        done_series     = series_info['done'],
        doing_series    = series_info['total'] - series_info['done'],
        series_table    = get_series_table()
    ))

def main():
    preprocess_article_and_series()
    print_readme()

if __name__ == '__main__':
    main()
