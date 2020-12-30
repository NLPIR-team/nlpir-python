# coding=utf-8
"""
Tested function:

- :func:`nlpir.key_extract.import_dict`
- :func:`nlpir.key_extract.delete_user_word`
- :func:`nlpir.key_extract.clean_user_dict`
- :func:`nlpir.key_extract.get_key_words`
- :func:`nlpir.key_extract.clean_saved_user_dict`
- :func:`nlpir.key_extract.import_blacklist`
- :func:`nlpir.key_extract.clean_blacklist`
"""
from nlpir import key_extract
from tests.strings import test_str, user_dict_path
import os
import pytest


def test_dict_in_memory():
    from tests.strings import test_str
    assert "孟德斯鸠" not in [i["word"] for i in key_extract.get_key_words(test_str, max_key=10)]
    key_extract.import_dict(["孟德斯鸠"])
    assert "孟德斯鸠" in [i["word"] for i in key_extract.get_key_words(test_str, max_key=10)]
    key_extract.delete_user_word(["孟德斯鸠"])
    assert "孟德斯鸠" not in [i["word"] for i in key_extract.get_key_words(test_str, max_key=10)]
    key_extract.import_dict(["孟德斯鸠"])
    assert "孟德斯鸠" in [i["word"] for i in key_extract.get_key_words(test_str, max_key=10)]
    key_extract.clean_user_dict()


def test_store_dict():
    key_extract.import_dict(["孟德斯鸠"])
    assert key_extract.save_user_dict()
    assert "孟德斯鸠" in [i["word"] for i in key_extract.get_key_words(test_str, max_key=10)]
    assert key_extract.clean_saved_user_dict()


@pytest.mark.run(order=-2)
def test_black_list():
    user_dict = """孟德斯鸠 user\n"""
    with open(user_dict_path, "w", encoding="utf-8") as f:
        f.write(user_dict)
    assert key_extract.import_dict(["孟德斯鸠"])
    assert key_extract.import_blacklist(user_dict_path, ['user'])
    assert "孟德斯鸠" not in [i["word"] for i in key_extract.get_key_words(test_str, max_key=10)]
    assert key_extract.clean_blacklist()
    assert key_extract.clean_saved_user_dict()
    os.remove(user_dict_path)
