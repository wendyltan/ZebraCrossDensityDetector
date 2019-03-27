#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2019/3/27 18:39
# @Author  : wendy
# @Usage   : 
# @File    : markdown_convertor.py
# @Software: PyCharm

import markdown
import codecs

html = '''
<html lang="zh-cn">
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type" />
<link href="github-markdown.css" rel="stylesheet">
</head>
<body>
%s
</body>
</html>'''
def convert(filename):
    name = filename
    in_file = '%s.md' % (name)
    out_file = '%s.html' % (name)

    input_file = codecs.open(in_file, mode="r", encoding="utf-8")
    text = input_file.read()
    body = markdown.markdown(text)

    output_file = codecs.open(out_file, "w",encoding="utf-8",errors="xmlcharrefreplace")
    output_file.write(html % body)
