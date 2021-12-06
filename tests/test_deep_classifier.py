# coding=utf-8
"""
Tested function:

- :func:`nlpir.deep_classifier.classify`
"""
from nlpir import deep_classifier


def test_classify():
    from tests.strings import test_str
    assert deep_classifier.classify(txt=test_str) == "教育"
