# NLPIR-python  A python wrapper and toolkit for NLPIR

nlpir-python 是一个 [NLPIR](https://github.com/NLPIR-team/NLPIR>) 的python调用包

nlpir-python is a python wrapper for NLPIR modules.

[![Documentation Status](https://readthedocs.org/projects/nlpir-python/badge/?version=latest)](https://nlpir-python.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/nlpir-python.svg)](https://badge.fury.io/py/nlpir-python)
![Test](https://github.com/NLPIR-team/nlpir-python/workflows/test/badge.svg)

- Documentation: https://nlpir-python.rtfd.io
- Github: https://github.com/NLPIR-team/nlpir-python
- Support: https://github.com/NLPIR-team/nlpir-python/issues
- Free software: [MIT license](http://opensource.org/licenses/MIT)

## About

本模块提供两种调用方式:

This package includes two level of method:

##### 1. Native call from Dynamic Link Library(DLL) 原生的直接调用DLL的调用方式

These methods are native method directory from DLL, you can easily use them if you are familiar with the NLPIR modules.

原生方法是直接调用的NLPIR中的api,并进行了部分简化处理,和python化.

```  python
    from nlpir.native import ICTCLAS
    test_str = "法国启蒙思想家孟德斯鸠曾说过：“一切有权力的人都容易滥用" \
               "权力，这是一条千古不变的经验。有权力的人直到把权力用到" \
               "极限方可休止。”另一法国启蒙思想家卢梭从社会契约论的观点" \
               "出发，认为国家权力是公民让渡其全部“自然权利”而获得的，" \
               "他在其名著《社会契约论》中写道：“任何国家权力无不是以民" \
               "众的权力（权利）让渡与公众认可作为前提的”。"
    ictclas = ICTCLAS()
    ictclas.paragraph_process(test_str, 0)
```

##### 2. High-level pythonic method 整合后的更加Python的调用方式

However, the native methods are not very friendly to the beginners. These methods provide a wrapper and tools for the
native call, make it easier to use.

然而,对于一般用户来说,原生api功能强大但是却不是很友好.这里nlpir-python对原生api就行包装, 并提供了一些工具方法,使其更利于使用.

``` python
    from nlpir import ictclas, tools
    tools.update_license()
    test_str = "法国启蒙思想家孟德斯鸠曾说过：“一切有权力的人都容易滥用" \
               "权力，这是一条千古不变的经验。有权力的人直到把权力用到" \
               "极限方可休止。”另一法国启蒙思想家卢梭从社会契约论的观点" \
               "出发，认为国家权力是公民让渡其全部“自然权利”而获得的，" \
               "他在其名著《社会契约论》中写道：“任何国家权力无不是以民" \
               "众的权力（权利）让渡与公众认可作为前提的”。"

    for word, pos in ictclas.segment(test_str, pos_tagged=True):
        print(word, pos)

```

**NOTE**: This module only support python3.6+

**NOTE**: This repo use the git-lfs, please install lfs when pull this repo

## Supported Table

|                   | Native        | Native Doc    | Native Test   | High-Level    | High-Level Doc    | High-Level Test   | Tutorial      | 
| ----              | :----:        | :----:        | :----:        | :----:        | :----:            | :----:            | :----:        |    
| ICTCLAS           |       ✔       |       ✔       |       ✔       |       ✔       |         ✔         |         ✔         |       ✔       |
| NewWordFinder     |       ✔       |       ✔       |       ✔       |       ✔       |         ✔         |         ✔         |               |
| KeyExtract        |       ✔       |       ✔       |       ✔       |       ✔       |         ✔         |         ✔         |               |
| Summary           |       ✔       |       ✔       |       ✔       |       ✔       |         ✔         |         ✔         |               |
| SentimentNew      |       ✔       |       ✔       |       ✍       |               |                   |                   |               |
| SentimentAnalysis |       ✔       |       ✔       |       ✍       |               |                   |                   |               |
| Classify          |       ✔       |       ✔       |       ✍       |               |                   |                   |               |
| DeepClassify      |       ✔       |       ✔       |       ✍       |               |                   |                   |               |
| Cluster           |       ✔       |       ✔       |               |       ✔       |         ✔         |                   |               |
| DocCompare        |               |               |               |               |                   |                   |               |
| DocExtractor      |       ✔       |       ✔       |               |       ✔       |         ✔         |                   |               |
| DocParser         |               |               |               |               |                   |                   |               |
| iEncoder          |               |               |               |               |                   |                   |               |
| HTMLParser        |               |               |               |               |                   |                   |               |
| KeyScanner        |       ✔       |       ✔       |               |       ✔       |         ✔         |                   |               |
| RedupRemover      |               |               |               |               |                   |                   |               |
| SpellChecker      |               |               |               |               |                   |                   |               |
| SplitSentence     |               |               |               |               |                   |                   |               |
| TextSimilarity    |       ✩       |               |               |               |                   |                   |               |
| Word2vec          |               |               |               |               |                   |                   |               |