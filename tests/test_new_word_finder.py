# coding=utf-8
"""
Tested function:

- :func:`nlpir.new_word_finder.find_new_words`
- :func:`nlpir.new_word_finder.find_new_words_batch`
"""
from nlpir import new_word_finder
from tests.strings import test_source_filename


def test_new_word_finder():
    with open(test_source_filename, encoding="utf-8") as f:
        data = f.read()
    assert "主权者" in [_["word"] for _ in new_word_finder.find_new_words(text=data, max_key=100, )]


def test_new_word_finder_batch():
    with open(test_source_filename, encoding="utf-8") as f:
        data = f.read()
    data_list = [data * 3]
    assert "主权者" in [_["word"] for _ in new_word_finder.find_new_words_batch(text_iter=data_list)]
