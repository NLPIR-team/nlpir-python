# coding=utf-8
"""
Tested function:

- :func:`nlpir.native.new_word_finder.NewWordFinder.init_lib`
- :func:`nlpir.native.new_word_finder.NewWordFinder.exit_lib`
- :func:`nlpir.native.new_word_finder.NewWordFinder.get_new_words`
- :func:`nlpir.native.new_word_finder.NewWordFinder.get_file_new_words`
- :func:`nlpir.native.new_word_finder.NewWordFinder.batch_start`
- :func:`nlpir.native.new_word_finder.NewWordFinder.batch_addmen`
- :func:`nlpir.native.new_word_finder.NewWordFinder.batch_addfile`
- :func:`nlpir.native.new_word_finder.NewWordFinder.batch_complete`
- :func:`nlpir.native.new_word_finder.NewWordFinder.batch_getresult`
- :func:`nlpir.native.new_word_finder.NewWordFinder.get_last_error_msg`

"""

from nlpir.native.new_word_finder import NewWordFinder
from nlpir import native, clean_logs
from tests.strings import test_source_filename
import json
import pytest

json_out = native.OUTPUT_FORMAT_JSON


def get_new_word_finder(encode=native.UTF8_CODE):
    return NewWordFinder(encode=encode)


@pytest.mark.run(order=-1)
def test_init_exit():
    new_word_finder = get_new_word_finder()
    new_word_finder.exit_lib()
    clean_logs(include_current=True)


def test_new_word_finder():
    new_word_finder = get_new_word_finder()
    with open(test_source_filename, encoding="utf-8") as f:
        data = f.read()
    assert "主权者" in [_["word"] for _ in json.loads(new_word_finder.get_new_words(
        line=data,
        max_key_limit=100,
        format_opt=json_out
    ))]


def test_file_new_word_finder():
    new_word_finder = get_new_word_finder()
    assert "主权者" in [_["word"] for _ in json.loads(new_word_finder.get_file_new_words(
        file_name=test_source_filename,
        max_key_limit=100,
        format_opt=json_out
    ))]


def test_batch_new_word_finder():
    new_word_finder = get_new_word_finder()
    with open(test_source_filename, encoding='utf-8') as f:
        data = f.read()
    assert new_word_finder.batch_start()
    for i in range(3):
        assert new_word_finder.batch_addmen(text=data)
    for i in range(3):
        assert new_word_finder.batch_addfile(filename=test_source_filename)
    assert new_word_finder.batch_complete()
    assert "主权者" in [_["word"] for _ in json.loads(new_word_finder.batch_getresult(format_json=True))]


def test_get_last_error_msg():
    new_word_finder = get_new_word_finder()
    msg = new_word_finder.get_last_error_msg()
    assert msg is not None
    clean_logs(include_current=True)
